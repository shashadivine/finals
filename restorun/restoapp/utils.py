from .models import inventory

def merge_sort(items, attribute):
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid], attribute)
    right = merge_sort(items[mid:], attribute)

    return merge(left, right, attribute)

def merge(left, right, attribute):
    merged = []

    while left and right:
        if getattr(left[0], attribute) <= getattr(right[0], attribute):
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))

    merged.extend(left)
    merged.extend(right)
    return merged

def search_item(attribute_value, attribute_name):
    # Fetch items from inventory, not using a db
    items = inventory.get_all_items()
    sorted_items = merge_sort(items, attribute_name)
    return binary_search(sorted_items, attribute_value, attribute_name)

def binary_search(sorted_items, value, attribute):
    low, high = 0, len(sorted_items) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_value = getattr(sorted_items[mid], attribute)

        if mid_value == value:
            return sorted_items[mid]
        elif mid_value < value:
            low = mid + 1
        else:
            high = mid - 1

    return None
