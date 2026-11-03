from typing import Self, Any


class Treatment:
    def __init__(self, name: str, price: float):
        self.name: str = name
        self.price: float = price

    def __repr__(self) -> str:
        return f"Treatment(name={self.name}, price={self.price})"

    def __str__(self) -> str:
        return f"{self.name:<18} {self.price:>6.2f} PLN]"

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Nazwa musi być ciągiem znaków.")
        self._name = value

    @price.setter
    def price(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Cena musi być wartością liczbową.")
        if value <= 0.0:
            raise ValueError(f"Cena musi być większa od 0. Podano {value}.")
        self._price = round(float(value), 2)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Treatment):
            return False
        return self.treatment_id == other.treatment_id

    def __lt__(self, other: "Treatment") -> bool:
        if not isinstance(other, Treatment):
            return NotImplemented
        return (self.price, self.name) < (other.price, other.name)

class Catalogs:
    def __init__(self, name: str, treatments: list[Treatment]) -> None:
        self.name = name
        self.treatments: list[Treatment] = treatments if treatments is not None else []

    @property
    def treatments(self) -> list[Treatment]:
        return list(self._treatments)

    def add_treatment(self, treatment: Treatment) -> None:
        if not isinstance(treatment, Treatment):
            raise TypeError("W katalogu można umieszczać wyłącznie instancje klasy Treatment.")
        self._treatments.append(treatment)

    def total_price(self, discount_percent: float = 0.0) -> float:
        if not (0.0 <= discount_percent <= 100.0):
            raise ValueError("Rabat musi mieścić się w przedziale <0; 100>.")
        raw_sum = sum(item.price for item in self._treatments)
        discount_multiplier = (100.0 - discount_percent) / 100.0
        return round(raw_sum * discount_multiplier, 2)

    def __str__(self) -> str:
        lines = [f"===== KATALOG {self.name} ====="]
        lines.extend(f"  * {item}" for item in self._treatments)
        lines.append(f"  SUMA DO ZAPŁATY ZA CAŁY KATALOG: {self.total_price():.2f} PLN")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "treatments": [item.to_dict() for item in self.treatments],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        restored_items = [Treatment.from_dict(raw) for raw in data.get("treatments", [])]
        return cls(int(data["name"]), restored_items)
