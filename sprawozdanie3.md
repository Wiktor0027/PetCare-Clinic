# Sprawozdanie z Zadania Laboratoryjnego nr 3
**Przedmiot:** Programowanie w języku Python (`IwIK-S1`)
**Projekt:** PetCare Clinic
**Zespół (Autorzy):**
1. Wiktor Paszyński (nr albumu: 164865) – login Git: `Wiktor0027`
2. Michał Nowak (nr albumu: 164855) – login Git: `Michal-misiek`
**Data oddania:** 10.11.2026

---

## 1. Cel i Zakres Inżynierski Zadania
*Aktualizacja systemu zarządzania Kliniką PetCare w celu odejścia od list i przejścia na model OOP - klasy.

---

## 2. Architektura Rozwiązania i Struktura Modułów
*(Wykaz zrealizowanych plików w katalogu `src/` wraz z przypisaniem ich odpowiedzialności).*
* `src/data.py` – Przechowuje kopię awaryjną bazy danych
* `src/validators.py` – Przechowuje walidatory wprowadzanych danych
* `src/services.py` – Zawiera funkcje dodawania i wyświetlania list
* `src/storage.py` - Odpowiada za wszelką funkcjonalność związaną z operacjami na plikach
* `src/models.py` - Odpowiada za przekształcenie działania programu na model OOP (Object-Oriented Programming)
* `src/test_models.py` - Zawiera testy modułu models
* `src/main.py` – Odpowiada za implementację innych modułów oraz menu CLI
* `src/data/` - Folder przechowuje bazy danych oraz ich kopie zapasowe

---

## 3. Kluczowy Fragment Kodu i Uzasadnienie Inżynierskie
*(Wybrany, najważniejszy lub najciekawszy fragment kodu źródłowego zrealizowany w tym etapie – maksymalnie 15–25 linii).*

```python
        case 3:
            print("\nOferta zabiegów - sortowanie wg kryteriów")
            while True:
                print("\n1. Sortuj po cenie rosnąco")
                print("2. Sortuj po cenie malejąco")
                print("3. Pokaż tylko dostępne")
                print("4. Pokaż tylko niedostępne")
                print("0. Wyjście")
                choice = get_int_input("\nWybierz opcję [0-4]: ", 0, 4)
                if choice == 0:
                    break
                elif choice == 1:
                    output = catalog.sorted_by_price()
                    title ="=== Produkty posortowane po cenie rosnąco ==="
                elif choice == 2:
                    output = catalog.sorted_by_price(True)
                    title = "=== Produkty posortowane po cenie malejąco ==="
                elif choice == 3:
                    output = catalog.only_active()
                    title = "=== Produkty dostępne ==="
                elif choice == 4:
                    output = catalog.only_inactive()
                    title = "=== Produkty niedostępne ==="
                print(f"\n{title}")
                display_items(output)

                input("\nNaciśnij enter aby wrócić do menu")
```

**Uzasadnienie wyboru:**
Powyższy fragment kodu jest przeróbką wcześniej istniejącego (sprzed przejścia na model OOP) kodu odpowiedzialnego za wyświetlanie zabiegów w sposób uporządkowany. Wciąż wykorzystywane jest wprowadzanie wyboru sortowania przez użytkownika i tytuły tabeli od niego zależne, natomiast sama tabela - w przeciwieństwie nawet do poprzedniej wersji - wyświetlana jest przez funkcję display_items(), która przyjmuje tablicę przekazaną przez metodę klasy TreatmentCatalog.

---

## 4. Scenariusze Weryfikacji i Wyniki Testów
*(Dowód działania programu w konsoli. Należy przedstawić przynajmniej dwa scenariusze).*

### Scenariusz A: Ścieżka poprawna (Happy Path)
* **Dane wejściowe:** Wybrano opcję 2, wprowadzono nazwę "Przeszczep skóry", wybrano kategorię 3, wprowadzono cenę 4499.99, wprowadzono czas trwania 90, określono dostępność 1, naciśnięto Enter i wybrano opcję 0 (zakończ program)
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
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-5]: 2

Dodaj nowy zabieg

Wprowadź nazwę: Przeszczep skóry

0 - Brak kategorii
1 - Konsultacje
2 - Profilaktyka
3 - Chirurgia

Wybierz kategorię spośród powyższych: 3
Wprowadź cenę (maks. dla wybranej kategorii: 8000): 4499.99
Wprowadź czas trwania zabiegu (minuty): 90
Określ dostępność (1 - Tak, 2 - Nie): 1

Pomyślnie dodano nowy zabieg.
Naciśnij Enter, aby kontynuować.

========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-5]: 0
Zamykanie programu. Do widzenia!

Process finished with exit code 0
```

### Scenariusz B: Obsługa błędów i wartości brzegowych
* **Dane wejściowe (błędne):** Wybrano opcję 2, wprowadzono nazwę "blad", wybrano kategorię -1 (nieistniejącą), wybrano kategorię 1, wprowadzono cenę 301 (powyżej maksimum), wprowadzono cenę 300, wprowadzono czas trwania 0 (poniżej minimum), wprowadzono czas trwania 10000 (powyżej maksimum), wprowadzono czas trwania 1, określono dostępność 1 (dostępne), naciśnięto Enter i wybrano opcję 0 (zakończ program)
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
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-5]: 2

Dodaj nowy zabieg

Wprowadź nazwę: blad

0 - Brak kategorii
1 - Konsultacje
2 - Profilaktyka
3 - Chirurgia

Wybierz kategorię spośród powyższych: -1
Błąd: Wartość < 0

Wybierz kategorię spośród powyższych: 1
Wprowadź cenę (maks. dla wybranej kategorii: 300): 301
Błąd: Wartość> 300
Wprowadź cenę (maks. dla wybranej kategorii: 300): 300
Wprowadź czas trwania zabiegu (minuty): 0
Błąd: Wartość < 1
Wprowadź czas trwania zabiegu (minuty): 10000
Błąd: Wartość > 600
Wprowadź czas trwania zabiegu (minuty): 1
Określ dostępność (1 - Tak, 2 - Nie): 1

Pomyślnie dodano nowy zabieg.
Naciśnij Enter, aby kontynuować.

========================================
   System zarządzania Kliniki PetCare
========================================
1. Wyświetl ofertę zabiegów
2. Dodaj nowy zabieg do oferty
3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
4. Zaktualizuj ceny
5. Eksportuj ofertę zabiegów do CSV
0. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [0-5]: 0
Zamykanie programu. Do widzenia!

Process finished with exit code 0
```

---

## 5. Podział Pracy w Zespole
*(Precyzyjne i uczciwe rozliczenie wkładu obu członków zespołu – weryfikowane z historią commitów `git log`).*
* **Wiktor Paszyński:**
  * Odpowiedzialność za moduły: `main.py`, `models.py`, `services.py`
  * Zaimplementowane funkcjonalności: Pełna integracja modelu OOP (klasowego) z menu CLI - dostosowanie wymaganych funkcji z innych modułów.
  * Liczba wykonanych commitów: 5
* **Michał Nowak:**
  * Odpowiedzialność za moduły: `main.py`, `models.py`, `test_models.py`
  * Zaimplementowane funkcjonalności: Główna funkcjonalność modułu models oraz testy związane z tym modułem.
  * Liczba wykonanych commitów: 9
