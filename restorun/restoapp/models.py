from django.db import models
import json

class Item:
    def __init__(self, sku, name, cost, quantity, expiry_date, purchase_date, supplier, category):
        self.sku = sku
        self.name = name
        self.cost = cost
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.purchase_date = purchase_date
        self.supplier = supplier
        self.category = category

class Inventory:
    def __init__(self):
        self.items = {}  # Dictionary to store items by name
        self.load_items()  # Load saved items on initialization

    def add_item(self, item):
        if item.name in self.items:
            raise ValueError(f"Item '{item.name}' already exists in inventory.")
        self.items[item.name] = item
        self.save_items()

    def delete_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]
            self.save_items()
        else:
            raise ValueError(f"Item '{item_name}' does not exist in inventory.")

    def get_all_items(self):
        return list(self.items.values())

    def save_items(self):
        import json
        with open('inventory.json', 'w') as f:
            json.dump(
                {name: vars(item) for name, item in self.items.items()}, f, default=str
            )

    def load_items(self):
        import json
        from .models import Item
        try:
            with open('inventory.json', 'r') as f:
                data = json.load(f)
                for item_data in data.values():
                    self.items[item_data['name']] = Item(**item_data)
        except FileNotFoundError:
            self.items = {}

# Instantiate a global `inventory` object
inventory = Inventory()
