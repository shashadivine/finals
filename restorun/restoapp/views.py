from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Item, inventory
from .utils import search_item, merge_sort


# Display all items
def list_items(request):
    # Change the default sort to 'sku'
    sort_by = request.GET.get('sort', 'sku')  # Default to 'sku' if no sort parameter is provided

    # Retrieve items from the inventory
    items = inventory.get_all_items()

    # Sort the items if a valid sort parameter is provided
    if sort_by in ['sku', 'name', 'cost', 'quantity', 'expiry_date', 'purchase_date', 'supplier', 'category']:
        items = merge_sort(items, sort_by)

    return render(request, 'restoapp/item_list.html', {'items': items, 'sort_by': sort_by})



# Add new item
def add_item(request):
    # Generate the next available SKU
    existing_skus = sorted(
        [int(item.sku[1:]) for item in inventory.get_all_items() if item.sku.startswith("R")]
    )
    next_sku_number = next(
        (i for i in range(1, len(existing_skus) + 2) if i not in existing_skus), 1
    )
    next_sku = f"R{next_sku_number}"  # Add the "R" prefix

    if request.method == 'POST':
        try:
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
        except Exception as e:
            # Handle errors and pass them to the form
            return render(request, 'restoapp/add_item.html', {'next_sku': next_sku, 'error': str(e)})

    # For GET requests, render the form
    return render(request, 'restoapp/add_item.html', {'next_sku': next_sku})



# Search for an item
def search_items(request):
    if request.method == 'GET':
        query = request.GET.get('query', '').strip()  # Get the search query
        attribute = request.GET.get('attribute', 'sku')  # Default to searching by 'sku'

        # If no query is provided, redirect back to the inventory list
        if not query:
            return redirect('list_items')

        # Use the updated search_item function
        matching_items = search_item(query, attribute)

        # Render the new template for search results
        return render(
            request,
            'restoapp/search_results.html',
            {
                'items': matching_items,
                'query': query,
                'attribute': attribute
            }
        )

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


