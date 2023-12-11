# Contents

[Assessment Backend Developer](#Assessment-Backend-Developer)  
[APIDocs](#API-Documentation)  


## Assessment Backend Developer

**Dear candidate,**

It's great that you are taking our test. Through this test, we aim to assess your knowledge of Python, Flask, REST APIs, and self-sufficiency. We use this test for both inexperienced and experienced Python developers. It's important that you demonstrate an understanding of the core elements of Python, including the correct use of SOLID principles, exception handling, OOP, decorators, and package management. Additionally, inheritance is crucial as long as it is functional within the test application. Of course, it's important that you work in an organized and structured manner.

**To begin, we ask the following:**

- Create a publicly accessible git repository.
- Make clean interim commits so that the steps you have taken can be traced from your commits.
- Use Flask.
- Adhere to best practices for Python.
- Provide comments in your code to explain why you make certain choices. For this test, there are no "too many" comments as long as they clarify your thought process.
- Create a Flask REST API for a simple task list. The API should support basic operations such as retrieving all tasks, retrieving a specific task, adding a new task, and updating/removing an existing task.

**We expect the following from you:**

- An endpoint for searching tasks.
- Support for pagination, filtering, and sorting.
- Unit testing.
- (EXTRA) - Add authorization.
- (EXTRA) - Demonstrate the use of Azure services (can be mocked).

**Assessment criteria:**

- Structure and organization (40%)
- Re-usability and performance (30%)
- Code quality and best practices (30%)

## API Documentation

### /api/task [methods: GET, POST]

**GET**

required headers: 

    {'Authorization': 'token'}  

query parameters: 
    
    page (int)
    page_size (int)

returns:

200

    {
        'current_page': int, 
        'last_page': int, 
        'result': [
            {
                'id': int, 
                'title': string, 
                'description': string, 
                'status': string, 
                'due_date': datetime.isoformat
            }
        ]
    }  

400

    {'error': 'Invalid page or page_size. Please provide valid numeric values.'}
    {'error': 'Authorization header missing'}

403

    {'error': 'Forbidden'}

500

    {'error': str}

**POST**

required headers: 

    {'Authorization': 'token'}  

body:

    {
        'title': string (optional), 
        'description': string (optional), 
        'status': string (optional), 
        'due_date': datetime.isoformat (optional)
    }

returns:

200

    {
        'id': int, 
        'title': string, 
        'description': string, 
        'status': string, 
        'due_date': datetime.isoformat
    }

403

    {'error': 'Forbidden'}

500

    {'error': str}

### /api/task/< id >  [methods: GET, PATCH, DELETE]

**GET**

required headers: 

    {'Authorization': 'token'}  

returns:

200

    {
        'id': int, 
        'title': string, 
        'description': string, 
        'status': string, 
        'due_date': datetime.isoformat
    }

403

    {'error': 'Forbidden'}

500

    {'error': str}

**PATCH**

required headers: 

    {'Authorization': 'token'}  

body:

    {
        'title': string (optional), 
        'description': string (optional), 
        'status': string (optional), 
        'due_date': datetime.isoformat (optional)
    }

returns:

200

    {
        'id': int, 
        'title': string, 
        'description': string, 
        'status': string, 
        'due_date': datetime.isoformat
    }

403

    {'error': 'Forbidden'}

404

    {'error': 'Task not found'}

500

    {'error': str}

**DELETE**

required headers: 

    {'Authorization': 'token'}  

returns:

200

    'DELETED'

403

    {'error': 'Forbidden'}

404

    {'error': 'Task not found'}

500

    {'error': str}

### /api/task/search [methods: GET]

required headers: 

    {'Authorization': 'token'}  

query parameters: 
    
    page (int)
    page_size (int)
    status (string)
    after (string) YYYY-MM-dd
    before (string) YYYY-MM-dd
    title (string) 

returns:

200

    {
        'current_page': int, 
        'last_page': int, 
        'result': [
            {
                'id': int, 
                'title': string, 
                'description': string, 
                'status': string, 
                'due_date': datetime.isoformat
            }
        ]
    }  

400

    {'error': 'Invalid page or page_size. Please provide valid numeric values.'}
    {'error': 'Authorization header missing'}

403

    {'error': 'Forbidden'}

500

    {'error': str}


### /api/user/create [methods: POST]

**POST**

body:

    {
        'email': string, 
        'name': string, 
        'password': string
    }

returns:

200

    {
        'email': string, 
        'name': string
    }

400

    {'error': 'email, name and password cannot be null'}
    {'error': 'email already taken'}

500

    {'error': str}

### /api/user/login [methods: POST]

**POST**

body:

    {
        'email': string,
        'password': string
    }

returns:

200

    {
        'token': string
    }

400

    {'error': 'email and password cannot be null'}

403

    {'error' 'Forbidden'}

500

    {'error': str}
