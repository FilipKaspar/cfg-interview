# Bond Service Interview Assignment

## Validations

1. **Isin** - Isin is validated on the model
2. **Maturity date** - Maturity date is validated on the model as well
3. **Bond ownership** - Can be changed, but only in admin. That's intentional, otherwise it can be moved to model's validation from serializer's in order to validate on model's (db) level.

## Installation

In order to set up the virtual environment (for **local** and **tests**):

```bash
uv sync
```

Then either run every command using `uv run` or use:

```bash
source .venv/bin/activate
```

### Local

```bash
python manage.py runserver
```

### Docker

```bash
docker-compose build
```

```bash
docker-compose up
or
docker-compose up -d    # detach mode
```

Server is then ready at `http://localhost:8000/`

### Database

Database example is provided in the repository. 2 users are created with usernames **admin** and **staff**. Passwords are the same as the usernames. Db also has 3 pre-created bonds.

## API

API can be also run through DRF web browser UI at:

`http://localhost:8000/api`


### API Documentation

API Documentation can be accessed on:

`http://localhost:8000/swagger`

## Testing

To run the tests:

```bash
python manage.py test
```

## Localization

Localization has been added as an extra feature with support currently for Czech and English languages.