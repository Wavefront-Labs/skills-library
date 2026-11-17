---
id: computing-software.messaging-and-integration.celery.canvas-groups-results
name: canvas-groups-results
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, canvas, group, groupresult, parallel, unrolling, celery-canvas-chains]
level: practitioner
status: docs-checked
description: "Run Celery tasks in parallel with group, read GroupResult, avoid link and errback surprises on groups, and handle single-item group unrolling in chains."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: execute several signatures in parallel and track them as one result.

```python
from celery import group
g = group(add.s(2, 2), add.s(4, 4))
res = g()          # sends the messages from the current process
res.get()          # [4, 8]
group(add.s(i, i) for i in range(100))()   # iterators work
```

A group is itself a signature, so it combines with others. Tasks used in a group must not ignore their results, as for chords.

## GroupResult

`GroupResult` wraps a list of `AsyncResult` and behaves like one task:

- `successful()` True if all subtasks succeeded
- `failed()` True if any failed
- `waiting()` True if any is not ready
- `ready()` True if all are ready
- `completed_count()` number of successful subtasks
- `revoke()` revoke all
- `join()` gather results in call order, as a list

## Groups in a chain

Chaining a group with another task upgrades it to a chord: `group(add.s(i, i) for i in range(10)) | tsum.s()` gives 90. Within a chain the previous return value is forwarded to every task in the group. To stop that, make group members immutable: `add.s(4, 4) | group(add.si(i, i) for i in range(10))`.

## Callbacks and errbacks gotchas

Groups are not real tasks; linked signatures are passed down to each member. So `g.link(add.s())` does not receive the collected group result and does not wait for all tasks (in the page's example the callback ran in the background and raised because it got the wrong arguments). An errback linked with `g.link_error(log_error.s())` can run once per failing task. Make errbacks idempotent or counting; chords are the better tool where the backend supports them.

## Unrolling

A group with one signature is unrolled when chained, so the next task may get a single result or a list depending on group size:

```python
chain(add.s(2, 2), group(add.s(1)), add.s(1))
# add(2, 2) | add(1) | add(1)
chain(add.s(2, 2), group(add.s(1), add.s(2)), add.s(1))
# add(2, 2) | %add((add(1), add(2)), 1)
```

Make the following task accept either form. In Celery 4.x `chain(group(add.s(1, 1)), add.s(2))` wrongly became a chord; 5.x unrolls it to `add(1, 1) | add(2)`.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/canvas.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the inference that a result backend is required for groups.

Method: documentation only; no commands were run.
