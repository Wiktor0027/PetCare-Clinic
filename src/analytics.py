"""Raporty analityczne kliniki: JOIN, GROUP BY oraz agregacje SUM / AVG.

Wszystkie zapytania są parametryzowane (placeholdery ?) - żadna wartość
od użytkownika nie jest doklejana do tekstu SQL.
"""

from database import DEFAULT_DB_PATH, LEGACY_JSON_PATH, get_connection, initialize_schema


class ClinicAnalytics:
    def __init__(self, db_path=DEFAULT_DB_PATH, legacy_path=LEGACY_JSON_PATH):
        self.db_path = db_path
        initialize_schema(db_path, legacy_path)

    def _query(self, sql, params=()):
        connection = get_connection(self.db_path)
        try:
            return [dict(row) for row in connection.execute(sql, params).fetchall()]
        finally:
            connection.close()

    def patient_report(self, only_completed=None, min_total=0.0):
        """Wizyty i koszty per pacjent (LEFT JOIN + GROUP BY + COUNT/SUM/AVG).

        only_completed: None = wszystkie wizyty, True/False = tylko
        zakończone / niezakończone. Warunek jest w ON, żeby pacjenci bez
        pasujących wizyt nadal pojawiali się w raporcie (z zerami).
        min_total: filtr HAVING na łączny koszt.
        """
        flag = None if only_completed is None else int(only_completed)
        return self._query("""
            SELECT p.patient_id,
                   p.name,
                   p.species,
                   COUNT(v.visit_id)                       AS visits,
                   COALESCE(SUM(v.cost_pln), 0)            AS total_cost,
                   ROUND(AVG(v.cost_pln), 2)               AS avg_cost
            FROM patients AS p
            LEFT JOIN medical_visits AS v
                   ON v.patient_id = p.patient_id
                  AND (? IS NULL OR v.is_completed = ?)
            GROUP BY p.patient_id, p.name, p.species
            HAVING COALESCE(SUM(v.cost_pln), 0) >= ?
            ORDER BY total_cost DESC, p.patient_id
        """, (flag, flag, min_total))

    def species_report(self, date_from=None, date_to=None):
        """Statystyki per gatunek w opcjonalnym przedziale dat (RRRR-MM-DD)."""
        return self._query("""
            SELECT p.species,
                   COUNT(DISTINCT p.patient_id)            AS patients,
                   COUNT(v.visit_id)                       AS visits,
                   COALESCE(SUM(v.cost_pln), 0)            AS total_cost,
                   ROUND(AVG(v.cost_pln), 2)               AS avg_cost
            FROM patients AS p
            LEFT JOIN medical_visits AS v
                   ON v.patient_id = p.patient_id
                  AND (? IS NULL OR v.visit_date >= ?)
                  AND (? IS NULL OR v.visit_date <= ?)
            GROUP BY p.species
            ORDER BY total_cost DESC, p.species
        """, (date_from, date_from, date_to, date_to))

    def monthly_revenue(self, year):
        """Przychód z zakończonych wizyt w podziale na miesiące danego roku."""
        return self._query("""
            SELECT substr(v.visit_date, 1, 7)              AS month,
                   COUNT(*)                                AS visits,
                   SUM(v.cost_pln)                         AS revenue,
                   ROUND(AVG(v.cost_pln), 2)               AS avg_cost
            FROM medical_visits AS v
            WHERE v.is_completed = 1
              AND substr(v.visit_date, 1, 4) = ?
            GROUP BY month
            ORDER BY month
        """, (str(year),))

    def top_patients(self, limit=5):
        """Pacjenci o najwyższych łącznych kosztach (INNER JOIN + LIMIT)."""
        return self._query("""
            SELECT p.patient_id, p.name, p.species,
                   COUNT(v.visit_id)                       AS visits,
                   SUM(v.cost_pln)                         AS total_cost
            FROM patients AS p
            JOIN medical_visits AS v ON v.patient_id = p.patient_id
            GROUP BY p.patient_id, p.name, p.species
            ORDER BY total_cost DESC, p.patient_id
            LIMIT ?
        """, (int(limit),))

    def treatment_category_report(self, min_count=0):
        """Katalog zabiegów per kategoria (JOIN categories + GROUP BY).

        LEFT JOIN zachowuje puste kategorie; HAVING odfiltrowuje kategorie
        z mniejszą liczbą zabiegów niż min_count.
        """
        return self._query("""
            SELECT c.name                                  AS category,
                   COUNT(t.treatment_id)                   AS treatments,
                   COALESCE(SUM(t.is_active), 0)           AS active,
                   COALESCE(SUM(t.price_pln), 0)           AS total_price,
                   ROUND(AVG(t.price_pln), 2)              AS avg_price,
                   ROUND(AVG(t.duration_min), 1)           AS avg_duration
            FROM categories AS c
            LEFT JOIN treatments AS t ON t.category_id = c.category_id
            GROUP BY c.category_id, c.name
            HAVING COUNT(t.treatment_id) >= ?
            ORDER BY c.category_id
        """, (min_count,))


def format_table(rows, columns, empty_message="Brak danych."):
    """Wypisz listę słowników jako tabelę tekstową.

    columns: lista krotek (klucz, nagłówek, szerokość).
    """
    if not rows:
        print(empty_message)
        return
    print(" | ".join(f"{title:<{width}}" for _, title, width in columns))
    print("-" * (sum(width for _, _, width in columns) + 3 * (len(columns) - 1)))
    for row in rows:
        cells = []
        for key, _, width in columns:
            value = row[key]
            if value is None:
                value = "-"
            elif isinstance(value, float):
                value = f"{value:.2f}"
            cells.append(f"{str(value):<{width}}")
        print(" | ".join(cells))
