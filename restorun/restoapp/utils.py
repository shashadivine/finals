from .models import inventory
from datetime import datetime

def merge_sort(items, attribute):
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid], attribute)
    right = merge_sort(items[mid:], attribute)

    return merge(left, right, attribute)

def merge(left, right, attribute):
    print(f"Sorting by {attribute}:")
    print(f"Left: {[getattr(item, attribute) for item in left]}")
    print(f"Right: {[getattr(item, attribute) for item in right]}")
    merged = []

    while left and right:
        # Handle date comparisons
        left_value = getattr(left[0], attribute)
        right_value = getattr(right[0], attribute)

        # Convert strings to dates if necessary
        if isinstance(left_value, str) and attribute in ['expiry_date', 'purchase_date']:
            left_value = datetime.strptime(left_value, '%Y-%m-%d').date()
        if isinstance(right_value, str) and attribute in ['expiry_date', 'purchase_date']:
            right_value = datetime.strptime(right_value, '%Y-%m-%d').date()

        if left_value <= right_value:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))

    merged.extend(left)
    merged.extend(right)
    return merged


def search_item(query, attribute):
    # Fetch all items from the inventory
    items = inventory.get_all_items()
    # Filter items based on the attribute and query
    filtered_items = [
        item for item in items if str(getattr(item, attribute, '')).lower() == query.lower()
    ]
    return filtered_items  # Return all matching items


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
