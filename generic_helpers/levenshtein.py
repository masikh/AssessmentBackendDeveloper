""" Search with levenshtein distance """
from Levenshtein import distance


def has_matching_adjacent_characters(query, field_value, threshold=3):
    """ Check if the entire query string is present in the field_value
        and the query is at least 3 characters. Return a boolean
    """
    return query.lower() in field_value.lower() and len(query) >= threshold


def search_by_levenshtein(query, model=None, field_name=None, threshold=21):
    """ Search by levenshtein word distance (case sensitivity)

        see: https://en.wikipedia.org/wiki/Levenshtein_distance for a comprehensive
        explanation what levenshtein distance is.

        This method allows you to query a string upon a given field in a given model
    """

    # Check if a model is provided
    if model is None or field_name is None:
        raise ValueError('model and field cannot be None')

    # Create an empty results list
    results = []

    # NOTE: If we provide a model that doesn't exist, we expect a 500 (internal server error)
    # handled by the generic Flask @api.errorhandler(InternalServerError) handler

    for item in model.query.all():
        # Check if the field is part of the table
        if not hasattr(item, field_name):
            raise AttributeError('No such field in table')

        # Get the value of the field from the item
        field_value = getattr(item, field_name)

        # Calculate the word distance on current item
        distance_value = distance(query.lower(), field_value.lower())

        # Augment the item with the distance_value and add to results list if and only if
        # it's within the threshold distance
        if distance_value < threshold:
            # Check if at least three adjacent character match the query before adding to the result
            if has_matching_adjacent_characters(query, field_value):
                results.append((item, distance_value))

    # Sort the list based on the second element (distance_value)
    sorted_list = sorted(results, key=lambda x: x[1])

    # Return the sorted_list of augmented results
    return sorted_list
