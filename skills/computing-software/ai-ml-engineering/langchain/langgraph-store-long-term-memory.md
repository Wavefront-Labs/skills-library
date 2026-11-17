---
id: computing-software.ai-ml-engineering.langchain.langgraph-store-long-term-memory
name: langgraph-store-long-term-memory
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langgraph, memory, long-term-memory, langgraph-store, basestore, postgresstore, cross-thread-memory]
level: practitioner
status: verified
description: "Persist memories across LangGraph threads with BaseStore: namespaces per user, put/get/search, semantic index config, PostgresStore in production and injecting store into nodes."
sources:
  - https://langchain-ai.github.io/langgraph/concepts/memory/
  - https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/
  - https://langchain-ai.github.io/langgraph/reference/store/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Long-term memory with BaseStore

Checkpointers hold **one thread's** state. A store holds data shared **across threads** (user preferences, learned facts, org knowledge).

## Store setup
```python
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore          # pip install langgraph-checkpoint-postgres (also needs psycopg; not run here, no Postgres: signature and the pgvector migrations were read from the package source)
store = InMemoryStore(index={"embed": "openai:text-embedding-3-small", "dims": 1536, "fields": ["text"]})
# production:
with PostgresStore.from_conn_string(DB_URI, index={"embed": embed_fn, "dims": 1024}) as store:
    store.setup()                                           # runs migrations (pgvector needed for index)
    app = builder.compile(checkpointer=checkpointer, store=store)
```

## Reading and writing in nodes
```python
from langgraph.store.base import BaseStore
def call_model(state, config, *, store: BaseStore):
    uid = config["configurable"]["user_id"]
    ns = ("users", uid, "memories")
    hits = store.search(ns, query=state["messages"][-1].content, limit=5)
    facts = "\n".join(h.value["text"] for h in hits)
    ...
    store.put(ns, key=str(uuid4()), value={"text": "Prefers invoices in EUR", "source_thread": config["configurable"]["thread_id"]})
```
Newer APIs inject via `runtime: Runtime[Context]` and `runtime.store`; `get_store()` works inside tools.

- Namespaces are tuples - put the user/tenant id in them and derive it from authenticated config, never from model output.
- `put` with an existing key overwrites (use it to update a profile document); `delete(ns, key)` for right-to-erasure.
- `search` without `query` filters by namespace prefix and `filter={"type": "preference"}`; with `query` it ranks by embedding similarity (requires index config). Items stored with `index=False` are still returned after the ranked ones with `score=None` (run), so filter on `score` if you only want semantic hits.
- `index=False` on `put` stores without embedding (cheap for bulk metadata).

## Design
- Profile (one document per user, updated) vs collection (many small facts, searched). Profiles are easy to inject; collections scale but need dedupe.
- Write memories in the background (after responding) to keep latency low.
- Show users what is remembered and let them delete it.

## Verify
- [ ] Fact stored in thread A is retrieved in a new thread B for the same user, not for another user.
- [ ] Store survives restart (Postgres) and delete removes the item from search results.
