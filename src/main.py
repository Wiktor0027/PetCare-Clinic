from services import display_items
from storage import update_prices_report, csv_export
from validators import get_int_input, get_non_empty_string, get_float_input
from models import TreatmentCatalog, showCats, CATEGORIES, MAX_PRICE, CLASS_BY_ID


# Obsługa pozycji menu
def handle_menu_choice(choice: int) -> bool:
    # Ładowanie bazy danych zabiegów z pliku JSON
    PATH = "data/vet_catalog.json"
    catalog = TreatmentCatalog.load(PATH)
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
                catalog.save(PATH)
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
            update_prices_report("data/vet_catalog.json", "data/cennik.csv")
            print("\nZaktualizowano ceny z pliku.")
            input("Naciśnij Enter, aby kontynuować.")
        case 5:
            csv_export("zabiegi")
            print("\nPomyślnie wyeksportowano bazę danych zabiegów do pliku CSV.")
            input("Naciśnij Enter, aby kontynuować.")
        case 0 | "q" | "exit":
            print("Zamykanie programu. Do widzenia!")
            return False # Przypisuje wartość False do zmiennej 'running', tym samym kończąc działanie pętli
        case _:
            print("Błąd: Niewłaściwy wybór. Wybierz wartość pomiędzy 1 a 5.")
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
    print("0. Wyjście z programu")
    print("-" * 40)

def main():
    # Nieskończona pętla menu CLI
    running = True
    while running:
        print_menu()
        user_choice = get_int_input("\nWprowadź swój wybór [0-5]: ", 0, 5)
        running = handle_menu_choice(user_choice)


# Zapobiega samowolnemu uruchomieniu funkcji main() przy imporcie
if __name__ == "__main__":
    main()