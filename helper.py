import time

def get_item_by_id(list, id_to_match):
    """return the instance with the given id"""
    for item in list:
        if item.id == id_to_match:
            return item
    return False

def get_items_by_value(list, attr_to_match, value_to_match):
    """return the instances where the given attribute
    matches the value provided"""
    return [item for item in list if getattr(item, attr_to_match) == value_to_match]

def get_items_by_date(list, attr_to_match, start_date="todo", end_date="todo"):
    """return a list of instances where the given date attribute
    sits in the date range given
    default to 'a long time ago' for the start date
    default to 'now' for the end date"""
    # TODO finish this function by adding propoer date handling
    return [item for item in list if start_date <= getattr(item, attr_to_match) <= end_date]
