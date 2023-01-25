# VATON
![](gH2pO7hOYz0.png)

--- 
This is a basic Rest-api service written in __Fastapi__. It serves as an example to quickly start and develop your own api.  
Full authorisation with JWT-token is implemented.  
The User and Role functions are implemented.  
__SqlAlchemy__ for *Postgresql* is used as orm.  
We have a Small Model with *MongoBD* attached to it. __AsyncMotor__ is used as a driver.  
--- 
### Before starting work, it is necessary to !!!!!!!! 

1) Run docker composer

```sh
docker composer up -d
```

2) Create venv and install poetry

```sh
pip install  poetry
```

3) Install requirements

```sh
poetry install
```

4) Activate venv.
4) Create migration

```sh
alembic upgrade head
```

5) Create role for user

```sh
python commander.py user create-all-role
```

5) Create the first user

```sh
python commander.py user create example@example.ru qwertyneabfywfv8374vf admin adminx
```

---


## Make file Commands
```sh
clean - Remove all build,  
format - Format files  
help - Show this help  
lint - Lint files  
poetry - Install poetry  
pre-commit - Format & lint before commit  
run-dev - Run the local development server  
run - Run the local server  
```

## commander.py

This file contains the basic commands for working with the database via sqlalchemy directly.
Commands:  
> db - Common commands for working with the database  
> user - Common commands for working with users

---

## MIGRATIONS

#### Create a new migration

- add model to app/core/aiembic_import.py
- go into the app folder  
Run commands:
``` sh
alembic revision --autogenerate -m "TEXT INFO"
alembic upgrade head
```

#### Create tables
Run commands:
```sh 
 alembic upgrade head
```
       

---

#### Base Commands poetry

poetry add - install packages  
poetry remove - remove packages  
poetry add - add packages  
poetry update - update all packages  
poetry install - install all packages  
poetry show --latest - show all packages  
