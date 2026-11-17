---
id: computing-software.web-development.litestar.litestar-stores-registry
name: litestar-stores-registry
category: computing-software
field: web-development
product: litestar
tags: [litestar, stores, store, namespace, redisstore, memorystore, filestore, store-registry]
level: practitioner
status: docs-checked
description: "Use Litestar key/value stores (Memory, File, Redis, Valkey), expiry, namespacing and the StoreRegistry to share and configure stores across caching, sessions and rate limits."
sources: [https://docs.litestar.dev/latest/usage/stores.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar stores and the store registry

Goal: pick a store backend, set expiry and namespaces, and wire stores into integrations.

## Method

1. Built-in stores (all async, `get`/`set`/`delete`):
   - `MemoryStore` (`litestar.stores.memory`): dictionary, no persistence, not thread or multiprocess safe, lowest overhead, the default store used internally. Do not rely on it when multiple worker processes must share data.
   - `FileStore` (`litestar.stores.file`): files on disk, persistent, slower, supports namespacing.
   - `RedisStore` (`litestar.stores.redis`) and `ValkeyStore`: support namespacing. Memcached is not supported.
2. Values are bytes: `await store.set("key", b"value")`; `get` returns bytes (strings passed to `set` are UTF-8 encoded) or `None` when missing.
3. Expiry: `await store.set("foo", b"bar", expires_in=1)`. Renew on read with `await store.get("foo", renew_for=1)`.
4. `MemoryStore` and `FileStore` do not delete expired data automatically; it happens on access or via `delete_expired()`. Call it periodically (the page uses an `after_response` handler at most every 30 seconds; a `FileStore` may also do it on startup). Redis uses native expiry.
5. Namespacing: `root_store = RedisStore.with_client()`, `cache_store = root_store.with_namespace("cache")`. Operations on a namespaced store affect only itself and children, so `cache_store.delete_all()` leaves `sessions` alone. `RedisStore` uses the `LITESTAR` namespace by default; pass `namespace=None` to turn that off.
6. Registry: `Litestar([], stores={"memory": MemoryStore()})`, then `app.stores.get("memory")`. An unregistered name creates a store through the default factory (a new `MemoryStore` by default) and returns the same instance on later calls.
7. Custom default: `Litestar([], stores=StoreRegistry(default_factory=default_factory))` with `default_factory(name: str)`.
8. Integrations pick stores by name. Defaults: `sessions` and `response_cache`; rate limiting requests its store via `app.stores.get`. Example: `stores={"redis": RedisStore.with_client(), "file": FileStore(Path("data"))}`, `ResponseCacheConfig(store="redis")`, `ServerSideSessionConfig(store="file").middleware`, `RateLimitConfig(rate_limit=("second", 10), store="redis").middleware`.

## Gotchas

- Stores may not be closed at shutdown; with `RedisStore` and your own Redis instance (not `RedisStore.with_client`) you must close it yourself.

## Verify

Per the page, a key stored with `expires_in=1` returns `None` from `get` after one second.

## Checked

2026-11-07. Read the full cited page(s) (usage/stores.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
