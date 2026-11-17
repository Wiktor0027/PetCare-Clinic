"""Obsługa bazy SQLite z katalogiem zabiegów."""

import csv
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from models import CATEGORIES, CLASS_BY_ID, Treatment, TreatmentCatalog


DATA_DIR = Path(__file__).resolve().parent / "data"
DEFAULT_DB_PATH = DATA_DIR / "petcare.sqlite3"
LEGACY_JSON_PATH = DATA_DIR / "vet_catalog.json"


def _catalog_from_legacy(data):
    """Wczytaj zapisane zabiegi bez ponownej walidacji formularza."""
    catalog = TreatmentCatalog(data.get("name", "PetCare"))
    for item in data.get("treatments", []):
        treatment = Treatment.from_dict(item)
        catalog.treatments.append(treatment)
    catalog.next_id = max(
        (item.treatment_id or 0 for item in catalog.treatments), default=0
    ) + 1
    return catalog


@contextmanager
def _connect(db_path=DEFAULT_DB_PATH):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize_database(db_path=DEFAULT_DB_PATH, legacy_path=LEGACY_JSON_PATH):
    """Utwórz tabele i jednorazowo zaimportuj katalog z JSON."""
    with _connect(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS treatments (
                treatment_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price_pln REAL NOT NULL CHECK (price_pln > 0),
                duration_min INTEGER NOT NULL CHECK (duration_min > 0),
                is_active INTEGER NOT NULL CHECK (is_active IN (0, 1)),
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        """)
        connection.executemany(
            "INSERT OR IGNORE INTO categories(category_id, name) VALUES (?, ?)",
            [(category_id, name) for category_id, name in CATEGORIES.items()],
        )
        count = connection.execute("SELECT COUNT(*) FROM treatments").fetchone()[0]

    if count == 0 and Path(legacy_path).exists():
        with open(legacy_path, encoding="utf-8-sig") as source:
            legacy = json.load(source)
        catalog = _catalog_from_legacy(legacy)
        with _connect(db_path) as connection:
            connection.executemany("""
                INSERT INTO treatments
                    (treatment_id, name, price_pln, duration_min, is_active, category_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (item.treatment_id, item.name, item.price_pln, item.duration_min,
                 int(item.is_active), next(key for key, value in CATEGORIES.items()
                                           if value == item.category))
                for item in catalog.treatments
            ])


def load_catalog(db_path=DEFAULT_DB_PATH):
    initialize_database(db_path)
    catalog = TreatmentCatalog("PetCare")
    with _connect(db_path) as connection:
        rows = connection.execute("""
            SELECT t.treatment_id, t.name, t.price_pln, t.duration_min,
                   t.is_active, c.name AS category
            FROM treatments AS t
            JOIN categories AS c ON c.category_id = t.category_id
            ORDER BY t.treatment_id
        """).fetchall()
        for row in rows:
            category_id = next(key for key, value in CATEGORIES.items()
                               if value == row["category"])
            treatment = CLASS_BY_ID[category_id](
                row["name"], row["price_pln"], row["duration_min"],
                bool(row["is_active"]), row["treatment_id"]
            )
            # Nie sprawdzaj ponownie limitów dla zapisanych danych.
            catalog.treatments.append(treatment)
            catalog.next_id = max(catalog.next_id, treatment.treatment_id + 1)
    return catalog


def add_treatment(treatment, db_path=DEFAULT_DB_PATH):
    initialize_database(db_path)
    category_id = next(key for key, value in CATEGORIES.items()
                       if value == treatment.category)
    with _connect(db_path) as connection:
        cursor = connection.execute("""
            INSERT INTO treatments
                (name, price_pln, duration_min, is_active, category_id)
            VALUES (?, ?, ?, ?, ?)
        """, (treatment.name, treatment.price_pln, treatment.duration_min,
              int(treatment.is_active), category_id))
        treatment.treatment_id = cursor.lastrowid
    return treatment


def save_catalog(catalog, db_path=DEFAULT_DB_PATH):
    """Zastąp zabiegi w jednej transakcji."""
    initialize_database(db_path)
    with _connect(db_path) as connection:
        connection.execute("DELETE FROM treatments")
        connection.executemany("""
            INSERT INTO treatments
                (treatment_id, name, price_pln, duration_min, is_active, category_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (item.treatment_id, item.name, item.price_pln, item.duration_min,
             int(item.is_active), next(key for key, value in CATEGORIES.items()
                                       if value == item.category))
            for item in catalog.treatments
        ])


def update_prices_report(price_path, db_path=DEFAULT_DB_PATH):
    initialize_database(db_path)
    updates = {}
    errors = []
    with open(price_path, newline="", encoding="utf-8-sig") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                treatment_id = int(row["id"])
                price = float(row["price"].replace(",", "."))
                if price <= 0:
                    raise ValueError
                updates[treatment_id] = price
            except (KeyError, TypeError, ValueError):
                errors.append(f"Wiersz {line_number}: niepoprawne ID lub cena")
    with _connect(db_path) as connection:
        cursor = connection.executemany(
            "UPDATE treatments SET price_pln = ? WHERE treatment_id = ?",
            [(price, treatment_id) for treatment_id, price in updates.items()],
        )
        updated = cursor.rowcount
    return updated, errors


def csv_export(csv_path, db_path=DEFAULT_DB_PATH):
    catalog = load_catalog(db_path)
    fieldnames = ["treatment_id", "name", "price_pln", "duration_min", "is_active", "category"]
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for treatment in catalog.treatments:
            writer.writerow(treatment.to_dict())
