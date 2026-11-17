---
id: computing-software.ai-ml-engineering.langchain.postgres-and-sqlite-checkpointers
name: postgres-and-sqlite-checkpointers
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langgraph, memory, checkpointer, langgraph-persistence, postgres-checkpointer, sqlite-checkpointer]
level: practitioner
status: docs-checked
description: "Use LangGraph persistence beyond memory: PostgresSaver / AsyncPostgresSaver and SqliteSaver setup, thread ids, encrypted serde and checkpoint growth."
sources:
  - https://docs.langchain.com/oss/python/langgraph/persistence
  - https://docs.langchain.com/oss/python/langgraph/add-memory
  - https://docs.langchain.com/oss/python/langgraph/checkpointers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Postgres / SQLite checkpointers

`InMemorySaver` (and `MemorySaver`) keep checkpoints in RAM, so they are lost when the process restarts. Use a database-backed checkpointer in production: `PostgresSaver` (with async support) or, for local development, `SqliteSaver`.

## Postgres
```bash
pip install -U "psycopg[binary,pool]" langgraph langgraph-checkpoint-postgres
```
```python
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://user:password@localhost:5432/dbname?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()          # needed the first time you use the Postgres checkpointer
    graph = builder.compile(checkpointer=checkpointer)
    graph.invoke(inp, {"configurable": {"thread_id": "1"}})
```
- Call `checkpointer.setup()` the first time; it creates the tables with indexes.
- Async apps: `from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver`, used as `async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:` followed by `await checkpointer.setup()`.
- Compile the graph with the checkpointer and pass a `thread_id` in `config["configurable"]` for every invocation; the checkpointer holds one thread's short-term state, while a store holds cross-thread long-term data.
- **Keep `thread_id` under 255 characters.** With `PostgresSaver` / `AsyncPostgresSaver` a longer value fails with a database error; use a UUID or hash when you need deterministic IDs.

## SQLite
`langgraph-checkpoint-sqlite` provides `SqliteSaver` / `AsyncSqliteSaver`, described by the docs as ideal for experimentation and local workflows, and installed separately. Construct it from a sqlite3 connection, for example `SqliteSaver(sqlite3.connect("checkpoint.db"))`.

## Operating it
- Checkpoints accumulate over long conversations, increasing latency and storage cost. The docs advise pruning old checkpoints periodically or setting a retention policy (for example a scheduled job that deletes checkpoints older than N days).
- `graph.get_state_history(config)` returns a thread's `StateSnapshot` list, newest first, and needs a `thread_id`. To list across every thread, call `.list` on the checkpointer with `config=None`.
- The default serializer is `JsonPlusSerializer` (ormsgpack and JSON), which does not suit all object types; `pickle_fallback=True` is an option. For encryption at rest use `EncryptedSerializer.from_pycryptodome_aes()` (reads `LANGGRAPH_AES_KEY`) and pass it as `serde=` to `SqliteSaver(...)` or `PostgresSaver.from_conn_string(..., serde=serde)`.
- Under the Agent Server, persistence is handled automatically; you do not configure checkpointers or stores yourself.

## Checked
Method: docs-checked 2026-11-09 against persistence (full), add-memory (production and Postgres sections, grepped for the rest) and checkpointers (grepped serde, sqlite, history sections). Dropped connection-pool autocommit and prepare_threshold advice, delete_thread, state-size and migration guidance, and the unread PyPI source because the pages read do not confirm them.
