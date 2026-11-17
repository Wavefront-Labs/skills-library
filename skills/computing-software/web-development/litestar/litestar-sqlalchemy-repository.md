---
id: computing-software.web-development.litestar.litestar-sqlalchemy-repository
name: litestar-sqlalchemy-repository
category: computing-software
field: web-development
product: litestar
tags: [litestar, sqlalchemy, repository, sqlalchemy-models, advanced-alchemy, uuidbase, crud, controller]
level: practitioner
status: docs-checked
description: "Define Litestar SQLAlchemy models on the built-in UUID or BigInt bases and wire SQLAlchemyAsyncRepository into controllers via a repository provider."
sources: [https://docs.litestar.dev/latest/usage/databases/sqlalchemy/models_and_repository.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar SQLAlchemy models and repository

Goal: get CRUD, pagination and bulk operations from the built-in repository classes instead of hand-written queries.

## Method

1. Declare models on one of the built-in `DeclarativeBase` bases (imported from `advanced_alchemy.base`; the examples import them as `base` from `advanced_alchemy.extensions.litestar`):
   - `UUIDBase` / `UUIDAuditBase`: UUID primary key. Native `UUID`/`GUID` where supported (Postgres), otherwise a 16-byte `BYTES` or `RAW` field.
   - `BigIntBase` / `BigIntAuditBase`: `BigInteger` primary key.
   - The `Audit` variants add `created_at` and `updated_at`.
2. Bases also give you an auto-generated snake-case table name from the class name, and Pydantic `BaseModel` and `Dict` classes map to an optimized JSON type (`JSONB` on Postgres, `VARCHAR` or `BYTES` with a JSON check constraint on Oracle, `JSON` on other dialects).
3. Create a repository by subclassing `SQLAlchemyAsyncRepository[Model]` (or `SQLAlchemySyncRepository` for a sync connection) and set `model_type`.
4. Provide it to controllers with a small function that takes the plugin-supplied session, then register it in `dependencies`:

```python
class AuthorRepository(repository.SQLAlchemyAsyncRepository[AuthorModel]):
    model_type = AuthorModel

async def provide_authors_repo(db_session: NamedDependency[AsyncSession]) -> AuthorRepository:
    return AuthorRepository(session=db_session)

class AuthorController(Controller):
    dependencies = {"authors_repo": Provide(provide_authors_repo)}
```

5. Configure the session with `SQLAlchemyAsyncConfig(connection_string=..., session_config=AsyncSessionConfig(expire_on_commit=False))` and add `SQLAlchemyInitPlugin(config=...)`; this creates the `db_session` dependency.
6. To add query options (for example eager loading) pass your own `statement=select(AuthorModel).options(selectinload(AuthorModel.books))` to the repository constructor.

## Features listed

- Generic sync and async repositories for select, insert, update, delete.
- Optimized bulk insert/update/delete, using `lambda_stmt` when possible.
- Counts, pagination, sorting and filtering with `LIKE`, `IN` and before/after dates.
- Tested backends: SQLite (aiosqlite or sqlite), Postgres (asyncpg, psycopg3), MySQL (asyncmy), Oracle (oracledb), Google Spanner, DuckDB, SQL Server (pyodbc).

## Verify

Run the docs example `sqlalchemy_async_repository.py`: its `AuthorController` exposes list, create, get, update and delete routes under `/authors`.

## Checked

2026-11-07. Read the full cited page(s) (usage/databases/sqlalchemy/models_and_repository.html) and the example files they include, and confirmed the claims in this skill against that text. Added the Oracle JSON-type exception the page lists.

Method: documentation only; no commands were run.
