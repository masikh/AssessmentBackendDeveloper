""" Search with levenshtein distance """
from Levenshtein import distance


def search_by_levenshtein(query, model=None, field=None, threshold=3):
    """ Search by word distance

        see: https://en.wikipedia.org/wiki/Levenshtein_distance for a comprehensive
        explanation what levenshtein distance is.

        This method allows you to query a string upon a given table in a given model
    """

    # Check if a model is provided
    if model is None or field is None:
        raise ValueError('model and field cannot be None')

    # Create an empty results list
    results = []

    # If we provide a model that doesn't exist, we expect a 500 (internal server error)
    # handled by the generic Flask @api.errorhandler(InternalServerError) handler

    for item in model.query.all():
        # Check if the field is part of the table
        if field not in item:
            raise KeyError('No such field in table')

        # Calculate the word distance on current item
        distance_value = distance(query, item[field])

        # It the distance is within the ballpark, add the item to the results
        if distance_value <= threshold:
            results.append((item, distance_value))  # Augment the result with a distance

    # Return the list of augmented results
    return results
