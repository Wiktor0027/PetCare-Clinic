# Sprawozdanie z Zadania Laboratoryjnego nr 2
**Przedmiot:** Programowanie w języku Python (`IwIK-S1`)  
**Projekt:** PetCare Clinic
**Zespół (Autorzy):**  
1. Wiktor Paszyński (nr albumu: 164865) – login Git: `[LOGIN]`
2. Michał Nowak (nr albumu: 164855) – login Git: `[LOGIN]`  
**Data oddania:** 13.10.2026

---

## 1. Cel i Zakres Inżynierski Zadania
*Stworzenie programu zarządzania Kliniką PetCare. Zawiera funkcjonalność wyświetlania - w tym z sortowaniem - i dodawania zabiegów. Użyto instrukcji `match-case`.

---

## 2. Architektura Rozwiązania i Struktura Modułów
*(Wykaz zrealizowanych plików w katalogu `src/` wraz z przypisaniem ich odpowiedzialności).*
* `src/data.py` – Przechowuje dane o zabiegach
* `src/validators.py` – Przechowuje walidatory wprowadzanych danych
* `src/services.py` – Zawiera funkcje dodawania i wyświetlania list
* `src/main.py` – Odpowiada za implementację innych modułów oraz menu CLI

---

## 3. Kluczowy Fragment Kodu i Uzasadnienie Inżynierskie
*(Wybrany, najważniejszy lub najciekawszy fragment kodu źródłowego zrealizowany w tym etapie – maksymalnie 15–25 linii).*

```python
print("\nDodaj nowy zabieg")
name = ""
while not get_non_empty_string(name):
    name = input("\nWprowadź nazwę: ").strip()
price = get_int_input("Wprowadź cenę: ", 0)
availability = get_int_input("Określ dostępność (1 - Tak, 2 - Nie): ", 1, 2)
if (availability == 1):
    availability = True
else:
    availability = False

new_item_data = {
    "name": name,
    "price": price,
    "available": availability
}

add_item(vet_catalog, new_item_data)
print("\nPomyślnie dodano nowy zabieg.")
input("Naciśnij Enter, aby kontynuować.")
```

**Uzasadnienie wyboru:**  
Przedstawiony fragment kodu wykorzystuje wszystkie dostępne walidatory - `get_int_input` (użyty 2 razy) oraz `get_non_empty_string` (użyty raz). Wykorzystanie `get_non_empty_string` samodzielnie jest o tyle ciekawe, że został on oryginalnie stworzony do użytku w drugim walidatorze.

---

## 4. Scenariusze Weryfikacji i Wyniki Testów
*(Dowód działania programu w konsoli. Należy przedstawić przynajmniej dwa scenariusze).*

### Scenariusz A: Ścieżka poprawna (Happy Path)
* **Dane wejściowe:** Wprowadzono "5" po uruchomieniu programu, następnie "Przegląd zębów", dalej "20", naciśnięto Enter po wyświetleniu odpowiedniego komunikatu w konsoli, zakończono wprowadzając 7
* **Oczekiwany i uzyskany wynik:**
```text
========================================
   System zarządzania Kliniki PetCare
========================================
1. Teleporada
2. Umów się na wizytę
3. Umówione wizyty
4. Wyświetl ofertę zabiegów
5. Dodaj nowy zabieg do oferty
6. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
7. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [1-7]: 5

Dodaj nowy zabieg

Wprowadź nazwę: Przegląd zębów
Wprowadź cenę: 20
Określ dostępność (1 - Tak, 2 - Nie): 1
Dodano pomyslnie (ID: 5): {'id': 5, 'name': 'Przegląd zębów', 'price': 20, 'available': True}

Pomyślnie dodano nowy zabieg.
Naciśnij Enter, aby kontynuować.

========================================
   System zarządzania Kliniki PetCare
========================================
1. Teleporada
2. Umów się na wizytę
3. Umówione wizyty
4. Wyświetl ofertę zabiegów
5. Dodaj nowy zabieg do oferty
6. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
7. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [1-7]: 7
Zamykanie programu. Do widzenia!

Process finished with exit code 0
```

### Scenariusz B: Obsługa błędów i wartości brzegowych
* **Dane wejściowe (błędne):** Wprowadzono wartość 0 po uruchomieniu programu, następnie 8 oraz 100 (wszystkie błędne); zakończono program wartością 7 (prawidłową)
* **Reakcja programu:**
```text
========================================
   System zarządzania Kliniki PetCare
========================================
1. Teleporada
2. Umów się na wizytę
3. Umówione wizyty
4. Wyświetl ofertę zabiegów
5. Dodaj nowy zabieg do oferty
6. Wyświetl ofertę zabiegów - sortowanie wg kryteriów
7. Wyjście z programu
----------------------------------------

Wprowadź swój wybór [1-7]: 0
Błąd: Wartość < 1

Wprowadź swój wybór [1-7]: 8
Błąd: Wartość > 7

Wprowadź swój wybór [1-7]: 100
Błąd: Wartość > 7

Wprowadź swój wybór [1-7]: 7
Zamykanie programu. Do widzenia!

Process finished with exit code 0
```

---

## 5. Podział Pracy w Zespole
*(Precyzyjne i uczciwe rozliczenie wkładu obu członków zespołu – weryfikowane z historią commitów `git log`).*
* **Wiktor Paszyński:**
  * Odpowiedzialność za moduły: `src/validators.py`, `src/main.py`
  * Zaimplementowane funkcjonalności: Funkcje `get_int_input` oraz `get_non_empty_string`. Główny szkielet i podstawowe działanie menu CLI, oraz implementacja opcji dodawania poprzez to menu.
  * Liczba wykonanych commitów: 5
* **Michał Nowak:**
  * Odpowiedzialność za moduły: `src/data.py`, `src/services.py`, `src/main.py`
  * Zaimplementowane funkcjonalności: Stworzenie tabeli zabiegów oraz wizyt. Funkcje `display_items` i `add_item`. Implementacja wyświetlania z sortowaniem w menu CLI.
  * Liczba wykonanych commitów: 5
