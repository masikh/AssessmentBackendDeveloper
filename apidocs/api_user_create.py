""" APIDocs for /api/user/create """


class APIUserCreate:  # pylint: disable=too-few-public-methods
    """flasgger definition for /api/user/create"""

    create_user = {
        "tags": ["User"],
        "summary": "Create a new user",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "id": "create_user",
                    "required": ["email", "name", "password"],
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "User's email",
                        },
                        "name": {
                            "type": "string",
                            "description": "User's name",
                        },
                        "password": {
                            "type": "string",
                            "description": "User's password",
                        },
                    },
                },
            },
        ],
        "responses": {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "example": {
                            "email": "user@example.com",
                            "name": "John Doe",
                        }
                    }
                },
            },
            "400": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": {"error": "email, name and password cannot be null"}
                    }
                },
            },
            "409": {
                "description": "Conflict",
                "content": {
                    "application/json": {"example": {"error": "email already taken"}}
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
