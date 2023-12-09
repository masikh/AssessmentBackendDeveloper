""" Create paginated results """


def set_paginated_response(data, page=1, page_size=20):
    """ Set paginated result

        default to first page and a page_size of 20 items
    """

    # Compute the total amount of pages using page_size and the amount of items per page
    total_items = len(data)
    total_pages = (total_items + page_size - 1) // page_size  # Calculate total pages

    # Guard clause. Return an empty list if we're out of bounds
    if page < 1 or page > total_pages:
        return {
            'result': [],
            'current_page': page,
            'last_page': total_pages
        }

    # Compute the start and end index in the 'data' array
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_items = data[start_index:end_index]

    # Return the result alongside useful information to retrieve the next or former page
    return {
        'result': paginated_items,
        'current_page': page,
        'last_page': total_pages
    }
