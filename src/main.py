from data import vet_catalog
from services import display_items, add_item
from validators import get_int_input, get_non_empty_string


# Obsługa pozycji menu
def handle_menu_choice(choice: int) -> bool:
    match choice:
        case 1:
            print("1. Teleporada")
        case 2:
            print("2. Umów się na wizytę")
        case 3:
            print("3. Umówione wizyty")
        case 4:
            print("\nOferta zabiegów")
            display_items(vet_catalog)
        case 5:
            print("\nDodaj nowy zabieg")
            name = ""
            while not get_non_empty_string(name):
                name = input("\nWprowadź nazwę: ")
            price = get_int_input("\nWprowadź cenę: ", 0)
            availability = get_int_input("\nOkreśl dostępność (1 - Tak, 2 - Nie): ", 1, 2)
            if (availability == 1):
                availability = True
            else:
                availability = False

            new_item_data = [
                {
                    "name": name,
                    "price": price,
                    "available": availability
                }
            ]

            add_item(vet_catalog, new_item_data)
            print("\nPomyślnie dodano nowy zabieg.")
        case 6:
            print("6. Wyświetl ofertę zabiegów - sortowanie wg kryteriów")
        case 7 | "q" | "exit":
            print("Zamykanie programu. Do widzenia!")
            return False # Przypisuje wartość False do zmiennej 'running', tym samym kończąc działanie pętli
        case _:
            print("Błąd: Niewłaściwy wybór. Wybierz wartość pomiędzy 1 a 4.")
    return True # Przypisuje wartość True do zmiennej 'running', kontynuując działanie pętli

# Wyświetlenie menu
def print_menu():
    print("\n" + "=" * 40)
    print("   System zarządzania Kliniki PetCare")
    print("=" * 40)
    print("1. Teleporada")
    print("2. Umów się na wizytę")
    print("3. Umówione wizyty")
    print("4. Wyświetl ofertę zabiegów")
    print("5. Dodaj nowy zabieg do oferty")
    print("6. Wyświetl ofertę zabiegów - sortowanie wg kryteriów")
    print("7. Wyjście z programu")
    print("-" * 40)

def main():
    # Nieskończona pętla menu CLI
    running = True
    while running:
        print_menu()
        user_choice = get_int_input("\nWprowadź swój wybór [1-7]: ", 1, 7)
        running = handle_menu_choice(user_choice)


# Zapobiega samowolnemu uruchomieniu funkcji main() przy imporcie
if __name__ == "__main__":
    main()