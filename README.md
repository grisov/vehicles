# Simple REST API.
------------------

## Overview

This is the server part of the REST API implementation of the
[Yalantis test task](https://docs.google.com/document/d/1sAqFWAIO1gIZbajQzFgW1f72qmfI8bdE-FE-JDCc5zU).
the solution is based on the
[OpenAPI/Swagger](https://openapis.org)
[specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md)
and the modern and fast (high-performance) framework
[FastAPI](https://fastapi.tiangolo.com/).


## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management (automatically installed inside the docker container).

**Note**: To run the application it is enough that only the `docker compose` tool is installed on the system. There is no need to install dependencies manually, the whole project will be automatically assembled and run inside the docker container.


## Usage

### Build and run application

* Start the stack with Docker Compose:

    ```bash
    docker compose up --build backend
    ```

* Now you can open your browser and interact with these URLs:

    - View this [README document as a web page](http://localhost:8000);

    - Automatic interactive documentation with Swagger UI (from the OpenAPI): [http://localhost:8000/docs](http://localhost:8000/docs)

    - Alternative automatic documentation with ReDoc (from the OpenAPI): [http://localhost:8000/redoc](http://localhost:8000/redoc)

**Note**: The first time you start your stack, it might take a minute for it to be ready.

To check the logs, run:

```bash
docker compose logs backend
```

### API endpoints

Once the docker container is successfully launched, you can make requests to the API endpoints of the application.

All endpoints are fully meet the requirements of the [task](https://docs.google.com/document/d/1sAqFWAIO1gIZbajQzFgW1f72qmfI8bdE-FE-JDCc5zU).

Detailed examples of requests can be found in the `./examples/` directory.


## Extra features

Because the SQLite database file is created and located inside the running docker container, all data in it is stored only while the docker container is running.

To quickly populate a database with randomly generated data, you can use the following command:

```bash
docker compose exec backend python -c "from app.utils import fill; fill()"
```

After that you can retrieve the contents of one of the tables using the following query from any external Python interpreter:

```python
import requests
response = requests.get("http://localhost:8000/vehicles/vehicle/")
print(response.json())
```


## Tools

### Tests

The application has a collection of intergration and unit tests for all endpoints, CRUD (create-read-update-delete) utils and some other components.

After the docker container started, a set of all tests can be run as follows:

```console
$ docker compose exec backend pytest
```

**Note**: To view the source code of the tests, go to the `./backend/app/app/tests/` directory.

More details on how to run tests will be described in the following sections.

### MyPy linter

The entire source code of the application is equipped with [type hints](https://mypy.readthedocs.io), you can check it with the following command:

```console
$ docker compose exec backend mypy app
```

### Flake8 linter

[**Flake8**](https://flake8.pycqa.org)
is a great toolkit for checking source code base against coding style (PEP8), programming errors (like "library imported but unused" and "Undefined name") and to check cyclomatic complexity.

To run this tool, use the following command:

```console
$ docker compose exec backend flake8 .
```

If no issue is found in the source code, the command will not output anything after the scan is complete.


## Additional details

### Dependencies

By default, the dependencies are managed with [Poetry](https://python-poetry.org/).

You can view the list of dependencies in the following file: `./backend/app/pyproject.toml`.

From `./backend/app/` you can install all the dependencies with:

```console
$ poetry install
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

Next, open your editor at `./backend/app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code inside. That way, your editor will be able to find all the imports, etc. Make sure your editor uses the environment you just created with Poetry.

Modify or add SQLAlchemy models in `./backend/app/app/models/`, Pydantic schemas in `./backend/app/app/schemas/`, API endpoints in `./backend/app/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./backend/app/app/crud/`. The easiest might be to copy the ones for Items (models, endpoints, and CRUD utils) and update them to your needs.

### How to launch the console inside the docker container

```console
$ docker compose up -d
```

and then `exec` inside the running container:

```console
$ docker compose exec backend bash
```

You should see an output like:

```console
root@7f2607af31c3:/app#
```

that means that you are in a `bash` session inside your container, as a `root` user, under the `/app` directory.

### How to run tests

To test the application run (inside the container):

```console
pytest
```

The tests run with Pytest, modify and add tests to `./backend/app/app/tests/`.

The `./backend/app` directory is mounted as a "host volume" inside the docker container (set in the file `docker-compose.yml`).
You can rerun the test on live code:

```Bash
docker compose exec backend pytest
```

You can also specify the parameters of the pytest command. For example, to stop on first error:

```bash
docker compose exec backend pytest -x
```

#### Test Coverage

Because the test scripts forward arguments to `pytest`, you can enable test coverage HTML report generation by passing `--cov-report=html`.

To run the local tests with coverage HTML reports:

```Bash
pytest --cov-report=html
```

To run the tests in a running stack with coverage HTML reports:

```bash
docker compose exec backend pytest --cov-report=html
```

### Deployment Technical Details

Building and pushing is done with the `docker-compose.yml` file, using the `docker compose` command. The file `docker-compose.yml` uses the file `.env` with default environment variables. And the scripts set some additional environment variables as well.


## Docker Compose files and env vars

There is a `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker compose`.

This Docker Compose file use the `.env` file containing configurations to be injected as environment variables in the container.

It also use some additional configurations taken from environment variables set in the scripts before calling the `docker compose` command.

It is all designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

Project designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose file.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose file.

### The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

Depending on your workflow, you could want to exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.

One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.


## URLs

These are the URLs that will be used and generated by the project.

Index page: [http://localhost:8000](http://localhost:8000)

Automatic Interactive Docs (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

Automatic Alternative Docs (ReDoc): [http://localhost:8000/redoc](http://localhost:8000/redoc)


## Thanks

This project was created using https://github.com/tiangolo/full-stack-fastapi-postgresql template.


## License

This project is distributed under the General Public License version 2.


## Contacts

The author of this project: [**Oleksandr Gryshchenko**](https://ua.linkedin.com/in/grisov).

You can contact the author through his [GitHub account](https://github.com/grisov).

Curriculum vitae can be downloaded [here](https://info.alwaysdata.net/static/grisov_curriculum_vitae.pdf).


## Contributions

Anyone can make changes to this project by creating a Pull Request [here](https://github.com/grisov/vehicles).
