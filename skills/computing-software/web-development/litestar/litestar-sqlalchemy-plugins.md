---
id: computing-software.web-development.litestar.litestar-sqlalchemy-plugins
name: litestar-sqlalchemy-plugins
category: computing-software
field: web-development
product: litestar
tags: [litestar, sqlalchemy, init-plugin, serialization-plugin, advanced-alchemy, dependency-injection, dto]
level: practitioner
status: docs-checked
description: "Wire SQLAlchemyPlugin, SQLAlchemyInitPlugin and SQLAlchemySerializationPlugin into Litestar: session and engine injection, before_send handlers, DTO generation."
sources: [https://docs.litestar.dev/latest/usage/databases/sqlalchemy/plugins/sqlalchemy_plugin.html, https://docs.litestar.dev/latest/usage/databases/sqlalchemy/plugins/sqlalchemy_init_plugin.html, https://docs.litestar.dev/latest/usage/databases/sqlalchemy/plugins/sqlalchemy_serialization_plugin.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar SQLAlchemy plugins

Goal: use SQLAlchemy 2.0+ in Litestar with injected sessions and automatic model serialization. Install: `pip install 'litestar[sqlalchemy]'`. The plugins live in `advanced_alchemy.extensions.litestar`.

## Method

`SQLAlchemyPlugin` combines `SQLAlchemyInitPlugin` and `SQLAlchemySerializationPlugin`:

```python
from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.di import NamedDependency

@post("/")
async def add_item(data: JSONBody[TodoItem], db_session: NamedDependency[AsyncSession]) -> Sequence[TodoItem]:
    async with db_session.begin():
        db_session.add(data)
    return (await db_session.execute(select(TodoItem))).scalars().all()

config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///todo_async.sqlite", create_all=True, metadata=Base.metadata
)
app = Litestar(route_handlers=[add_item], plugins=[SQLAlchemyPlugin(config=config)])
```

Sync variant uses `SQLAlchemySyncConfig`. Run with `litestar run`; the example in the page accepts a POST to `/` with JSON body like `{"title": "Your Todo Title", "done": false}`.

Init plugin (`SQLAlchemyInitPlugin(config=config)`):
- Makes the engine and session injectable (`db_session`, `db_engine` by default); stores engine and session factory in app state; configures a `before_send` handler; adds names to the signature namespace.
- Rename the dependencies with `engine_dependency_key` and `session_dependency_key` on the config.
- Default `before_send_handler` closes the session and removes it from the connection scope. Use `before_send_handler=async_autocommit_before_send_handler` to commit on success and roll back on failure.
- `engine_config` (`EngineConfig`) and `session_config` (`AsyncSessionConfig` or `SyncSessionConfig`) expose engine and session options.

Serialization plugin (`SQLAlchemySerializationPlugin()`, no arguments): generates a `SQLAlchemyDTO` for each handler `data` or return annotation that is a SQLAlchemy model (or collection) not already covered by an explicit DTO. Control fields by marking: `super_secret_value: Mapped[str] = mapped_column(info=dto_field("private"))` keeps the value out of responses.

## Gotchas

- The page's example drops the database before creating it for repeatability; do not do that in production.

## Verify

With the marking example, POSTing to `/` returns the item without `super_secret_value`, although the handler sets it.

## Checked

2026-11-07. Read the full cited page(s) (usage/databases/sqlalchemy/plugins/sqlalchemy_plugin.html, usage/databases/sqlalchemy/plugins/sqlalchemy_init_plugin.html, usage/databases/sqlalchemy/plugins/sqlalchemy_serialization_plugin.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
