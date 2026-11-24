# Sprawozdanie z Zadania Laboratoryjnego nr 4
**Przedmiot:** Programowanie w języku Python (`IwIK-S1`)
**Projekt:** PetCare Clinic
**Zespół (Autorzy):**
1. Wiktor Paszyński (nr albumu: 164865) – login Git: `Wiktor0027`
2. Michał Nowak (nr albumu: 164855) – login Git: `Michal-misiek`
**Data oddania:** 24.11.2026

---

## 1. Cel i Zakres Inżynierski Zadania
*

---

## 2. Architektura Rozwiązania i Struktura Modułów
*(Wykaz zrealizowanych plików w katalogu `src/` wraz z przypisaniem ich odpowiedzialności).*
* `src/data.py` – Przechowuje kopię awaryjną bazy danych
* `src/validators.py` – Przechowuje walidatory wprowadzanych danych
* `src/services.py` – Zawiera funkcje dodawania i wyświetlania list
* `src/storage.py` - Odpowiada za wszelką funkcjonalność związaną z operacjami na plikach
* `src/models.py` - Odpowiada za przekształcenie działania programu na model OOP (Object-Oriented Programming)
* `src/test_models.py` - Zawiera testy modułu models
* `src/database.py` - Odpowiada za połączenie z bazą danych
* `src/migrate_database.py` - Migracja bazy danych JSON do SQLite
* `src/sqlite_storage.py` - Odpowiada za obsługę bazy danych SQLite
* `src/test_database.py` - Zawiera testy bazy danych SQLite
* `src/patient_repository.py` - Odpowiada za zarządzanie danymi pacjentów
* `src/analytics.py` - Zawiera wszelką funckjonalność danych analitycznych bazy danych SQLite
* `src/main.py` – Odpowiada za implementację innych modułów oraz menu CLI
* `src/data/` - Folder przechowuje bazy danych oraz ich kopie zapasowe

---

## 3. Kluczowy Fragment Kodu i Uzasadnienie Inżynierskie
*(Wybrany, najważniejszy lub najciekawszy fragment kodu źródłowego zrealizowany w tym etapie – maksymalnie 15–25 linii).*

```python
def get_connection(db_path=DEFAULT_DB_PATH):
    """Otwórz bazę z włączonymi kluczami obcymi i wierszami dostępnymi po nazwie."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
```

**Uzasadnienie wyboru:**
Przedstawiony fragment kodu z modułu database.py odpowiada - jak wskazuje sama nazwa funkcji - za ustanowienie połączenia z bazą danych. Bez tego ta część zadania byłaby niemożliwa do wykonania po stronie użytkownika.

---

## 4. Scenariusze Weryfikacji i Wyniki Testów
*(Dowód działania programu w konsoli. Należy przedstawić przynajmniej dwa scenariusze).*

### Scenariusz A: Ścieżka poprawna (Happy Path)
* **Dane wejściowe:** 8, Enter, 9, Enter, 11, 2026, Enter, 10, Enter, Enter, Enter, 0
* **Oczekiwany i uzyskany wynik:**
```text
========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
6. Dodaj pacjenta
7. Odczytaj pacjenta po ID
8. Wyświetl wszystkich pacjentów
9. Raport pacjentów (wizyty i koszty)
10. Raport według gatunków
11. Przychód miesięczny
12. Top pacjenci według kosztów
13. Statystyki katalogu zabiegów
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-13]: 8

Brak zapisanych pacjentów.
Naciśnij Enter, aby kontynuować.

========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
6. Dodaj pacjenta
7. Odczytaj pacjenta po ID
8. Wyświetl wszystkich pacjentów
9. Raport pacjentów (wizyty i koszty)
10. Raport według gatunków
11. Przychód miesięczny
12. Top pacjenci według kosztów
13. Statystyki katalogu zabiegów
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-13]: 9

Raport pacjentów (wizyty i koszty)
Brak zapisanych pacjentów.

Naciśnij Enter, aby kontynuować.

========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
6. Dodaj pacjenta
7. Odczytaj pacjenta po ID
8. Wyświetl wszystkich pacjentów
9. Raport pacjentów (wizyty i koszty)
10. Raport według gatunków
11. Przychód miesięczny
12. Top pacjenci według kosztów
13. Statystyki katalogu zabiegów
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-13]: 11
Podaj rok: 2026

Przychód miesięczny z zakończonych wizyt w 2026 r.:
Brak zakończonych wizyt w tym roku.

Naciśnij Enter, aby kontynuować.

========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
6. Dodaj pacjenta
7. Odczytaj pacjenta po ID
8. Wyświetl wszystkich pacjentów
9. Raport pacjentów (wizyty i koszty)
10. Raport według gatunków
11. Przychód miesięczny
12. Top pacjenci według kosztów
13. Statystyki katalogu zabiegów
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-13]: 10

Raport według gatunków
Od daty (RRRR-MM-DD, Enter = bez ograniczenia): 
Do daty (RRRR-MM-DD, Enter = bez ograniczenia): 
Brak danych.

Naciśnij Enter, aby kontynuować.

========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
6. Dodaj pacjenta
7. Odczytaj pacjenta po ID
8. Wyświetl wszystkich pacjentów
9. Raport pacjentów (wizyty i koszty)
10. Raport według gatunków
11. Przychód miesięczny
12. Top pacjenci według kosztów
13. Statystyki katalogu zabiegów
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-13]: 0
Zamykanie programu. Do widzenia!

Process finished with exit code 0
```

### Scenariusz B: Obsługa błędów i wartości brzegowych
* **Dane wejściowe (błędne):** 11, -2 (błędne), 3000 (błędne), 2000, Enter, 0
* **Reakcja programu:**
```text
========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
6. Dodaj pacjenta
7. Odczytaj pacjenta po ID
8. Wyświetl wszystkich pacjentów
9. Raport pacjentów (wizyty i koszty)
10. Raport według gatunków
11. Przychód miesięczny
12. Top pacjenci według kosztów
13. Statystyki katalogu zabiegów
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-13]: 11
Podaj rok: -2
Błąd: Wartość < 1900
Podaj rok: 3000
Błąd: Wartość > 2100
Podaj rok: 2000

Przychód miesięczny z zakończonych wizyt w 2000 r.:
Brak zakończonych wizyt w tym roku.

Naciśnij Enter, aby kontynuować.

========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
6. Dodaj pacjenta
7. Odczytaj pacjenta po ID
8. Wyświetl wszystkich pacjentów
9. Raport pacjentów (wizyty i koszty)
10. Raport według gatunków
11. Przychód miesięczny
12. Top pacjenci według kosztów
13. Statystyki katalogu zabiegów
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-13]: 0
Zamykanie programu. Do widzenia!

Process finished with exit code 0
```

---

## 5. Podział Pracy w Zespole
*(Precyzyjne i uczciwe rozliczenie wkładu obu członków zespołu – weryfikowane z historią commitów `git log`).*
* **Wiktor Paszyński:**
  * Odpowiedzialność za moduły: `analitcs.py`, `main.py`
  * Zaimplementowane funkcjonalności: Implementacja danych analitycznych - funckjonalność, użycie w menu CLI. Sporządzenie sprawozdania.
  * Liczba wykonanych commitów: 3
* **Michał Nowak:**
  * Odpowiedzialność za moduły: `sqlite_storage.py`, `database.py`, `patient_repository.py`, `migrate_database.py`, `test_database.py`, `main.py`
  * Zaimplementowane funkcjonalności: Większość funkcjonalności związanej z bazą danych SQLite. Migracja z JSON na SQLite. Testy nowej bazy danych. Dodanie bazy danych pacjentów kliniki wraz z odpowiednią funkcjonalnością.
  * Liczba wykonanych commitów: 6
