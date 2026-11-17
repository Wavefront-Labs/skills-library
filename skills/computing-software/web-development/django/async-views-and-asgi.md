---
id: computing-software.web-development.django.async-views-and-asgi
name: async-views-and-asgi
category: computing-software
field: web-development
product: django
tags: [django, django-async, asgi, async-views, uvicorn, sync-to-async, async-orm, python, web-development]
level: practitioner
status: gated
description: "Using async Django: async views, async ORM methods, sync_to_async boundaries, running under ASGI with uvicorn/daphne, and when async actually helps."
sources:
  - https://docs.djangoproject.com/en/stable/topics/async/
  - https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
  - https://docs.djangoproject.com/en/stable/topics/db/queries/#asynchronous-queries
  - https://www.uvicorn.org/deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async views and ASGI

**Goal:** use async where concurrency pays (outbound HTTP fan-out, streaming, long-polling) without accidental thread hopping.

## 1. When it helps
Async wins for I/O-bound views that wait on several external calls, SSE/streaming responses and many idle connections. Plain CRUD views gain little; the ORM still runs DB calls in a thread pool for most backends.

## 2. Async views
```python
import asyncio, httpx
async def dashboard(request):
    async with httpx.AsyncClient(timeout=5) as client:
        weather, rates = await asyncio.gather(client.get(W_URL), client.get(R_URL))
    orders = [o async for o in Order.objects.filter(user=request.user)[:10]]
    count = await Order.objects.filter(user=request.user).acount()
    obj = await Order.objects.aget(pk=1)
    return render(request, "dash.html", {...})
```
Async ORM API: `aget`, `acreate`, `acount`, `aexists`, `afirst`, `aupdate`, `adelete`, `async for` over querysets; model `asave`/`adelete`/`arefresh_from_db` (4.2+). Transactions (`atomic`) are not async (there is no `aatomic`; `transaction.atomic()` in async code raises `SynchronousOnlyOperation`) - wrap in `sync_to_async`.

## 3. Crossing the boundary
```python
from asgiref.sync import sync_to_async, async_to_sync
@sync_to_async
def charge(user_id): ...                       # sync code with ORM transactions / blocking libs
await charge(user.id)
```
Calling sync ORM directly in async code raises `SynchronousOnlyOperation`. `request.user` is lazy and sync: use `await request.auser()` (5.0+).

## 4. Run under ASGI
```bash
uvicorn project.asgi:application --workers 4 --host 0.0.0.0 --port 8000
gunicorn project.asgi:application -k uvicorn_worker.UvicornWorker -w 4   # uvicorn-worker package (gated: unconfirmed, source is paywalled or blocked)
daphne project.asgi:application                                           # Channels
```
Under WSGI, async views still work but each runs in its own one-off event loop per request - no concurrency gain. The gunicorn line above was not run: gunicorn imports `fcntl` and cannot start on Windows, so only the package name and worker path are unconfirmed. The uvicorn (`--workers 2`) and daphne lines were run and answered requests.

## 5. Avoid mixed-mode slowness
Every sync middleware in an async stack costs a thread switch per request. Keep the middleware stack async-capable (the Django built-ins checked all report `async_capable = True`: security, sessions, common, csrf, auth, messages, clickjacking, locale, cache, gzip, conditional-get, remote-user, broken-links).

## 6. Streaming
```python
async def events(request):
    async def gen():
        while True:
            yield f"data: {await next_event()}\n\n"
    return StreamingHttpResponse(gen(), content_type="text/event-stream")
```
Async iterators in `StreamingHttpResponse` are served natively under ASGI (4.2+); under WSGI Django consumes the whole iterator and emits a warning ("StreamingHttpResponse must consume asynchronous iterators..."). For WebSockets use Django Channels.

## 7. Connections
Persistent DB connections (`CONN_MAX_AGE`) behave differently in async contexts; Django 5.1 added native PostgreSQL connection pooling (`OPTIONS: {"pool": True}` with psycopg 3).

## Verify
- [ ] Load test: async fan-out view latency ~ slowest upstream, not their sum.
- [ ] No `SynchronousOnlyOperation` errors in logs.
- [ ] ASGI server is actually used in production (check process list / startup logs).

## Checked
Django 6.1.2 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets. Async checks used a file-backed SQLite database (in-memory SQLite does not share across the async thread pool).
- Run: `acreate`, `aget`, `acount`, `aexists`, `afirst`, `aupdate`, `adelete`, `async for` slicing, `asave`, `request.auser()` in an AsyncClient view; sync ORM and `transaction.atomic()` inside `async def` raised `SynchronousOnlyOperation`; `transaction.aatomic` does not exist; `sync_to_async` around an atomic block worked.
- Run: a view gathering three 0.3 s awaits took 0.30 s; an async generator in `StreamingHttpResponse` streamed three chunks under AsyncClient.
- Run: `uvicorn asgi:application --workers 2` and `daphne asgi:application` served a 404 on localhost (processes stopped afterwards).
- Fetched: 4.1 and 4.2 and 5.0 and 5.1 release notes (async iterators 4.2, model async methods 4.2, `auser` 5.0, PostgreSQL `pool` option 5.1), topics/async.txt ("under a WSGI server, async views will run in their own, one-off event loop"). The PostgreSQL pool option was read from the release notes, not run (no PostgreSQL here).
- Not run: the gunicorn uvicorn-worker line (gunicorn needs `fcntl`); marked gated.
