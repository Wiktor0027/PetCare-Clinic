import json
from dataclasses import dataclass, asdict


MAX_PRICE = {
    "konsultacja": 300,
    "profilaktyka": 500,
    "chirurgia": 8000,
}

@dataclass
class Treatment:
    name: str
    category: str
    price_pln: float
    duration_min: float
    is_active: bool = True
    treatment_id: int = None


class TreatmentCatalog:
    def __init__(self, name):
        self.name = name
        self.treatments = []
        self.next_id = 1       # następny wolny numer

    def add_treatment(self, treatment):
        # 1. kategoria musi istnieć
        if treatment.category not in MAX_PRICE:
            raise ValueError("Nieznana kategoria: " + treatment.category)

        # 2. cena nie może przekraczać limitu kategorii
        if treatment.price_pln > MAX_PRICE[treatment.category]:
            raise ValueError("Za wysoka cena dla kategorii " + treatment.category)

        # 3. numer: nadaj automatycznie albo sprawdź ten z pliku
        if treatment.treatment_id is None:
            treatment.treatment_id = self.next_id
        else:
            for t in self.treatments:
                if t.treatment_id == treatment.treatment_id:
                    raise ValueError("Zabieg o numerze " + str(treatment.treatment_id) + " już istnieje")

        self.next_id = max(self.next_id, treatment.treatment_id + 1)

        self.treatments.append(treatment)
        return treatment       # żeby od razu znać nadany numer

    def total_cost(self):
        # suma cen aktywnych zabiegów
        total = 0.0
        for t in self.treatments:
            if t.is_active:
                total += t.price_pln
        return total

    # --- zapis i odczyt JSON ---

    def save(self, path):
        data = {
            "name": self.name,
            "treatments": [asdict(t) for t in self.treatments],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        catalog = cls(data["name"])
        for item in data["treatments"]:
            catalog.add_treatment(Treatment(**item))
        return catalog
    #poprawka