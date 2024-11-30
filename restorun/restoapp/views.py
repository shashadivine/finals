from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Item, inventory
from .utils import search_item

# Display all items
def list_items(request):
    items = inventory.get_all_items()  # Retrieve items from Inventory
    return render(request, 'restoapp/item_list.html', {'items': items})

# Add new item
def add_item(request):
    # Generate the next SKU with "R" prefix
    existing_skus = [item.sku for item in inventory.get_all_items()]
    next_sku_number = len(existing_skus) + 1  # Incremental number
    next_sku = f"R{next_sku_number}"  # Add the "R" prefix

    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        sku = request.POST.get('sku')  # Use the pre-filled SKU from the form
        cost = float(request.POST.get('cost'))
        quantity = int(request.POST.get('quantity'))
        expiry_date = datetime.strptime(request.POST.get('expiry_date'), '%Y-%m-%d').date()
        purchase_date = datetime.strptime(request.POST.get('purchase_date'), '%Y-%m-%d').date()
        supplier = request.POST.get('supplier')
        category = request.POST.get('category')

        # Check if a custom category was entered
        new_category = request.POST.get('new_category')
        if category == 'Other' and new_category:
            category = new_category

        # Create a new item and add it to the inventory
        new_item = Item(
            sku=sku,
            name=name,
            cost=cost,
            quantity=quantity,
            expiry_date=expiry_date,
            purchase_date=purchase_date,
            supplier=supplier,
            category=category
        )
        inventory.add_item(new_item)

        # Redirect to the item list page
        return redirect('list_items')

    return render(request, 'restoapp/add_item.html', {'next_sku': next_sku})
# Delete an item
def delete_item(request, sku):
    try:
        # Iterate through the inventory to find the item with the given SKU
        for item_name, item in inventory.items.items():
            if item.sku == sku:
                inventory.delete_item(item_name)
                break
        else:
            raise ValueError(f"Item with SKU {sku} not found.")
    except ValueError as e:
        return render(request, 'restoapp/item_list.html', {'error': str(e)})
    return redirect('list_items')


# Search for an item
def search_items(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        attribute = request.GET.get('attribute')  # e.g., 'sku', 'name'
        item = search_item(query, attribute)
        return render(request, 'restoapp/search_results.html', {'item': item})
    return render(request, 'restoapp/search.html')
