"""Repozytorium zapisujące pacjentów i ich wizyty w SQLite."""

from database import (
    DEFAULT_DB_PATH,
    LEGACY_JSON_PATH,
    get_connection,
    initialize_schema,
)


class PatientRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH, legacy_path=LEGACY_JSON_PATH):
        self.db_path = db_path
        initialize_schema(db_path, legacy_path)

    def save_patient(self, patient):
        """Zapisz pacjenta wraz z wizytami jako jedną transakcję."""
        return self.save_patients([patient])[0]

    def save_patients(self, patients):
        """Zapisz wiele agregatów pacjentów w jednej transakcji."""
        connection = get_connection(self.db_path)
        try:
            with connection:
                patient_ids = []
                for patient in patients:
                    cursor = connection.execute(
                        "INSERT INTO patients (name, species, owner_phone) VALUES (?, ?, ?)",
                        (patient["name"], patient["species"], patient["owner_phone"]),
                    )
                    patient_id = cursor.lastrowid
                    patient_ids.append(patient_id)
                    connection.executemany("""
                        INSERT INTO medical_visits
                            (patient_id, visit_date, diagnosis, cost_pln, is_completed)
                        VALUES (?, ?, ?, ?, ?)
                    """, [
                        (patient_id, visit["visit_date"], visit["diagnosis"],
                         visit["cost_pln"], int(visit["is_completed"]))
                        for visit in patient.get("medical_visits", [])
                    ])
            return patient_ids
        finally:
            connection.close()

    def get_patient(self, patient_id):
        """Pobierz pacjenta razem z jego wizytami; zwróć None, jeśli go brak."""
        connection = get_connection(self.db_path)
        try:
            patient = connection.execute(
                "SELECT patient_id, name, species, owner_phone "
                "FROM patients WHERE patient_id = ?", (patient_id,)
            ).fetchone()
            if patient is None:
                return None
            visits = connection.execute("""
                SELECT visit_id, patient_id, visit_date, diagnosis, cost_pln, is_completed
                FROM medical_visits WHERE patient_id = ? ORDER BY visit_id
            """, (patient_id,)).fetchall()
            result = dict(patient)
            result["medical_visits"] = [dict(visit) for visit in visits]
            return result
        finally:
            connection.close()

    def delete_patient(self, patient_id):
        """Usuń pacjenta; baza automatycznie usunie również jego wizyty."""
        connection = get_connection(self.db_path)
        try:
            with connection:
                cursor = connection.execute(
                    "DELETE FROM patients WHERE patient_id = ?", (patient_id,)
                )
                return cursor.rowcount > 0
        finally:
            connection.close()
