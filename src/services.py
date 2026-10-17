import json,csv
from json import JSONDecodeError


def display_items(items_list):
    print(f"{'ID':<4} | {'Nazwa':<25} | {'Cena':<10} | {'Dostepny':<10}")
    print("-"*57)

    for item in items_list:
        item_id = item["id"]
        item_name = item["name"]
        item_price = item["price"]
        available = "Tak" if item["available"] else "Nie"
        print(f"{item_id:<4} | {item_name:<25} | {item_price:<10.2f} | {available:<10}")

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


def update_prices(database,price_path):
    with open(database) as json_file:
        datab = json.load(json_file)
    with open(price_path) as csv_file:
        prices = {int(row["id"]): float(row["price"].replace(",",".")) for row in csv.DictReader(csv_file)}
    for product in datab:
        if product["id"] in prices:
            product["price"] = prices[product["id"]]
    with open(database, "w") as json_file:
        json.dump(datab,json_file,ensure_ascii=False,indent=2)

