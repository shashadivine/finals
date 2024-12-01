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

def search_item(query, attribute):
    # fetch all items from the inventory
    items = inventory.get_all_items()
    # filter items based on attribute and query
    filtered_items = [
        item for item in items if str(getattr(item, attribute, '')).lower() == query.lower()
    ] # for case sensitive matches
    return filtered_items  # return all matching items

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
