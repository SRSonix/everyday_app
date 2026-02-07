# Everyday App

## Local Development

### Start the Database

```bash
docker compose up -d
```

This starts a PostgreSQL 17 instance on `localhost:5432`. Data is persisted in `.pgdata/` at the project root.

### Run Migrations

```bash
cd migrations
uv sync
uv run python run.py
```

By default this runs `alembic upgrade head`. You can pass custom alembic arguments:

```bash
uv run python run.py downgrade -1
```

### Run the App

```bash
cd app
uv sync
set +a && . app/local.env && set -a
uv run fastapi dev
```

### Run Tests

```bash
cd app
uv run pytest
```

Tests use testcontainers to spin up an isolated PostgreSQL instance automatically.
