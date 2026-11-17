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
from patient_repository import PatientRepository

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
        case 4: #do poprawy
            updated, errors = update_prices_report(DATA_DIR / "cennik.csv")
            print(f"\nZaktualizowano ceny dla {updated} zabiegów.")
            for error in errors:
                print(error)
            input("Naciśnij Enter, aby kontynuować.")
        case 5: #do poprawy
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
        case 0 | "q" | "exit":
            print("Zamykanie programu. Do widzenia!")
            return False # Przypisuje wartość False do zmiennej 'running', tym samym kończąc działanie pętli
        case _:
            print("Błąd: Wybierz wartość pomiędzy 0 a 8.")
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
    print("0. Wyjście z programu")
    print("-" * 40)

def main():
    # Nieskończona pętla menu CLI
    running = True
    while running:
        print_menu()
        user_choice = get_int_input("\nWprowadź swój wybór [0-8]: ", 0, 8)
        running = handle_menu_choice(user_choice)


def display_patient(patient):
    print(f"\nID: {patient['patient_id']} | Pacjent: {patient['name']}")
    print(f"Gatunek: {patient['species']} | Telefon właściciela: {patient['owner_phone']}")
    if not patient["medical_visits"]:
        print("Wizyty: brak")
        return
    print("Wizyty:")
    for visit in patient["medical_visits"]:
        status = "zakończona" if visit["is_completed"] else "niezakończona"
        print(
            f"  - {visit['visit_date']}: {visit['diagnosis']}; "
            f"{visit['cost_pln']:.2f} zł; {status}"
        )


# Zapobiega samowolnemu uruchomieniu funkcji main() przy imporcie
if __name__ == "__main__":
    main()
