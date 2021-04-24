# Simple REST API for Yalantis.
-------------------------------

## Overview
This is the server part of the REST API implementation of the
[Yalantis test task](https://bit.ly/39LSq74).
the solution is based on the use of the
[OpenAPI/Swagger](https://openapis.org)
[specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md)
and the
[Connexion/Flask](https://github.com/zalando/connexion)
 framework.

## Requirements
Python 3.7 or higher

## Usage
To run the server, please execute the following from the root directory:

```
  pip install -r requirements.txt
  python -m api
```

and open your browser to here:

```
  http://localhost:5000/api/v1/ui/
```

OpenAPI definition lives here:

```
  http://localhost:5000/api/v1/openapi.json
```

This ReadMe document can also be found at the following address:

```
  http://localhost:5000/
```

## Examples
In the "examples/" directory you will find examples of queries to various API endpoints using Python.

## Endpoints
This API provides the following endpoints:

1. Add course to the database.  
  *Path:* /api/v1/add  
  *Allowed methods:* GET, POST  
  *Required fields:*  
    - **name**: the name of the training course;
    - **start**: the start date of the course in ISO format;
    - **end**: the end date of the course in ISO format;
    - **amount**: the number of lectures that make up the course.  
  *Response*: the course that has been added to the database with its assigned ID.
2. Get a course from the database by its ID.  
  *Path:* /api/v1/course/{id}  
  *Allowed method:* GET  
  *Response*: the course from the database with its ID.
3. Delete a course from the database by its ID.  
  *Path:* /api/v1/course/{id}  
  *Allowed method:* DELETE  
  *Response*: the deleted course from the database with its ID.
4. Update course information by the specified ID.  
  *Path:* /api/v1/course/{id}  
  *Allowed method:* PUT  
  *Required fields:*  
    - **name**: the name of the training course;
    - **start**: the start date of the course in ISO format;
    - **end**: the end date of the course in ISO format;
    - **amount**: the number of lectures that make up the course.  
  *Response*: the updated course in the database with its ID.
5. Search the database by part of the name and filter by start or end dates.  
  *Path:* /api/v1/search  
  *Allowed methods:* GET, POST  
  *Optional fields:*  
    - **name**: the part of the course name;
    - **start**: the start date to filter results;
    - **end**: the end date to filter results;  
  *Response*: a list of courses that meet the search criteria.

## Testing
There are several possible ways for running tests.  
To install all the necessary dependencies for the test environment - do the following:

```
  pip install -r test-requirements.txt
```

### Unittest
This is the easiest and fastest way - just run the following command from the root of the repository:

```
  python -m unittest discover
```

### PyTest
The following command will run the tests using the ** pytest ** tool:

```
  python -m pytest
```

### Running integration tests
The ** tox ** tool allows to check the correct working of the server in different environments.  
To run a set of tests in Python versions 3.7, 3.8 and 3.9 - run the following commands:

```
  pip install tox
  python -m tox
```

## Linters
The source code of the module meets the formatting standards PEP and has [type hints](https://mypy.readthedocs.io).

## Deploy in production
To deploy the module in production, please use a WSGI server.  
Don't forget to change the value of the variable ** api.config.SERVER_NAME **.

## License
This project is distributed under the General Public License version 2.

## Contacts
The author of this project: [** Oleksandr Gryshchenko **](https://ua.linkedin.com/in/grisov).  
You can contact the author through his [GitHub account](https://github.com/grisov).

## Contributions
Anyone can make changes to this project by creating a Pull Request [here](https://github.com/grisov/catalog_of_courses).
