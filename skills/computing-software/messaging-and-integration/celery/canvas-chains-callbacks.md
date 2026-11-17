---
id: computing-software.messaging-and-integration.celery.canvas-chains-callbacks
name: canvas-chains-callbacks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, canvas, chain, callbacks, errback, link, link-error, celery-canvas-chains]
level: practitioner
status: docs-checked
description: "Link Celery tasks with link, on_error and chain, read intermediate results via parent and children, and understand the task id a chain inherits."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run tasks in sequence, pass each result forward, handle errors, and read intermediate results.

## Callbacks with link

```python
add.apply_async((2, 2), link=other_task.s())
res = add.apply_async((2, 2), link=mul.s(16))   # mul(4, 16)
```

The callback runs only if the parent exited successfully, receiving the parent's return value as the first argument (partial args follow it). `add.apply_async((2, 2), link=add.s(8))` computes 2+2, then 4+8.

Inspect with `res.children` and `res.children[0].get()`. `res.collect()` iterates `(AsyncResult, value)` pairs and raises `IncompleteStream` if the graph is not fully formed; use `res.collect(intermediate=True)` to iterate anyway. Signatures link too: `s.link(mul.s(4))`, `s.link(log_result.s())`.

## Error callbacks

```python
add.s(2, 2).on_error(log_error.s()).delay()
# same as add.apply_async((2, 2), link_error=log_error.s())

@app.task
def log_error(request, exc, traceback):
    ...
```

The worker does not call the errback as a task; it calls the function directly, passing the raw request, exception and traceback.

## chain

```python
from celery import chain
res = chain(add.s(4, 4), mul.s(8), mul.s(10))()   # (4+4)*8*10
res.get()                # 640
res.parent.get()         # 64
res.parent.parent.get()  # 8
(add.s(2, 2) | mul.s(8) | mul.s(10)).apply_async()   # pipe form
```

Calling a chain sends the first task to the broker and returns an `AsyncResult` for the last task. Chains can be partial: `c1 = (add.s(4) | mul.s(8)); c1(16)` gives 160. Chains nest: `add.s(4, 16) | mul.s(2) | (add.s(4) | mul.s(8))` gives 352. Use `.si()` to build a chain of independent tasks: `(add.si(2, 2) | add.si(4, 4) | add.si(8, 8))()` gives `res.get()` of 16 (the last task's own result), with `res.parent.get()` 8 and `res.parent.parent.get()` 4.

Since 5.4 a chain inherits the task id of the last task. The graph is available as `res.parent.parent.graph` (a `DependencyGraph`); `graph.to_dot(fh)` writes dot format, then `dot -Tpng graph.dot -o graph.png`.

## Warning

For complex workflows the default JSON serializer has been observed to inflate message sizes drastically through recursive references; pickle is not vulnerable and may be preferable.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/canvas.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: clarified what a chain of immutable signatures returns.

Method: documentation only; no commands were run.
