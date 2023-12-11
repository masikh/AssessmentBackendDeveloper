class APITaskCRUD:
    jwt_header = {
        "name": "Authorization",
        "in": "header",
        "type": "string",
        "required": True,
        "description": "Authentication token",
    }

    task_properties = {
        "id": {"type": "int", "description": "Unique identifier for the task"},
        "title": {"type": "string", "description": "Title of the task"},
        "description": {"type": "string", "description": "Description of the task"},
        "status": {"type": "string", "description": "Status of the task"},
        "due_date": {
            "type": "datetime",
            "description": "Due date of the task in ISO format",
        },
    }

    api_get_tasks = {
        "tags": ["Task"],
        "summary": "Get a list of tasks",
        "parameters": [
            jwt_header,
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
            "401": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {"error": "Authorization header missing"}
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

    api_post_task = {
        "tags": ["Task"],
        "summary": "Create a new task",
        "parameters": [
            jwt_header,
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "id": "task_properties",
                    "required": ["title", "description", "status", "due_date"],
                    "properties": task_properties,
                },
            },
        ],
        "responses": {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 1,
                            "title": "New Task",
                            "description": "New Task Description",
                            "status": "Pending",
                            "due_date": "2023-01-03T12:00:00",
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

    api_get_task_by_id = {
        "tags": ["Task"],
        "summary": "Get details of a specific task by ID",
        "parameters": [
            {
                "name": "id",
                "in": "path",
                "required": True,
                "schema": {"type": "int"},
                "description": "ID of the task",
            },
            jwt_header,
        ],
        "responses": {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 1,
                            "title": "Task 1",
                            "description": "Description 1",
                            "status": "Pending",
                            "due_date": "2023-01-01T12:00:00",
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

    api_patch_task_by_id = {
        "tags": ["Task"],
        "summary": "Update details of a specific task by ID",
        "parameters": [
            jwt_header,
            {
                "name": "id",
                "in": "path",
                "required": True,
                "schema": {"type": "int"},
                "description": "ID of the task",
            },
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "id": "task_properties",
                    "required": ["title", "description", "status", "due_date"],
                    "properties": task_properties,
                },
            },
        ],
        "responses": {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 1,
                            "title": "Updated Task",
                            "description": "Updated Task Description",
                            "status": "Completed",
                            "due_date": "2023-01-04T12:00:00",
                        }
                    }
                },
            },
            "403": {
                "description": "Forbidden",
                "content": {"application/json": {"example": {"error": "Forbidden"}}},
            },
            "404": {
                "description": "Not Found",
                "content": {
                    "application/json": {"example": {"error": "Task not found"}}
                },
            },
            "500": {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {"example": {"error": "Internal Server Error"}}
                },
            },
        },
    }

    api_delete_task_by_id = {
        "tags": ["Task"],
        "summary": "Delete a specific task by ID",
        "parameters": [
            jwt_header,
            {
                "name": "id",
                "in": "path",
                "required": True,
                "schema": {"type": "int"},
                "description": "ID of the task",
            },
        ],
        "responses": {
            "200": {
                "description": "Successful response",
                "content": {"application/json": {"example": "DELETED"}},
            },
            "403": {
                "description": "Forbidden",
                "content": {"application/json": {"example": {"error": "Forbidden"}}},
            },
            "404": {
                "description": "Not Found",
                "content": {
                    "application/json": {"example": {"error": "Task not found"}}
                },
            },
            "500": {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {"example": {"error": "Internal Server Error"}}
                },
            },
        },
    }
