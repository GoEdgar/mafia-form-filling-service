# Form filling API for Mafia Statistics

## Installation

* Setup virtual environment:
    ```bash
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    ```
* Install dependencies
    ```bash
    pip install 'setuptools<58.0.0'
    pip install -r requirements.txt
    ```
* Create local database with PostgreSQL and set the following environment
  variables:
    ```text
    DB_USER
    DB_PASSWORD
    DB_HOST
    DB_PORT
    DB_NAME
    ```

## Running

* Firstly, run migrations with alembic:
    ```bash
    alembic upgrade head
    ```
* Then run web-server (configure the port if you need):
    ```bash
    gunicorn --bind 0.0.0.0:8000 -w 1 -t 4 main:app
    ```
