from django.db import models

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
        self.items = {}  # Use a dictionary to store items by name

    def add_item(self, item):
        if item.name in self.items:
            raise ValueError(f"Item '{item.name}' already exists in inventory.")
        self.items[item.name] = item

    def delete_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]
        else:
            raise ValueError(f"Item '{item_name}' does not exist in inventory.")

    def get_all_items(self):
        return list(self.items.values())  # Return all items as a list
    
inventory = Inventory()