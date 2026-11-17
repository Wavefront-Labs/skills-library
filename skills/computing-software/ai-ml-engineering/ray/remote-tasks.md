---
id: computing-software.ai-ml-engineering.ray.remote-tasks
name: remote-tasks
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-remote, remote-function, object-ref, ray-get]
level: practitioner
status: docs-checked
description: "Define Ray tasks with @ray.remote, launch with .remote(), fetch with ray.get, pass ObjectRefs between tasks, and avoid common pitfalls."
sources:
  - https://docs.ray.io/en/latest/ray-core/tasks.html
  - https://docs.ray.io/en/latest/ray-core/patterns/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote tasks

```python
import ray
ray.init()

@ray.remote
def square(x): return x * x

refs = [square.remote(i) for i in range(8)]     # non-blocking, returns ObjectRefs
print(ray.get(refs))                            # blocks, [0, 1, 4, ...]

@ray.remote
def add(a, b): return a + b
total = add.remote(square.remote(2), square.remote(3))   # refs as args: the value is passed to the second task once the first finishes
print(ray.get(total))                           # 13
```
Multiple returns: `@ray.remote(num_returns=2)`.

## Gotchas
- Calling `ray.get` in a loop (`for i: ray.get(f.remote(i))`) serializes everything; submit all, then get once.
- Parallelizing a function that runs quickly can be slower than the plain call because per-task overhead dominates; batch work inside each task.
- An argument over 100 KB passed by value is stored in the object store implicitly, and Ray does not deduplicate repeats; call `ray.put` once and pass the ref.
- Capturing objects of more than a few MB in a remote function's closure slows it or causes OOM; `ray.put` them and pass refs.

## Verify
Time `ray.get(refs)` against a sequential loop of the plain function; tasks that do real work should run faster in parallel.

## Checked
2026-11-03: checked against the Ray docs source `core/tasks/index.md`, `core/doc_code/tasks.py` and the patterns pages `pass-large-arg-by-value`, `closure-capture-large-objects`, `too-fine-grained-tasks`. Removed the unsourced per-task overhead figure, the TypeError claim and the speedup claim.
Method: documentation only; no commands were run.
