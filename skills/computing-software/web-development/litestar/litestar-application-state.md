---
id: computing-software.web-development.litestar.litestar-application-state
name: litestar-application-state
category: computing-software
field: web-development
product: litestar
tags: [litestar, app-state, state, immutable-state, dependency-injection, handlers, middleware]
level: practitioner
status: docs-checked
description: "Seed and use Litestar application State, inject it into handlers and dependencies, and lock it down with ImmutableState."
sources: [https://docs.litestar.dev/latest/usage/applications.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar application state

Goal: share contextual data across the app through `app.state`.

## Method

- `app.state` is a `litestar.datastructures.State`, reachable wherever the app is. The app is put in the ASGI scope as `scope["litestar_app"]`; get it with `Litestar.from_scope(scope)` (middleware) or `request.app` / `socket.app`.
- Seed it by passing a `State` to the constructor. `State` accepts a dict, a `State`/`ImmutableState` instance, or a list of key/value tuples. Set `deep_copy=True` on `State` to deep copy the initial data and prevent outside mutation.

```python
@get("/", sync_to_thread=False)
def handler(state: State) -> dict[str, Any]:
    return state.dict()


app = Litestar(route_handlers=[handler], state=State({"count": 100}))
```

- Inject by naming a `state` kwarg (a reserved keyword argument) in a handler or dependency, typed `State`. The annotation is not just for type checkers: Litestar instantiates a new state instance of the class you give, so custom classes work.
- Startup/shutdown hooks receive `app` and can set `app.state.value = "abc123"`.
- For read-only state, annotate with `ImmutableState`; setting an attribute raises `AttributeError`.

```python
@get("/", sync_to_thread=False)
def handler(state: ImmutableState) -> dict[str, Any]:
    setattr(state, "count", 1)  # raises AttributeError
    return state.dict()
```

## Gotchas

- The docs warn that state can make code hard to reason about because changes happen in different ASGI contexts; use it sparingly.

## Verify

The `State({"count": 100})` handler above returns `{"count": 100}`; the ImmutableState handler raises AttributeError on assignment.

## Checked

2026-11-07. Read the full cited page(s) (usage/applications.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
