# Kopia zapasowa na wypadek błędu odczytu pliku JSON - ustawienia fabryczne
vet_catalog = [
    {
        "id": 1,
        "name": "Szczepienia ochronne",
        "price": 100.00,
        "available": True,
    },
    {
        "id": 2,
        "name": "Zabiegi pielegnacyjne",
        "price": 120.00,
        "available": True,
    },
    {
        "id": 3,
        "name": "Badania laboratoryjne",
        "price": 70.00,
        "available": True,
    },
    {
        "id": 4,
        "name": "Kastracje i sterylizacja",
        "price": 92.99,
        "available": True,
    }
]#Baza w pamieci RAM: lista slownikow

active_order = {
    "order_id": 1001,
    "items": [
        {"id": 1, "qty": 3, "price":100.00}
    ],
    "is_paid": True,
    "referral_program": True,
}#model aktywnego zamowienia klienta
