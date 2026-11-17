---
id: computing-software.messaging-and-integration.celery.canvas-map-starmap-chunks
name: canvas-map-starmap-chunks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, canvas, map, starmap, chunks, skew, batching, celery-canvas-map-chunks]
level: practitioner
status: docs-checked
description: "Use Celery map, starmap and chunks to process an iterable with fewer messages, convert chunks to a group, and skew countdowns."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply one task to many items without sending one message per item.

## map and starmap

Built-in tasks that call the task for each element. Unlike `group`, only one task message is sent and the operation is sequential.

```python
~tsum.map([list(range(10)), list(range(100))])   # [45, 4950]
~add.starmap(zip(range(10), range(10)))          # [0, 2, 4, ..., 18]
```

`map` is equivalent to a task doing `[tsum(range(10)), tsum(range(100))]`; `starmap` over argument pairs from `zip(...)` is like `[add(i, i) for i in range(10)]`. Both are signatures, so they combine with groups and take options:

```python
add.starmap(zip(range(10), range(10))).apply_async(countdown=10)
```

(`~sig` is the same as `sig.apply_async().get()`.)

## chunks

Chunking splits an iterable into parts, e.g. one million objects into 10 tasks of a hundred thousand. The page says the parallelism loss is rarely real on a busy cluster and avoiding message overhead can considerably raise performance.

```python
add.chunks(zip(range(100), range(100)), 10)        # signature; 10 items per task
res = add.chunks(zip(range(100), range(100)), 10)()
res.get()    # list of 10 lists of 10 results
```

Calling the chunks signature sends the chunk messages from the current process (like `group`). `.apply_async()` instead creates a dedicated task so the individual tasks are applied in a worker:

```python
add.chunks(zip(range(100), range(100)), 10).apply_async()
```

Convert to a group and stagger start times with `skew`:

```python
group = add.chunks(zip(range(100), range(100)), 10).group()
group.skew(start=1, stop=10)()
```

The first task then has a countdown of one second, the second two seconds, and so on.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/canvas.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: an unsupported 1000-item chunks example; reworded the starmap argument sentence.

Method: documentation only; no commands were run.
