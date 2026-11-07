import json
import os
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from storage import backup_menu

CATEGORIES = {
    0: "Brak kategorii",
    1: "Konsultacje",
    2: "Profilaktyka",
    3: "Chirurgia"
}

def showCats():
    for cat in CATEGORIES:
        print(f"{cat} - {CATEGORIES[cat]}")

MAX_PRICE = {
    CATEGORIES[0]: 100000,
    CATEGORIES[1]: 300,
    CATEGORIES[2]: 500,
    CATEGORIES[3]: 8000,
}

@dataclass
class Treatment:
    name: str
    category: str
    price_pln: float
    duration_min: float
    is_active: bool = True
    treatment_id: int = None

    def __lt__(self, other):
        if not isinstance(other, Treatment):
            return NotImplemented
        return self.price_pln < other.price_pln

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class TreatmentCatalog:
    def __init__(self, name):
        self.name = name
        self.treatments = []
        self.next_id = 1       # następny wolny numer

    def to_dict(self):
        return {
            "name": self.name,
            "treatments": [t.to_dict() for t in self.treatments],
        }


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
        backup_menu()
        data = self.to_dict()
        target = path
        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            dir="data/",
            prefix="vet_catalog_tmp_",
            suffix=".json",
            encoding="utf-8"
        ) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=4)
            tmp.flush()
            os.fsync(tmp.fileno())
            temp_path = Path(tmp.name)
        os.replace(temp_path, target)

    @classmethod
    def from_dict(cls, data):
        catalog = cls(data["name"])
        for item in data["treatments"]:
            catalog.add_treatment(Treatment.from_dict(item))
        return catalog
    def __eq__(self, other):
        if not isinstance(other, TreatmentCatalog):
            return NotImplemented
        return self.name == other.name and self.treatments == other.treatments
    @classmethod
    def load(cls, path, default_name="PetCare"):
       if not os.path.exists(path):
           return cls(default_name)

       with open(path, encoding="utf-8-sig") as f:
           content = f.read().strip()
       if not content:
           return cls(default_name)