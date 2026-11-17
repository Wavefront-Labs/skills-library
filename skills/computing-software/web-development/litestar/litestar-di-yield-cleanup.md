---
id: computing-software.web-development.litestar.litestar-di-yield-cleanup
name: litestar-di-yield-cleanup
category: computing-software
field: web-development
product: litestar
tags: [litestar, dependency-injection, yield, cleanup, generator, exceptions, provide, try-finally]
level: practitioner
status: docs-checked
description: "Write Litestar generator dependencies that clean up after the handler, react to handler exceptions, and avoid re-raising."
sources: [https://docs.litestar.dev/latest/usage/dependency-injection.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar yield dependencies and cleanup

Goal: run teardown (close a connection, roll back or commit) after a handler returns.

## Method

A dependency may be a sync or async generator function. Code after `yield` is the cleanup step; it runs after the handler returns but before the response is sent (HTTP).

```python
STATE = {"result": None, "connection": "closed"}

def generator_function() -> Generator[str, None, None]:
    try:
        STATE["connection"] = "open"
        yield "hello"
        STATE["result"] = "OK"
    except ValueError:
        STATE["result"] = "error"
    finally:
        STATE["connection"] = "closed"

@get("/{name:str}", dependencies={"message": Provide(generator_function)})
def index(name: FromPath[str], message: NamedDependency[str]) -> dict[str, str]:
    if name == "John":
        return {name: message}
    raise ValueError()
```

- An exception in the handler is raised inside the generator at the point where it first yielded. This lets the dependency branch on success versus error, for example rolling back a database session on error and committing otherwise.
- Always wrap `yield` in `try` / `finally` so cleanup runs even on exceptions.

## Gotchas

- Do not re-raise exceptions inside the dependency; exceptions caught there are still handled by the normal mechanisms.
- Exceptions raised during cleanup are re-raised in an `ExceptionGroup` (the `exceptiongroup` package is used on Python below 3.11). This happens after all dependencies have been cleaned up, so one failing cleanup does not stop the others.

## Verify

Using `TestClient` as in the page:

```python
with TestClient(app=app) as client:
    client.get("/John").json()   # {"John": "hello"}; STATE == {"result": "OK", "connection": "closed"}
    client.get("/Peter")         # status 500; STATE == {"result": "error", "connection": "closed"}
```

## Checked

2026-11-07. Read the full cited page(s) (usage/dependency-injection.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
