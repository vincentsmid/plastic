# FastAPI template repository

This is a template repository to be cloned and built upon when creating a new project. Environment is managed by poetry, templating by jinja, fastAPI for api, SQLite DB for development, PiccoloORM with its admin and more.

Dev environment completely automatised on docker.

## API documentation

### [Swagger UI](https://localhost:8000/docs)

Swagger UI is used to manually test and check API endpoints.

### [Database admin panel](http://localhost:8000/database)

Here runs piccolo admin - here you can see everything important in databases - refer to Database structure below to see what is what.

## How to run locally without Docker Compose

1. Clone the repository and make sure you have Python 3.11 installed (should work with 3.10 too).

2. Install [Poetry for Python](https://python-poetry.org/docs/#installation)
   - For change of version go to file `pyproject.toml` and change line:`python = "^3.11"` to `python = "^3.10"`
   - then delete the file `poetry.lock` and run `poetry lock`.

3. Move into the cloned directory.

```bash
cd <reponame>
```

4. Install all dependencies and enter shell

```bash
poetry install
poetry shell
```

You can now select the appropriate Python interpreter version in the bottom right corner of VS Code.

5. Create DB migrations

```bash
piccolo migrations new main_app --auto
```

6. Apply all database migrations

```bash
piccolo migrations forwards all
```

7. Create admin user

```bash
piccolo user create
```

8. Change environment variables in `main_app/.env` (access your working dir using command `pwd`)

```
WHATEVER_ENV_VARIABLES_YOU_USE="Hello"
```

9. Run the uvicorn server

```bash
uvicorn main_app.main:app --reload --host 0.0.0.0 --port 8000
```

## File structure - change as you need, but a lot will probably remain the same

An example taken from [our CDN](https://gitlab.gpcz.eu/green-panda/cdn).

```
/
│
├── main_app/                   # Main application package
│   ├── main.py                 # Entry point for the FastAPI app + jinja + piccolo admin
│   ├── db_models.py            # PiccoloORM db models
│   ├── validation.py           # Functions to validate permissions
│   ├── generator.py            # Functions to generate new admins and
applications
│   ├── fileinfo.sqlite         # SQLite database file
│   ├── api/                    # API related modules
│   │   ├── api_admin           # Admin dashboard api modules
│   │   │   │   ├── generate_user.py      # Endpoint to create cdn superusers (admins, not applications)
│   │   │   │   ├── user_login.py         # Admin login
│   │   │   │   ├── generate_app.py       # Endpoint to generate an external app that will access the API
│   │   │   │   └── generate_project.py   # Endpoint to generate a file project to be accessed by apps authorized to do so
│   │   │   └── router.py       # FastAPI Router for admin api
│   │   ├── api_v1/             # Version 1 of the API
│   │   │   ├── endpoints/      # Endpoints for version 1
│   │   │   │   ├── download_files.py  # File download endpoint
│   │   │   │   ├── upload_files.py    # File upload endpoint
│   │   │   │   ├── delete_files.py    # File delete endpoint
│   │   │   │   └── make_public.py     # Endpoint to publish an already uploaded file via caddy to a static url open to the www
│   │   │   └── router.py       # FastAPI Router for version 1 API
│   │   └── ...                 # Future API versions
│   └── piccolo_migrations/     # Dir for database migrations
│       └── main_app_....       # Migration files (there will be multiple - dev side needs to generate them using migration commands)
│
├── templates/                  # Jinja templates for frontend
│   └── index.html              # Jinja index
│
├── static/                     # Static assets
│   └── styles.css              # Styles used by jinja
│
├── pyproject.toml              # Project dependencies
├── piccolo_conf.py             # PiccoloORM configuration
├── Dockerfile                  # Dockerfile
├── docker-compose.yml          # Docker-compose used for running the app
└── README.md                   # Documentation
```

## DB structure

### DB structure is defined in db_models.py

Current:

```python
print("paste the contents of db_models.py here")
```
