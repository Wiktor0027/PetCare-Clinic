"""Testy schematu, repozytorium i migracji bazy kliniki."""

import json
import sqlite3
import tempfile
from pathlib import Path

from database import get_connection, initialize_schema
from migrate_database import migrate_json_to_sqlite
from patient_repository import PatientRepository


def test_schema_and_foreign_key():
    with tempfile.TemporaryDirectory() as folder:
        db_path = Path(folder) / "test.sqlite3"
        initialize_schema(db_path, Path(folder) / "missing.json")
        connection = get_connection(db_path)
        try:
            tables = {row["name"] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )}
            assert {"patients", "medical_visits"} <= tables
            foreign_keys = connection.execute(
                "PRAGMA foreign_key_list(medical_visits)"
            ).fetchall()
            assert foreign_keys[0]["on_delete"] == "CASCADE"
            try:
                connection.execute("""
                    INSERT INTO medical_visits
                        (patient_id, visit_date, diagnosis, cost_pln, is_completed)
                    VALUES (999, '2026-01-01', 'test', 10, 0)
                """)
                assert False, "Brak kontroli klucza obcego"
            except sqlite3.IntegrityError:
                pass
        finally:
            connection.close()


def test_repository_save_read_and_cascade_delete():
    with tempfile.TemporaryDirectory() as folder:
        db_path = Path(folder) / "test.sqlite3"
        repository = PatientRepository(db_path)
        patient_id = repository.save_patient({
            "name": "Burek",
            "species": "Pies",
            "owner_phone": "123456789",
            "medical_visits": [{
                "visit_date": "2026-11-17",
                "diagnosis": "Kontrola",
                "cost_pln": 80.0,
                "is_completed": True,
            }],
        })
        patient = repository.get_patient(patient_id)
        assert patient["name"] == "Burek"
        assert len(patient["medical_visits"]) == 1
        assert patient["medical_visits"][0]["diagnosis"] == "Kontrola"

        assert repository.delete_patient(patient_id) is True
        connection = get_connection(db_path)
        try:
            count = connection.execute(
                "SELECT COUNT(*) FROM medical_visits WHERE patient_id = ?",
                (patient_id,),
            ).fetchone()[0]
            assert count == 0
        finally:
            connection.close()


def test_json_migration_and_backup():
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        json_path = folder / "legacy.json"
        db_path = folder / "test.sqlite3"
        json_path.write_text(json.dumps({"patients": [{
            "name": "Mruczek",
            "species": "Kot",
            "owner_phone": "987654321",
            "medical_visits": [{
                "visit_date": "2026-11-17",
                "diagnosis": "Szczepienie",
                "cost_pln": 60,
                "is_completed": False,
            }],
        }]}), encoding="utf-8")

        result = migrate_json_to_sqlite(json_path, db_path)
        assert result["patients"] == 1
        assert result["archive"].exists()
        patient = PatientRepository(db_path).get_patient(1)
        assert patient["name"] == "Mruczek"
        assert len(patient["medical_visits"]) == 1


if __name__ == "__main__":
    tests = [
        test_schema_and_foreign_key,
        test_repository_save_read_and_cascade_delete,
        test_json_migration_and_backup,
    ]
    for test in tests:
        test()
        print(f"OK  {test.__name__}")
    print("Wszystkie testy bazy przeszły.")
