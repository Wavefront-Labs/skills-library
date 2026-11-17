---
id: computing-software.web-development.litestar.litestar-application-hooks
name: litestar-application-hooks
category: computing-software
field: web-development
product: litestar
tags: [litestar, application-hooks, on-app-init, before-send, after-exception, app-config, observability]
level: practitioner
status: docs-checked
description: "Use Litestar application hooks after_exception, before_send and on_app_init to observe errors, modify ASGI messages and share app configuration."
sources: [https://docs.litestar.dev/latest/usage/applications.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar application hooks

Goal: instrument the app (monitoring, tracing, logging) with app-level hooks.

## Method

Each hook kwarg on `Litestar` takes one sync or async callable or a list; lists are called in the order given.

- `after_exception`: called with `(exc, scope)` after an exception occurs.

```python
async def after_exception_handler(exc: Exception, scope: "Scope") -> None:
    state = Litestar.from_scope(scope).state
    ...

app = Litestar([my_handler], after_exception=[after_exception_handler])
```

- `before_send`: called on every ASGI message sent, with `(message, scope)`. Because it fires for each message, filter on type, e.g. only `http.response.start`:

```python
async def before_send_hook_handler(message: Message, scope: Scope) -> None:
    if message["type"] == "http.response.start":
        headers = MutableScopeHeaders.from_message(message=message)
        headers["My-Header"] = Litestar.from_scope(scope).state.message

app = Litestar(route_handlers=[handler], on_startup=[on_startup], before_send=[before_send_hook_handler])
```

- `on_app_init`: each handler receives the `AppConfig` before the app is built and must return an `AppConfig`. Use it for shared configuration across apps or third-party config systems.

```python
def receive_app_config(app_config: "AppConfig") -> "AppConfig":
    app_config.on_shutdown.append(close_db_connection)
    return app_config

app = Litestar([], on_app_init=[receive_app_config])
```

## Gotchas

- `after_exception` only receives exceptions for side effects; it does not handle them. Use exception handlers to handle.
- `on_app_init` handlers cannot be async: they run inside `Litestar.__init__`, outside an async context.

## Verify

In the after_exception example, a request to a handler raising `HTTPException(status_code=400)` triggers the hook, which logs the exception type and path.

## Checked

2026-11-07. Read the full cited page(s) (usage/applications.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
