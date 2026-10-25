# from data import vet_catalog # Pozostałość po zadaniu 1
from services import display_items, add_item
from storage import load_database, save_database, update_prices, csv_export
from validators import get_int_input, get_non_empty_string, get_float_input

# Obsługa pozycji menu
def handle_menu_choice(choice: int) -> bool:
    # Ładowanie bazy danych zabiegów z pliku JSON
    vet_catalog = load_database("data/vet_catalog.json")

    match choice:
        case 1:
            print("\nOferta zabiegów")
            display_items(vet_catalog)
            input("\nNaciśnij Enter, aby kontynuować.")
        case 2:
            print("\nDodaj nowy zabieg")
            name = ""
            while not get_non_empty_string(name):
                name = input("\nWprowadź nazwę: ").strip()
            price = get_float_input("Wprowadź cenę: ", 0.01)
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
            save_database("data/vet_catalog.json", vet_catalog)

            print("\nPomyślnie dodano nowy zabieg.")
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
                    output = sorted(vet_catalog, key=lambda x: x["price"])
                    title ="=== Produkty posortowane po cenie rosnąco ==="
                elif choice == 2:
                    output = sorted(vet_catalog, key=lambda x: x["price"], reverse=True)
                    title = "=== Produkty posortowane po cenie malejąco ==="
                elif choice == 3:
                    output = [p for p in vet_catalog if p["available"] == True]
                    title = "=== Produkty dostępne ==="
                elif choice == 4:
                    output = [p for p in vet_catalog if p["available"] == False]
                    title = "=== Produkty niedostępne ==="
                print(f"\n{title}")
                print(f"{'ID':<5} | {'Nazwa':<30} | {'Cena':<10} | {'Dostępny'}")
                print("-"*50)

                for p in output:
                    status = "Tak" if p["available"] else "Nie"
                    print(f"{p['id']:<5} | {p['name']:<30} | {p['price']:<10} | {status}")
                input("\nNaciśnij enter aby wrócić do menu")
        case 4:
            update_prices("data/vet_catalog.json", "data/cennik.csv")
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