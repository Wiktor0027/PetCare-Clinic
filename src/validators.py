def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        raw = input(prompt).strip()
        # Jeśli funkcja get_non_empty_string() nie zwróciła True, wejście jest puste - obecny krok pętli kończy się
        if not get_non_empty_string(raw):
            print("Błąd: Puste wejście.")
            continue
        try:
            val = int(raw)
            # Jeśli wejście liczbowe 'val' jest mniejsze od minimalnej wartości 'min_val', kończy się obecny krok pętli
            if min_val is not None and val < min_val:
                print(f"Błąd: Wartość < {min_val}")
                continue
            # Jeśli wejście liczbowe 'val' jest większe od maksymalnej wartości 'max_val', kończy się obecny krok pętli
            if max_val is not None and val > max_val:
                print(f"Błąd: Wartość > {max_val}")
                continue
            return val # Wejście liczbowe 'val' jest w porządku - przekazanie zmiennej
        except ValueError:
            # Wejście 'raw' nie jest liczbą - nie mogło zostać przekonwertowane na liczbę
            print(f"Błąd: {raw} nie jest liczbą.")

def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    while True:
        raw = input(prompt).strip()
        # Jeśli funkcja get_non_empty_string() nie zwróciła True, wejście jest puste - obecny krok pętli kończy się
        if not get_non_empty_string(raw):
            print("Błąd: Puste wejście.")
            continue
        try:
            val = float(raw)
            # Jeśli wejście liczbowe 'val' jest mniejsze od minimalnej wartości 'min_val', kończy się obecny krok pętli
            if min_val is not None and val < min_val:
                print(f"Błąd: Wartość < {min_val}")
                continue
            # Jeśli wejście liczbowe 'val' jest większe od maksymalnej wartości 'max_val', kończy się obecny krok pętli
            if max_val is not None and val > max_val:
                print(f"Błąd: Wartość> {max_val}")
                continue
            return val
        except ValueError:
            # Wejście 'raw' nie jest liczbą - nie mogło zostać przekonwertowane na liczbę
            print(f"Błąd: {raw} nie jest liczbą.")

def get_non_empty_string(prompt) -> bool:
    # Zwraca False jeśli zmienna 'prompt' jest pusta, w przeciwnym wypdaku - True
    if not prompt:
        return False
    return True