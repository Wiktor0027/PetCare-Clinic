from models import Treatment, TreatmentCatalog, MAX_PRICE

CAT = next(iter(MAX_PRICE))          # dowolna poprawna kategoria
LIMIT = MAX_PRICE[CAT]


def make_catalog():
    catalog = TreatmentCatalog("PetCare")
    catalog.add_treatment(Treatment("Konsultacja", CAT, 100.0, 30))
    catalog.add_treatment(Treatment("Szczepienie", CAT, 50.0, 15, False))
    catalog.add_treatment(Treatment("Kontrola", CAT, 75.0, 20))
    return catalog


# 1. Poprawne instancjonowanie
def test_valid_instantiation():
    t = Treatment("Szczepienie", CAT, 80.0, 15)
    assert t.name == "Szczepienie"
    assert t.category == CAT
    assert t.price_pln == 80.0
    assert t.duration_min == 15
    assert t.is_active is True
    assert t.treatment_id is None

    catalog = make_catalog()
    assert catalog.name == "PetCare"
    assert len(catalog.treatments) == 3
    # ID nadane automatycznie, unikalne i kolejne
    assert [t.treatment_id for t in catalog.treatments] == [1, 2, 3]
    assert catalog.next_id == 4
    # suma tylko aktywnych (100 + 75)
    assert catalog.total_cost() == 175.0


# 2. Odrzucenie błędnych danych (niezmienniki)
def test_invalid_data_rejected():
    catalog = TreatmentCatalog("PetCare")

    # nieznana kategoria
    try:
        catalog.add_treatment(Treatment("X", "nieistniejaca", 10.0, 10))
        assert False, "Brak ValueError dla nieznanej kategorii"
    except ValueError:
        pass

    # cena powyżej limitu kategorii
    try:
        catalog.add_treatment(Treatment("X", CAT, LIMIT + 1, 10))
        assert False, "Brak ValueError dla zbyt wysokiej ceny"
    except ValueError:
        pass

    # zduplikowany numer
    catalog.add_treatment(Treatment("A", CAT, 10.0, 10, treatment_id=5))
    try:
        catalog.add_treatment(Treatment("B", CAT, 20.0, 10, treatment_id=5))
        assert False, "Brak ValueError dla duplikatu ID"
    except ValueError:
        pass

    # nieudane dodania nie mogą zostawić śladu w katalogu
    assert len(catalog.treatments) == 1


# 3. Protokół porównań (__lt__)
def test_sorting_protocol():
    a = Treatment("A", CAT, 300.0, 10)
    b = Treatment("B", CAT, 100.0, 10)
    c = Treatment("C", CAT, 200.0, 10)
    items = [a, b, c]
    items.sort()
    assert [t.price_pln for t in items] == [100.0, 200.0, 300.0]


# 4. Round-trip serialization
def test_round_trip():
    original = make_catalog()
    restored = TreatmentCatalog.from_dict(original.to_dict())

    assert original == restored
    # dodatkowa kontrola, gdyby __eq__ w katalogu był niepełny
    assert original.name == restored.name
    assert original.next_id == restored.next_id
    assert original.treatments == restored.treatments


if __name__ == "__main__":
    tests = [
        test_valid_instantiation,
        test_invalid_data_rejected,
        test_sorting_protocol,
        test_round_trip,
    ]
    for test in tests:
        test()
        print(f"OK  {test.__name__}")
    print("\nWszystkie testy przeszły.")