---
id: computing-software.software-engineering.python.async-generators-and-comprehensions
name: async-generators-and-comprehensions
category: computing-software
field: software-engineering
product: python
tags: [python, py-asyncio-adv, async-generators-comprehensions, async-for, aclosing, asyncgen, async-iterator]
level: practitioner
status: docs-checked
description: "Write async generators and async comprehensions, close them deterministically with contextlib.aclosing and avoid leaked generators on early break or cancellation."
sources: ["https://docs.python.org/3/reference/expressions.html#asynchronous-generator-functions", "https://docs.python.org/3/library/contextlib.html#contextlib.aclosing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async generators and comprehensions

```python
import asyncio
from contextlib import aclosing

async def ticker(n, delay=0.1):
    try:
        for i in range(n):
            yield i
            await asyncio.sleep(delay)
    finally:
        print("cleanup")           # runs on aclose(), but only if someone closes it

async def main():
    async with aclosing(ticker(100)) as gen:      # guarantees aclose() on break/exception
        async for i in gen:
            if i == 3: break

    evens = [i async for i in ticker(10, 0) if i % 2 == 0]    # async comprehension
    both = {k: v async for k, v in pairs()}                    # dict/set variants too
    results = [await f(x) for x in xs]                         # await in comprehension: sequential
    batch = await asyncio.gather(*(f(x) for x in xs))          # concurrent alternative

asyncio.run(main())
```

## Rules
- `async def` + `yield` makes an async generator (an async iterator): driven by `__anext__()`, `asend()` and `aclose()`.
- `await` or `async for` inside a comprehension makes it asynchronous; awaiting inside a plain list comprehension runs items one after another. Since 3.11 asynchronous comprehensions are allowed inside comprehensions in async functions.

## Gotchas
- Breaking out of `async for` does not close the generator immediately; an unfinished async generator is finalised through the finalizer registered with `sys.set_asyncgen_hooks()` (the event loop installs one), which calls `aclose()`, so cleanup is not deterministic. Wrap in `aclosing` or call `aclose()` explicitly.
- Avoid cancel scopes (`asyncio.timeout()`, task groups) that span a `yield` when the generator may be consumed from another task.

## Verify
- [ ] Test that breaking early still runs the `finally` block (use `aclosing`).

## Checked

2026-11-08. Confirmed on the Python reference (yield expressions, asynchronous generator functions and comprehensions) and the contextlib page: `async def` containing `yield` is an asynchronous generator function returning an asynchronous iterator, `__anext__()`/`asend()`/`aclose()`, finalizer registered via `sys.set_asyncgen_hooks()` that calls `aclose()`, `aclosing()` gives deterministic cleanup when a generator exits early by break or exception, the 3.11 change for nested asynchronous comprehensions. Removed: the `return value` restriction, `python -X dev`/debug-mode warnings, the "ignored GeneratorExit" message, sync-iteration and anyio remarks, and the specific cancel-wrong-task claim (not on the cited pages; the cancel-scope advice is kept as a caution only).

Method: docs-only read of cited pages, 2026-11-08
