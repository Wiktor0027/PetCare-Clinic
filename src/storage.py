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
    dir_path = Path(__file__).resolve().parent.parent / "data"
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def atomic_save_menu(catalog: list[dict]) -> None:
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
    source = get_data_dir()
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