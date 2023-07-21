import os, sys, csv, json
import datetime as dt
import random

import django
from faker import Faker


try:
    path_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(path_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "tracksales.config.settings")
    django.setup()

    from tracksales.sales.models import Client, Employee, Product, ProductOrder, Order
except:
    raise ImportError("Couldn't import django models")

db_json_path = './datasets/db.json'
names_csv_path = './datasets/names.csv'
produts_csv_path = './datasets/products.csv'


def get_names(filename=names_csv_path):
    names_set = set()

    with open(filename, mode='r') as file:
        csvFile = csv.reader(file)
        is_header = True

        for line in csvFile:
            if is_header:
                is_header = False
                continue

            full_name = line[0].strip()
            names_set.add(full_name)

    return names_set


def get_products(filename=produts_csv_path):
    products_list = []
    with open(filename, mode='r') as file:
        csvFile = csv.reader(file)

        is_header = True

        for line in csvFile:
            if is_header:
                is_header = False
                continue

            name = line[0].strip()
            price = line[1].strip().lstrip('$').replace(',', '')

            try:
                price = float(price)
            except ValueError:
                input("Value error: " + price)

            product = {
                "name": name,
                "price": price
            }

            products_list.append(product)

    return products_list


def export_json(data, filename=db_json_path):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def import_json(filename=db_json_path):
    with open(filename, 'r') as f:
        data = json.load(f)
        return data


def load_from_csv():
    data = {
        "employees": [],
        "clients": [],
        "products": [],
    }

    # Names
    names_set = get_names()
    names_list = list(names_set)

    employees_names = names_list[:10]
    clients_names = names_list[10:]

    data["employees"] = employees_names
    data["clients"] = clients_names

    # Products
    products_list = get_products()
    data["products"] = products_list

    # Export
    export_json(data)


def random_birthday():
    fake = Faker()

    start_date = dt.datetime(year=1970, month=1, day=1)
    end_date = dt.datetime(year=2000, month=1, day=1)
    fake_date = fake.date_between(start_date=start_date, end_date=end_date)

    return fake_date

def random_date():
    fake = Faker()

    start_date = dt.datetime(year=2023, month=1, day=1)
    end_date = dt.datetime(year=2023, month=7, day=20)
    fake_date = fake.date_between(start_date=start_date, end_date=end_date)

    return fake_date

def random_quantity():
    return random.randint(50, 200)


def load_to_db():
    data = import_json()

    for employee_name in data["employees"]:
        birth_date = random_birthday()
        Employee.objects.get_or_create(
            full_name=employee_name,
            defaults={'birth_date': birth_date}
        )

    for client_name in data["clients"]:
        birth_date = random_birthday()
        Client.objects.get_or_create(
            full_name=client_name,
            defaults={'birth_date': birth_date}
        )

    for product in data['products']:
        quantity = random_quantity()
        Product.objects.get_or_create(
            name=product['name'],
            defaults={'price': product['price'], 'quantity': quantity}
        )

    print("Employees:", Employee.objects.count())
    print("Clients:", Client.objects.count())
    print("Products:", Product.objects.count())

def create_orders():
    number_orders = int(input("Number of orders to create: "))

    for _ in range(number_orders):
        items_count = random.randint(1, 5)

        product_orders = []

        all_products = list(Product.objects.order_by('?'))
        random_produts = all_products[:items_count]
        
        for product in random_produts:
            quantity = random.randint(1, 10)
            product_order = ProductOrder(
                product=product,
                quantity=quantity
            )
            product_orders.append(product_order)
        
        objs = ProductOrder.objects.bulk_create(product_orders)

        employee = Employee.objects.order_by("?").first()
        client = Client.objects.order_by("?").first()
        date = random_date()
        
        order = Order.objects.create(
            client=client, 
            employee=employee, 
            date=date,
        )

        order.products.set(objs)

    print("Order count:", Order.objects.count())


def main():
    print("----------------------")
    print(" 1. Load from csv")
    print(" 2. Load to database")
    print(" 3. Create random orders")
    print("----------------------")
    cmd = int(input("Enter command:"))

    match cmd:
        case 1:
            load_from_csv()
        case 2:
            load_to_db()
        case 3:
            create_orders()


if __name__ == '__main__':
    main()
