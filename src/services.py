def display_items(items_list):
    print(f"{'ID':<4} | {'Nazwa':<25} | {'Kategoria':<20} | {'Cena':<10} | {'Czas trwania':<14} | {'Dostepny':<10}")
    print("-"*98)

    for item in items_list:
        item_id = item.treatment_id
        item_name = item.name
        item_price = item.price_pln
        item_cat = item.category
        item_duration = item.duration_min
        available = "Tak" if item.is_active else "Nie"
        print(f"{item_id:<4} | {item_name:<25} | {item_cat:<20} | {item_price:<10.2f} | {item_duration:<14} | {available:<10}")

def add_item(items_list, new_items_data):
    if items_list :
        max_id=max(item["id"] for item in items_list) #szukamy najwiekszego id
        new_id = max_id+1
    else:
        new_id = 1
    new_record = {"id": new_id, **new_items_data}#tworzy nowzy slownik i laczy wygenerowane id oraz nowe dane
    items_list.append(new_record)
    print(f"Dodano pomyslnie (ID: {new_id}): {new_record}")
    return new_record