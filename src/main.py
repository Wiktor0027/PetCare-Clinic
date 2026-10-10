from validators import get_int_input


def handle_menu_choice(choice: int) -> bool:
    match choice:
        case 1:
            print("1. Teleporada")
        case 2:
            print("2. Umów się na wizytę")
        case 3:
            print("3. Umówione wizyty")
        case 4 | "q" | "exit":
            print("Zamykanie programu. Do widzenia!")
            return False
        case _:
            print("Błąd: Niewłaściwy wybór. Wybierz wartość pomiędzy 1 a 4.")
    return True

def print_menu():
    print("\n" + "=" * 40)
    print("   System zarządzania Kliniki PetCare")
    print("=" * 40)
    print("1. Teleporada")
    print("2. Umów się na wizytę")
    print("3. Umówione wizyty")
    print("4. Wyjście z programu")
    print("-" * 40)

def main():
    running = True
    while running:
        print_menu()
        user_choice = get_int_input("Wprowadź swój wybór [1-4]: ", 1, 4)
        running = handle_menu_choice(user_choice)


if __name__ == "__main__":
    main()