from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .utils import search_item

# Display all items
def list_items(request):
    items = Item.objects.all().order_by('expiry_date')
    return render(request, 'restoapp/item_list.html', {'items': items})

# Add new item
def add_item(request):
    if request.method == 'POST':
        data = request.POST
        item = Item(
            sku=data['sku'],
            name=data['name'],
            cost=data['cost'],
            quantity=data['quantity'],
            expiry_date=data['expiry_date'],
            purchase_date=data['purchase_date'],
            supplier=data['supplier'],
            category=data['category']
        )
        item.save()
        return redirect('list_items')
    return render(request, 'restoapp/add_item.html')

# Delete an item
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('list_items')

# Search for an item
def search_items(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        attribute = request.GET.get('attribute')  # e.g., 'sku', 'name'
        item = search_item(query, attribute)
        return render(request, 'restoapp/search_results.html', {'item': item})
    return render(request, 'restoapp/search.html')
