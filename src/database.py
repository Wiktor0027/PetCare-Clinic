"""Połączenie i schemat bazy danych kliniki."""

import sqlite3
from pathlib import Path

from sqlite_storage import DEFAULT_DB_PATH, LEGACY_JSON_PATH, initialize_database


def get_connection(db_path=DEFAULT_DB_PATH):
    """Otwórz bazę z włączonymi kluczami obcymi i wierszami dostępnymi po nazwie."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_schema(db_path=DEFAULT_DB_PATH, legacy_path=LEGACY_JSON_PATH):
    """Przygotuj bazę katalogu oraz tabele pacjentów i wizyt."""
    initialize_database(db_path, legacy_path)
    connection = get_connection(db_path)
    try:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    species TEXT NOT NULL CHECK (species IN ('Pies', 'Kot', 'Gryzon')),
                    owner_phone TEXT NOT NULL
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS medical_visits (
                    visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    visit_date TEXT NOT NULL,
                    diagnosis TEXT NOT NULL,
                    cost_pln REAL NOT NULL CHECK (cost_pln >= 0),
                    is_completed INTEGER NOT NULL CHECK (is_completed IN (0, 1)),
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                        ON DELETE CASCADE
                )
            """)
    finally:
        connection.close()
