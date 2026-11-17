---
id: computing-software.ai-ml-engineering.langchain.memory-namespaces-per-user-and-privacy
name: memory-namespaces-per-user-and-privacy
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, memory-namespaces, langgraph-store, privacy, data-deletion, multi-tenant]
level: practitioner
status: docs-checked
description: "Partition LangGraph store memories by user namespace, enforce isolation with @auth.on.store handlers, and configure store and checkpoint TTLs."
sources:
  - https://docs.langchain.com/oss/python/langgraph/stores
  - https://docs.langchain.com/langsmith/store-auth
  - https://docs.langchain.com/langsmith/auth
  - https://docs.langchain.com/langsmith/configure-ttl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Memory namespaces per user and privacy controls

**Goal:** long-term memories do not leak between users, expire when they should, and can be enumerated and deleted per user.

## Namespace design
Store items are addressed by a namespace tuple plus a key. The namespace can be any length and need not be user-specific.
```python
ns = (user_id, "memories")
store.put(ns, memory_id, {"text": "Prefers email over phone"})
hits = store.search(ns, limit=5)         # default limit is 10
```
- `namespace_prefix` in `search` matches by prefix, not exactly: `("alice",)` also returns items under `("alice", "memories")` and `("alice", "preferences")`. To restrict to one level, pass the full namespace or filter on `item.namespace`.
- `store.search` with no query or filter lists items under the prefix; page with `limit` and `offset`.
- `store.list_namespaces(prefix=("alice",), max_depth=2)` discovers which namespaces exist, for example to iterate over users.
- Delete a single item with `store.delete(namespace, key)`.

## Enforce on the server (LangSmith Deployment, or self-hosted with custom auth)
By default store namespaces are shared across all callers. Configure custom authentication and add a store handler. A single `@auth.on.store` handler covers `put`, `get`, `search`, `delete` and `list_namespaces`; action-specific handlers such as `@auth.on.store.put` exist for per-operation rules. Store handlers receive a mutable `value` dict and rewrite `value["namespace"]` rather than returning a metadata filter.

Explicit namespace plus deny (application puts the user identity first in every namespace):
```python
from langgraph_sdk import Auth
auth = Auth()

@auth.on.store
async def authorize_store(ctx: Auth.types.AuthContext, value: Auth.types.on.store.value):
    namespace = tuple(value["namespace"])
    if not namespace or namespace[0] != ctx.user.identity:
        raise Auth.exceptions.HTTPException(status_code=403, detail="Not authorized to access this namespace.")
```
Automatic prefix rewriting (agent code uses logical namespaces such as `("memories", "preferences")`):
```python
@auth.on.store
async def scope_store(ctx: Auth.types.AuthContext, value: Auth.types.on.store.value):
    namespace = tuple(value["namespace"]) if value.get("namespace") else ()
    if not namespace or namespace[0] != ctx.user.identity:
        namespace = (ctx.user.identity, *namespace)
    value["namespace"] = namespace
```
- Pick one scoping layer, auth rewriting or application-level namespaces, not both, or data is double-scoped and reads break.
- The user id for explicit namespaces typically comes from `config["configurable"]["langgraph_auth_user_id"]`.
- A global `@auth.on` handler that denies unhandled requests also blocks the store unless you register `@auth.on.store`.
- Store isolation is separate from thread isolation (thread metadata `owner` filters); configure both for multi-user agents.

## Retention (TTL) in `langgraph.json`
```json
{
  "checkpointer": {"ttl": {"strategy": "delete", "sweep_interval_minutes": 60, "default_ttl": 43200}},
  "store": {"ttl": {"refresh_on_read": true, "sweep_interval_minutes": 120, "default_ttl": 10080}}
}
```
- Times are in minutes. Checkpointer strategies: `delete` (removes the whole thread when TTL expires; window does not refresh with activity) and `keep_latest` (keeps the thread and latest checkpoint, deletes older checkpoint data). If `default_ttl` is omitted nothing expires.
- Store `refresh_on_read` defaults to true (reads via `get` or `search` reset the timer). Store `default_ttl` applies only to items created after deployment; delete older items manually.
- Override per item by passing `ttl` to `put`, and control read refresh with `refresh_ttl` on `get` / `search`. A per-thread TTL can be set in `client.threads.create(ttl={"strategy": "delete", "ttl": 43200})`.
- Restart or redeploy (`langgraph dev` or `langgraph up`) for TTL config to take effect.

## Verify
- [ ] Cross-user test: user B reading the same logical namespace sees only their own item, and cannot read user A's note.
- [ ] Deleting a user's items via `list_namespaces` plus `delete` leaves nothing under their prefix.

## Checked
Method: docs-checked 2026-11-09 against stores (grepped namespace and search sections), store-auth (full), auth (handler table, grepped) and configure-ttl (full). Dropped the org-level namespace scheme, LangMem templated namespaces, PII filtering and export/erasure advice, which the pages read do not confirm.
