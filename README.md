## Baza Pool Services

Backend for baza pool services, it hosts cryptocurrency mining pools, pool are hosted based on user voting.
This backend serves API for checking pool stats, vote on a coin/token to host pool. Also it has admin management API
for voting sessions.

### How to run the project

- Copy sample.env

```bash
    cp sample.env .env
```

- Fill the .env file

- Install python poetry and dotenv

- Install dependency

```bash
    poetry install
```

- Migrate DB

```bash
    dotenv run poetry run python manage.py migrate
```

```bash
    dotenv run poetry run python manage.py runserver
```
