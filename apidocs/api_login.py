""" APIDocs for /api/login """


class APILogin:  # pylint: disable=too-few-public-methods
    """flasgger definition for /api/login"""

    login_user = {
        "tags": ["User"],
        "summary": "User login",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "id": "login_user",
                    "required": ["email", "password"],
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "User's email",
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
                            "token": "example_token",
                        }
                    }
                },
            },
            "400": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": {"error": "email and password cannot be null"}
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
