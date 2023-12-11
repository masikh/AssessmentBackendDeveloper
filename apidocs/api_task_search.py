""" APIDocs for /api/task/search """


class APITaskSearch:  # pylint: disable=too-few-public-methods
    """flasgger definition for /api/task/search"""

    api_search_task = {
        "tags": ["Tasks"],
        "summary": "Search tasks",
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "type": "string",
                "required": True,
                "description": "Authentication token",
            },
            {
                "name": "page",
                "in": "query",
                "schema": {"type": "int"},
                "description": "Page number for pagination",
            },
            {
                "name": "page_size",
                "in": "query",
                "schema": {"type": "int"},
                "description": "Number of tasks per page",
            },
            {
                "name": "status",
                "in": "query",
                "schema": {"type": "string"},
                "description": "Filter tasks by status",
            },
            {
                "name": "after",
                "in": "query",
                "schema": {"type": "string"},
                "description": "Filter tasks due after this date (YYYY-MM-dd)",
            },
            {
                "name": "before",
                "in": "query",
                "schema": {"type": "string"},
                "description": "Filter tasks due before this date (YYYY-MM-dd)",
            },
            {
                "name": "title",
                "in": "query",
                "schema": {"type": "string"},
                "description": "Search tasks by title",
            },
            {
                "name": "sort_order",
                "in": "query",
                "schema": {"type": "string", "enum": ["ascending", "descending"]},
                "description": "Sort order for tasks ('ascending' or 'descending')",
            },
        ],
        "responses": {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "example": {
                            "current_page": 1,
                            "last_page": 3,
                            "result": [
                                {
                                    "id": 1,
                                    "title": "Task 1",
                                    "description": "Description 1",
                                    "status": "Pending",
                                    "due_date": "2023-01-01T12:00:00",
                                },
                                {
                                    "id": 2,
                                    "title": "Task 2",
                                    "description": "Description 2",
                                    "status": "Completed",
                                    "due_date": "2023-01-02T12:00:00",
                                },
                            ],
                        }
                    }
                },
            },
            "400": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "Invalid page or page_size. Please provide valid numeric values."
                        }
                    }
                },
            },
            "403": {
                "description": "Forbidden",
                "content": {"application/json": {"example": {"error": "Forbidden"}}},
            },
            "500": {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {"example": {"error": "Internal Server Error"}}
                },
            },
        },
    }
