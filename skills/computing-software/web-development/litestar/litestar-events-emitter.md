---
id: computing-software.web-development.litestar.litestar-events-emitter
name: litestar-events-emitter
category: computing-software
field: web-development
product: litestar
tags: [litestar, events, event-emitter, listener, emit, async, non-blocking]
level: practitioner
status: docs-checked
description: "Use Litestar's event emitter and listener pattern: define listeners, emit events from handlers, listen to several events, and match listener arguments."
sources: [https://docs.litestar.dev/latest/usage/events.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar events: emitter and listeners

Goal: run side effects (emails, notifications) without blocking the response.

## Method

- Decorate an async function with `@listener("event_id")` from `litestar.events` and register it via `Litestar(listeners=[...])`.
- Emit from a handler with `request.app.emit("event_id", ...)`.

```python
@listener("user_created")
async def send_welcome_email_handler(email: str) -> None:
    await send_welcome_mail(email)


@post("/users")
async def create_user_handler(data: JSONBody[UserDTO], request: Request) -> None:
    await user_repository.insert(data)
    request.app.emit("user_created", email=data.email)


app = Litestar(
    route_handlers=[create_user_handler], listeners=[send_welcome_email_handler]
)
```

- One listener, several events: `@listener("user_created", "password_changed")`.
- Several listeners can subscribe to the same event (e.g. two `@listener("user_deleted")` functions).
- `emit` signature: `def emit(self, event_id: str, *args: Any, **kwargs: Any) -> None`.

## Gotchas

- Every listener of an event receives all args and kwargs passed to `emit`. If two listeners of `user_deleted` are `(email: str)` and `(reason: str)` and you emit `email=..., reason=...`, an exception is raised. Give each listener `**kwargs`:

```python
@listener("user_deleted")
async def send_farewell_email_handler(email: str, **kwargs) -> None: ...


@listener("user_deleted")
async def notify_customer_support(reason: str, **kwargs) -> None: ...
```

- The default backend is `SimpleEventEmitter`, an in-memory async queue. It has no retry, persistence or scheduling; for those, implement your own backend (subclass `BaseEventEmitterBackend`, implement `emit`, `__aenter__`, `__aexit__`) on a DB/key store such as Redis or Postgres, or a message broker or job queue.

## Verify

After a POST to `/users` in the example, the response returns without waiting for the email and the listener runs on its own async block.

## Checked

2026-11-07. Read the full cited page(s) (usage/events.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
