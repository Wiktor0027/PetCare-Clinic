from pathlib import Path
from datetime import date
import sqlite3

from services import display_items
from sqlite_storage import (
    add_treatment as save_treatment,
    csv_export,
    load_catalog,
    update_prices_report,
)
from validators import get_int_input, get_non_empty_string, get_float_input
from models import showCats, CATEGORIES, MAX_PRICE, CLASS_BY_ID
from patient_repository import PatientRepository, display_patient
from analytics import ClinicAnalytics, format_table

DATA_DIR = Path(__file__).resolve().parent / "data"
EXPORT_PATH = Path(__file__).resolve().parent / "zabiegi.csv"

# Obsługa pozycji menu
def handle_menu_choice(choice: int) -> bool:
    # Wczytaj katalog z bazy SQLite.
    catalog = load_catalog()
    match choice:
        case 1:
            print("\nOferta zabiegów")
            display_items(catalog.treatments)
            input("\nNaciśnij Enter, aby kontynuować.")
        case 2:
            print("\nDodaj nowy zabieg")
            name = ""
            while not get_non_empty_string(name):
                name = input("\nWprowadź nazwę: ").strip()
            print()
            showCats()
            category = get_int_input("\nWybierz kategorię spośród powyższych: ", 0, len(CATEGORIES) - 1)
            price = get_float_input(
                f"Wprowadź cenę (maks. dla wybranej kategorii: {MAX_PRICE[CATEGORIES[category]]}): ", 0.01,
                MAX_PRICE[CATEGORIES[category]])
            duration = get_int_input("Wprowadź czas trwania zabiegu (minuty): ", 1, 600)
            availability = get_int_input("Określ dostępność (1 - Tak, 2 - Nie): ", 1, 2) == 1

            try:
                treatment = CLASS_BY_ID[category](name, price, duration, availability)
                catalog.add_treatment(treatment)
                save_treatment(treatment)
                print("\nPomyślnie dodano nowy zabieg.")
            except ValueError as e:
                print("\nNie dodano zabiegu:", e)

            input("Naciśnij Enter, aby kontynuować.")
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
        case 4:
            updated, errors = update_prices_report(DATA_DIR / "cennik.csv")
            print(f"\nZaktualizowano ceny dla {updated} zabiegów.")
            for error in errors:
                print(error)
            input("Naciśnij Enter, aby kontynuować.")
        case 5:
            csv_export(EXPORT_PATH)
            print("\nPomyślnie wyeksportowano bazę danych zabiegów do pliku CSV.")
            input("Naciśnij Enter, aby kontynuować.")
        case 6:
            print("\nRejestracja pacjenta")
            name = input("Imię pacjenta: ").strip()
            while not get_non_empty_string(name):
                name = input("Imię pacjenta nie może być puste: ").strip()

            print("1. Pies\n2. Kot\n3. Gryzon")
            species = {1: "Pies", 2: "Kot", 3: "Gryzon"}[
                get_int_input("Wybierz gatunek [1-3]: ", 1, 3)
            ]
            owner_phone = input("Telefon właściciela: ").strip()
            while not get_non_empty_string(owner_phone):
                owner_phone = input("Telefon nie może być pusty: ").strip()

            visits = []
            if get_int_input("Dodać wizytę? (1 - Tak, 2 - Nie): ", 1, 2) == 1:
                visit_date = input("Data wizyty (RRRR-MM-DD): ").strip()
                while True:
                    try:
                        date.fromisoformat(visit_date)
                        break
                    except ValueError:
                        visit_date = input("Podaj poprawną datę RRRR-MM-DD: ").strip()
                diagnosis = input("Opis / diagnoza: ").strip()
                while not get_non_empty_string(diagnosis):
                    diagnosis = input("Opis nie może być pusty: ").strip()
                cost = get_float_input("Koszt wizyty w PLN: ", 0)
                completed = get_int_input(
                    "Czy wizyta została zakończona? (1 - Tak, 2 - Nie): ", 1, 2
                ) == 1
                visits.append({
                    "visit_date": visit_date,
                    "diagnosis": diagnosis,
                    "cost_pln": cost,
                    "is_completed": completed,
                })

            patient = {
                "name": name,
                "species": species,
                "owner_phone": owner_phone,
                "medical_visits": visits,
            }
            try:
                patient_id = PatientRepository().save_patient(patient)
                print(f"\nDodano pacjenta. Jego ID to: {patient_id}")
            except (KeyError, ValueError, sqlite3.Error) as error:
                print(f"\nNie udało się dodać pacjenta: {error}")
            input("Naciśnij Enter, aby kontynuować.")
        case 7:
            patient_id = get_int_input("Podaj ID pacjenta: ", 1)
            patient = PatientRepository().get_patient(patient_id)
            if patient is None:
                print("\nNie znaleziono pacjenta o takim ID.")
            else:
                display_patient(patient)
            input("Naciśnij Enter, aby kontynuować.")
        case 8:
            patients = PatientRepository().list_patients()
            if not patients:
                print("\nBrak zapisanych pacjentów.")
            for patient in patients:
                display_patient(patient)
            input("Naciśnij Enter, aby kontynuować.")
        case 9:
            print("\nRaport pacjentów (wizyty i koszty)")
            rows = ClinicAnalytics().patient_report()
            format_table(rows, [
                ("patient_id", "ID", 4), ("name", "Pacjent", 18),
                ("species", "Gatunek", 8), ("visits", "Wizyty", 7),
                ("total_cost", "Suma PLN", 10), ("avg_cost", "Śr. PLN", 10),
            ], "Brak zapisanych pacjentów.")
            input("\nNaciśnij Enter, aby kontynuować.")
        case 10:
            print("\nRaport według gatunków")
            date_from = input("Od daty (RRRR-MM-DD, Enter = bez ograniczenia): ").strip() or None
            date_to = input("Do daty (RRRR-MM-DD, Enter = bez ograniczenia): ").strip() or None
            try:
                for value in (date_from, date_to):
                    if value:
                        date.fromisoformat(value)
                rows = ClinicAnalytics().species_report(date_from, date_to)
                format_table(rows, [
                    ("species", "Gatunek", 8), ("patients", "Pacjenci", 9),
                    ("visits", "Wizyty", 7), ("total_cost", "Suma PLN", 10),
                    ("avg_cost", "Śr. PLN", 10),
                ])
            except ValueError:
                print("\nNiepoprawny format daty.")
            input("\nNaciśnij Enter, aby kontynuować.")
        case 11:
            year = get_int_input("Podaj rok: ", 1900, 2100)
            print(f"\nPrzychód miesięczny z zakończonych wizyt w {year} r.:")
            rows = ClinicAnalytics().monthly_revenue(year)
            format_table(rows, [
                ("month", "Miesiąc", 8), ("visits", "Wizyty", 7),
                ("revenue", "Przychód PLN", 13), ("avg_cost", "Śr. PLN", 10),
            ], "Brak zakończonych wizyt w tym roku.")
            input("\nNaciśnij Enter, aby kontynuować.")
        case 12:
            limit = get_int_input("Ilu pacjentów pokazać? [1-50]: ", 1, 50)
            print(f"\nTop {limit} pacjentów według łącznych kosztów")
            rows = ClinicAnalytics().top_patients(limit)
            format_table(rows, [
                ("patient_id", "ID", 4), ("name", "Pacjent", 18),
                ("species", "Gatunek", 8), ("visits", "Wizyty", 7),
                ("total_cost", "Suma PLN", 10),
            ], "Brak wizyt w bazie.")
            input("\nNaciśnij Enter, aby kontynuować.")
        case 13:
            print("\nStatystyki katalogu zabiegów wg kategorii")
            rows = ClinicAnalytics().treatment_category_report()
            format_table(rows, [
                ("category", "Kategoria", 16), ("treatments", "Zabiegi", 8),
                ("active", "Aktywne", 8), ("total_price", "Suma cen", 10),
                ("avg_price", "Śr. cena", 10), ("avg_duration", "Śr. czas", 9),
            ])
            input("\nNaciśnij Enter, aby kontynuować.")
        case 0 | "q" | "exit":
            print("Zamykanie programu. Do widzenia!")
            return False # Przypisuje wartość False do zmiennej 'running', tym samym kończąc działanie pętli
        case _:
            print("Błąd: Wybierz wartość pomiędzy 0 a 13.")
    return True # Przypisuje wartość True do zmiennej 'running', kontynuując działanie pętli

# Wyświetlenie menu
def print_menu():
    print("\n" + "=" * 40)
    print("   System zarządzania Kliniki PetCare")
    print("=" * 40)
    print("1. Wyświetl ofertę zabiegów")
    print("2. Dodaj nowy zabieg do oferty")
    print("3. Wyświetl ofertę zabiegów - sortowanie wg kryteriów")
    print("4. Zaktualizuj ceny")
    print("5. Eksportuj ofertę zabiegów do CSV")
    print("6. Dodaj pacjenta")
    print("7. Odczytaj pacjenta po ID")
    print("8. Wyświetl wszystkich pacjentów")
    print("9. Raport pacjentów (wizyty i koszty)")
    print("10. Raport według gatunków")
    print("11. Przychód miesięczny")
    print("12. Top pacjenci według kosztów")
    print("13. Statystyki katalogu zabiegów")
    print("0. Wyjście z programu")
    print("-" * 40)

def main():
    # Nieskończona pętla menu CLI
    running = True
    while running:
        print_menu()
        user_choice = get_int_input("\nWprowadź swój wybór [0-13]: ", 0, 13)
        running = handle_menu_choice(user_choice)


# Zapobiega samowolnemu uruchomieniu funkcji main() przy imporcie
if __name__ == "__main__":
    main()
