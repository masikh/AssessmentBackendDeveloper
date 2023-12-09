""" Simple generic helper to check if a given value is defined in an Enum class """


def is_valid_enum(value, enum_class):
    """ Check if the value is indeed a value from a item in the enum_class """

    # Check all statuses in the enum_class
    for status in enum_class:
        # Check if we find a match
        if value.lower() == status.value.lower():
            return True
    # All statuses are exhausted, return False
    return False
