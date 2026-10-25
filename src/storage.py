import csv
import json
from json import JSONDecodeError

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