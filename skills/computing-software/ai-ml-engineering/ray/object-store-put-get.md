---
id: computing-software.ai-ml-engineering.ray.object-store-put-get
name: object-store-put-get
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-put, object-store, plasma, zero-copy]
level: practitioner
status: docs-checked
description: "Share data via the Ray object store with ray.put/ray.get, zero-copy numpy reads, serialization limits and passing ObjectRefs to tasks."
sources:
  - https://docs.ray.io/en/latest/ray-core/objects.html
  - https://docs.ray.io/en/latest/ray-core/objects/serialization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object store put and get

```python
import numpy as np, ray
ray.init()
big = np.zeros((10_000, 10_000), dtype=np.float32)   # ~400 MB
ref = ray.put(big)                                   # one copy into shared memory

@ray.remote
def total(a): return float(a.sum())                  # a is a read-only zero-copy view

ray.get([total.remote(ref) for _ in range(8)])       # no per-task copy of big
x = ray.get(ref)                                      # numpy arrays come back zero-copy, read-only
x.flags.writeable                                     # False
```

## Gotchas
- Zero-copy applies to NumPy arrays and collections of them; other objects are deserialized into Python objects.
- Modifying a zero-copy array raises `ValueError: assignment destination is read-only`; call `.copy()` first.
- An argument over 100 KB passed by value is stored implicitly for each call and Ray does not deduplicate; use one `ray.put`.
- Objects are immutable and reference-counted; keep the `ObjectRef` alive while tasks need it.
- Ray uses Pickle protocol 5 with cloudpickle (lambdas, nested functions, dynamic classes); lock objects are mostly unserializable.
- `ray.get(ref, timeout=...)` raises `GetTimeoutError` (a subclass of `TimeoutError`).

## Verify
`ray memory` lists the object and its references; `x.flags.writeable` is `False` for a NumPy array from `ray.get`.

## Checked
2026-11-03: checked against the Ray docs source `core/objects/index.md`, `core/objects/serialization.md`, `core/patterns/pass-large-arg-by-value.md` and `core/scheduling/memory-management.md`. Removed the unsourced Arrow zero-copy, submit-time pickling and per-task memory claims.
Method: documentation only; no commands were run.
