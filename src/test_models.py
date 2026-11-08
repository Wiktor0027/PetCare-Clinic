from models import (Treatment, Consultation, Prevention, Surgery, TreatmentCatalog, MAX_PRICE)


def make_catalog():
    c = TreatmentCatalog("PetCare")
    c.add_treatment(Consultation("Wizyta", 100.0, 30))
    c.add_treatment(Prevention("Szczepienie", 50.0, 15, False))
    c.add_treatment(Surgery("Sterylizacja", 1000.0, 90))
    return c


# 1. Poprawne instancjonowanie
def test_valid_instantiation():
    t = Consultation("Wizyta", 80.0, 15)
    assert t.name == "Wizyta"
    assert t.category == "Konsultacje"
    assert t.is_active is True
    assert t.treatment_id is None

    c = make_catalog()
    assert len(c.treatments) == 3
    assert [t.treatment_id for t in c.treatments] == [1, 2, 3]
    assert c.next_id == 4


# 2. Odrzucenie błędnych danych
def test_invalid_data_rejected():
    c = TreatmentCatalog("PetCare")

    class Bogus(Treatment):
        category = "Zmyslona"

    bad = [
        Bogus("X", 10.0, 10),                               # nieznana kategoria
        Consultation("X", MAX_PRICE["Konsultacje"] + 1, 10),  # za wysoka cena
        Consultation("X", -5.0, 10),                        # ujemna cena
        Consultation("X", 10.0, 0),                         # zerowy czas
    ]
    for t in bad:
        try:
            c.add_treatment(t)
            assert False, f"Brak ValueError dla {t}"
        except ValueError:
            pass

    c.add_treatment(Consultation("A", 10.0, 10, treatment_id=5))
    try:
        c.add_treatment(Consultation("B", 20.0, 10, treatment_id=5))
        assert False, "Brak ValueError dla duplikatu ID"
    except ValueError:
        pass

    assert len(c.treatments) == 1


# 3. Protokół porównań
def test_sorting_protocol():
    items = [Consultation("A", 300.0, 10),
             Consultation("B", 100.0, 10),
             Consultation("C", 200.0, 10)]
    items.sort()
    assert [t.price_pln for t in items] == [100.0, 200.0, 300.0]


# 4. Round-trip
def test_round_trip():
    original = make_catalog()
    restored = TreatmentCatalog.from_dict(original.to_dict())
    assert original == restored
    assert original.next_id == restored.next_id


# 5. Polimorfizm
def test_polymorphism():
    assert Consultation("W", 100.0, 30).final_price() == 100.0
    assert Prevention("S", 100.0, 15).final_price() == 90.0
    assert Surgery("O", 1000.0, 60).final_price() == 1150.0
    # aktywne: 100 + 1150 (szczepienie jest nieaktywne)
    assert make_catalog().total_cost() == 1250.0


# 6. Round-trip zachowuje podklasę
def test_round_trip_keeps_subclass():
    original = Surgery("Op", 1000.0, 60, treatment_id=1)
    restored = Treatment.from_dict(original.to_dict())
    assert type(restored) is Surgery
    assert original == restored


# 7. Metody menedżera
def test_catalog_queries():
    c = make_catalog()
    assert [t.name for t in c.only_active()] == ["Wizyta", "Sterylizacja"]
    assert [t.name for t in c.only_inactive()] == ["Szczepienie"]
    assert [t.price_pln for t in c.sorted_by_price()] == [50.0, 100.0, 1000.0]
    assert c.find_by_id(2).name == "Szczepienie"
    assert c.find_by_id(99) is None


if __name__ == "__main__":
    tests = [test_valid_instantiation, test_invalid_data_rejected,
             test_sorting_protocol, test_round_trip, test_polymorphism,
             test_round_trip_keeps_subclass, test_catalog_queries]
    for test in tests:
        test()
        print(f"OK  {test.__name__}")
    print("\nWszystkie testy przeszły.")