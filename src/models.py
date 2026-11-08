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
    price_pln: float
    duration_min: float
    is_active: bool = True
    treatment_id: int = None

    category = CATEGORIES[0]
    def final_price(self):
        return self.price_pln

    def __lt__(self, other):
        if not isinstance(other, Treatment):
            return NotImplemented
        return self.price_pln < other.price_pln

    def to_dict(self):
        d= asdict(self)
        d["category"]=self.category #kategoria do json
        return d

    @classmethod
    def from_dict(cls, data):
        d=dict(data)
        category = d.pop("category",CATEGORIES[0])
        kind = TYPES.get(category)
        if kind is None:
            raise ValueError("Nieznana kategoria: " + str(category))
        return kind(**d)

class Consultation(Treatment):
    category = CATEGORIES[1]

class Prevention(Treatment):
    category = CATEGORIES[2]

    def final_price(self):
        return self.price_pln * 0.9 #rabat :)

class Surgery(Treatment):
    category = CATEGORIES[3]
    add_fee = 150.0

    def final_price(self):
        return self.price_pln + self.add_fee

TYPES = {cls.category: cls for cls in (Treatment, Consultation, Prevention, Surgery)}
CLASS_BY_ID = {0: Treatment, 1: Consultation, 2: Prevention, 3: Surgery}
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
        if treatment.category not in MAX_PRICE:
            raise ValueError(f"Nieznana kategoria: {treatment.category}")

        if treatment.treatment_id is None:
            treatment.treatment_id = self.next_id
        elif self.find_by_id(treatment.treatment_id) is not None:
            raise ValueError(f"Zabieg o numerze {treatment.treatment_id} już istnieje")

        self.next_id = max(self.next_id, treatment.treatment_id + 1)
        self.treatments.append(treatment)
        return treatment

    def find_by_id(self, treatment_id):
        for t in self.treatments:
            if t.treatment_id == treatment_id:
                return t
        return None

    def sorted_by_price(self, descending=False):
        return sorted(self.treatments, reverse=descending)

    def only_active(self):
        return [t for t in self.treatments if t.is_active]

    def only_inactive(self):
        return [t for t in self.treatments if not t.is_active]

    def total_cost(self):
        return sum(t.final_price() for t in self.treatments if t.is_active)

    def __eq__(self, other):
        if not isinstance(other, TreatmentCatalog):
            return NotImplemented
        return self.name == other.name and self.treatments == other.treatments

    # --- zapis i odczyt JSON ---
    def to_dict(self):
        return {
            "name": self.name,
            "treatments": [t.to_dict() for t in self.treatments],
        }

    @classmethod
    def from_dict(cls, data):
        catalog = cls(data["name"])
        for item in data["treatments"]:
            catalog.add_treatment(Treatment.from_dict(item))
        return catalog

    def save(self, path):
        backup_menu()
        data = self.to_dict()
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,
                dir=Path(path).parent,
                prefix="vet_catalog_tmp_",
                suffix=".json",
                encoding="utf-8",
            ) as tmp:
                temp_path = Path(tmp.name)
                json.dump(data, tmp, ensure_ascii=False, indent=4)
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(temp_path, path)
        except Exception:
            if temp_path and temp_path.exists():
                temp_path.unlink()
            raise

    @classmethod
    def load(cls, path, default_name="PetCare"):
        if not os.path.exists(path):
            return cls(default_name)

        with open(path, encoding="utf-8-sig") as f:
            content = f.read().strip()
        if not content:
            return cls(default_name)

        return cls.from_dict(json.loads(content))