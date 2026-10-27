import csv
import datetime
import json
import os
import shutil
import tempfile
from json import JSONDecodeError
from pathlib import Path

import data


def load_database(name: str) -> None:
    try:
        with open(name, "r") as file:
            db = json.load(file)
    except FileNotFoundError:
        print("Błąd: Plik nie istnieje.")
        db = data.vet_catalog  # Odczyt kopii zapasowej w przypadku błędu odczytu pliku
    except PermissionError:
        print("Błąd: Brak dostępu do pliku.")
        db = data.vet_catalog  # Odczyt kopii zapasowej w przypadku błędu odczytu pliku
    except JSONDecodeError:
        print("Błąd: Nie udało się odczytać pliku.")
        db = data.vet_catalog  # Odczyt kopii zapasowej w przypadku błędu odczytu pliku
    return db

def save_database(name: str, db: None) -> None:
    try:
        with open(name, "w") as json_file:
            json.dump(db, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Błąd: Plik nie istnieje.")
    except PermissionError:
        print("Błąd: Brak dostępu do pliku.")
    except JSONDecodeError:
        print("Błąd: Nie udało się odczytać pliku.")

def update_prices(database, price_path):
    with open(database) as json_file:
        datab = json.load(json_file)
    with open(price_path) as csv_file:
        prices = {int(row["id"]): float(row["price"].replace(",",".")) for row in csv.DictReader(csv_file)}
    for product in datab:
        if product["id"] in prices:
            product["price"] = prices[product["id"]]
    with open(database, "w") as json_file:
        json.dump(datab, json_file, ensure_ascii=False, indent=2)

def csv_export(csv_name):
    with open("data/vet_catalog.json",'r') as json_file:
        datab = json.load(json_file)
    headers =list(datab[0].keys())
    with open(csv_name + ".csv", "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for row in datab:
            writer.writerow(row)

def get_data_dir() -> Path:
    dir_path = Path(__file__).resolve().parent / "data"
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def atomic_save_menu(catalog: list[dict]) -> None:
    backup_menu()
    target = get_data_dir() / "vet_catalog.json"
    with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            dir=get_data_dir(),
            prefix="vet_catalog_tmp_",
            suffix=".json",
            encoding="utf-8"
    ) as tmp:
        json.dump(catalog, tmp, ensure_ascii=False, indent=4)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_path = Path(tmp.name)
    os.replace(temp_path, target)

def backup_menu(keep: int = 3) -> Path | None:
    source = get_data_dir() / "vet_catalog.json"
    if not source.exists():
        return None
    backup_dir = get_data_dir() / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    target_backup = backup_dir / f"vet_catalog_{stamp}.bak"
    shutil.copy2(source, target_backup)

    current_backups = sorted(backup_dir.glob("vet_catalog_*.bak"))
    while len(current_backups) > keep:
        oldest = current_backups.pop(0)
        oldest.unlink(missing_ok=True)
    return target_backup

def update_prices_report(database_path, price_path):
    success_count = 0
    errors_report = []
    prices_to_update = {}

    with open(price_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for line_num, row in enumerate(reader, start=2):
            row_errors = []

            product_id = row.get("id")
            if not product_id:
                row_errors.append("brakujące ID")
            elif not product_id.isdigit():
                row_errors.append("ID nie jest liczbą całkowitą")

            if "name" in row and not row.get("name"):
                row_errors.append("brakująca nazwa")

            raw_price = row.get("price")
            price_float = None
            if not raw_price:
                row_errors.append("brakująca cena")
            else:
                clean_price = raw_price.replace(",", ".")
                try:
                    price_float = float(clean_price)
                except ValueError:
                    row_errors.append(f"Cena nie jest poprawną liczbą (podano: '{raw_price}')")

            if row_errors:
                errors_report.append({
                    "row": line_num,
                    "row_data": dict(row),
                    "errors": row_errors,
                })
            else:
                prices_to_update[int(product_id)] = price_float
                success_count += 1

    print(f"Pomyślnie zweryfikowano {success_count} wierszy z pliku CSV.")
    if errors_report:
        print(f"Znaleziono błędy w {len(errors_report)} wierszach: {errors_report}")

    if prices_to_update and os.path.exists(database_path):
        with open(database_path, 'r', encoding='utf-8') as json_file:
            datab = json.load(json_file)

        zaktualizowano_w_bazie = 0

        for product in datab:
            prod_id = int(product["id"])
            if prod_id in prices_to_update:
                product["price"] = prices_to_update[prod_id]
                zaktualizowano_w_bazie += 1

        with open(database_path, 'w', encoding='utf-8') as json_file:
            json.dump(datab, json_file, ensure_ascii=False, indent=2)

        print(f"Zaktualizowano ceny dla {zaktualizowano_w_bazie} produktów w bazie danych JSON.")
    else:
        print("Brak poprawnych danych do zaktualizowania bazy lub plik bazy nie istnieje.")
