---
id: computing-software.messaging-and-integration.celery.canvas-signatures-partials
name: canvas-signatures-partials
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, canvas, signature, partials, immutable, celery-canvas-signatures, apply-async]
level: practitioner
status: docs-checked
description: "Create Celery signatures with s, si and signature, add partial args, set options, clone, and make immutable signatures so callbacks ignore parent results."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: wrap a task invocation (args, kwargs, options) in a signature you can pass around, serialize, extend as a partial, or freeze as immutable.

## Create

```python
from celery import signature
signature('tasks.add', args=(2, 2), countdown=10)   # by name
add.signature((2, 2), countdown=10)                 # via the task
add.s(2, 2)                                         # star-args shortcut
add.s(2, 2, debug=True)                             # kwargs ok
```

Inspect with `s.args`, `s.kwargs`, `s.options`. Calling `add.s(2, 2)()` runs the task inline in the current process and returns `4`; `.delay()` and `.apply_async()` send it to a worker.

## Options

You can't pass options directly to `delay`, and `.s()` takes none. Set them at creation or chain `set`:

```python
add.signature((2, 2), countdown=1).delay()
add.signature((2, 2)).set(countdown=1).delay()
add.s(2, 2).set(countdown=1)
```

## Partials

Extra args given to `delay`/`apply_async` are **prepended** to the signature args:

```python
partial = add.s(2)        # incomplete
partial.delay(4)          # 4 + 2
subtract.s(10).delay(30)  # subtract(30, 10) = 20, not subtract(10, 30)
```

Extra kwargs are merged in with the new ones taking precedence (`s.delay(debug=True)` gives `add(2, 2, debug=True)`). Extra options are merged too, new taking precedence (`add.signature((2, 2), countdown=10).apply_async(countdown=1)` gives countdown 1).

Derive a copy with `clone`:

```python
s = add.s(2)
s.clone(args=(4,), kwargs={'debug': True})   # add(4, 2, debug=True)
```

## Immutable

Linked tasks and chord callbacks normally receive the parent result. When a callback should take no extra arguments, make it immutable:

```python
add.apply_async((2, 2), link=reset_buffers.signature(immutable=True))
add.apply_async((2, 2), link=reset_buffers.si())   # preferred shortcut
```

Only execution options can be set on an immutable signature; partial args/kwargs are not possible.

## Shell shortcut

`~sig` is the same as `sig.apply_async().get()`. The page says you probably should not use it in production code.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/canvas.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
