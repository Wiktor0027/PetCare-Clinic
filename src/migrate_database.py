"""Jednorazowo przenosi dane JSON do bazy SQLite."""

import argparse
import json
import shutil
from pathlib import Path

from database import DEFAULT_DB_PATH, LEGACY_JSON_PATH, get_connection, initialize_schema
from patient_repository import PatientRepository


def migrate_json_to_sqlite(json_path=LEGACY_JSON_PATH, db_path=DEFAULT_DB_PATH):
    json_path = Path(json_path)
    initialize_schema(db_path, json_path)
    if not json_path.exists():
        return {"patients": 0, "archive": None}

    with json_path.open(encoding="utf-8-sig") as source:
        legacy_data = json.load(source)

    connection = get_connection(db_path)
    try:
        patient_count = connection.execute(
            "SELECT COUNT(*) FROM patients"
        ).fetchone()[0]
    finally:
        connection.close()

    migrated = 0
    if patient_count == 0:
        repository = PatientRepository(db_path, json_path)
        migrated = len(repository.save_patients(legacy_data.get("patients", [])))

    archive_path = json_path.with_suffix(json_path.suffix + ".bak")
    if not archive_path.exists():
        shutil.copy2(json_path, archive_path)
    return {"patients": migrated, "archive": archive_path}


def main():
    parser = argparse.ArgumentParser(description="Migracja danych PetCare do SQLite")
    parser.add_argument("--json", default=str(LEGACY_JSON_PATH), help="Plik źródłowy JSON")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Plik bazy SQLite")
    args = parser.parse_args()
    result = migrate_json_to_sqlite(args.json, args.db)
    print(f"Przeniesiono pacjentów: {result['patients']}")
    if result["archive"]:
        print(f"Kopia JSON: {result['archive']}")


if __name__ == "__main__":
    main()
