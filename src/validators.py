def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not get_non_empty_string(raw):
            print("Błąd: Puste wejście.")
            continue
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"Błąd: Wartość < {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Błąd: Wartość > {max_val}")
                continue
            return val
        except ValueError:
            print(f"Błąd: {raw} nie jest liczbą!")

def get_non_empty_string(prompt) -> bool:
    if not prompt:
        return False
    return True