---
id: computing-software.software-engineering.python.contextvars-for-request-context
name: contextvars-for-request-context
category: computing-software
field: software-engineering
product: python
tags: [python, py-asyncio-adv, contextvars, contextvar, request-id, logging-context, task-local, copy-context]
level: practitioner
status: docs-checked
description: "Carry request IDs, user or tracing context across await points with contextvars: ContextVar.set/reset tokens, copy_context and Context.run, and the module-level rule."
sources: ["https://docs.python.org/3/library/contextvars.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# contextvars for request context

The docs say context managers with state should use context variables instead of `threading.local()` so state does not bleed into other code in concurrent use. Context variables are natively supported in asyncio with no extra configuration.

```python
import contextvars

request_id = contextvars.ContextVar("request_id", default="-")   # module level, never in closures

async def handle(rid):
    token = request_id.set(rid)
    try:
        await work()                    # code called from here sees rid
    finally:
        request_id.reset(token)         # restore the value before the set()
```

## API facts
- `ContextVar(name, *, default=...)`: `get()` returns the value in the current context, else the `get(default)` argument, else the variable's default; otherwise it raises `LookupError`.
- The docs' important rule: create context variables at the top module level and never in closures, because `Context` objects hold strong references to variables, which prevents proper garbage collection.
- `set()` returns a `Token`. `reset(token)` restores the value from before that `set()`; a token cannot be used twice. `Token.old_value` is `Token.MISSING` if the variable was unset. Since 3.14 a token works as a context manager (`with var.set(x):`) and resets automatically.
- `copy_context()` returns a copy of the current context. `ctx.run(callable, *args, **kwargs)` runs it with that context current; changes the callable makes to variables stay in `ctx` and do not leak outside.
- `Context` is a mapping: `ctx[var]` (KeyError if unset), `ctx.get(var, default)`, `var in ctx`, `copy()` (shallow), iteration and `len`.
- Each thread has its own context stack, so `ContextVar` behaves like `threading.local()` for values assigned in different threads.
- In the docs' asyncio example, a server stores the client address in a context variable in the handler task and reads it in a function called from there without passing it explicitly.

## Gotchas
- Setting a value inside a `ctx.run()` callable does not change the caller's context; read the result from `ctx[var]`.
- Use immutable values or replace them with `.set()`, since a context copy is shallow.

## Verify
- [ ] A test runs two concurrent tasks with different IDs and asserts each reads its own value.

## Checked
Date: 2026-11-03. Confirmed against the `contextvars` documentation (ContextVar, Token, Context, copy_context, `run`, asyncio support note, 3.14 token context manager). Removed as not on that page: logging `Filter` example, `create_task`/`TaskGroup` copy semantics, `asyncio.to_thread()` and `run_in_executor` propagation, `ThreadPoolExecutor.submit`, `-X thread_inherit_context` details, `loop.call_soon(context=)`, generator context claim.
Method: documentation only; no commands were run.
