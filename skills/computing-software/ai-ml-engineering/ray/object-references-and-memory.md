---
id: computing-software.ai-ml-engineering.ray.object-references-and-memory
name: object-references-and-memory
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-memory, object-ref-leak, reference-counting, ray-memory-debug]
level: practitioner
status: docs-checked
description: "Debug Ray object references and memory leaks with ray memory, reference types, ray.free and avoiding pinned objects in the driver."
sources:
  - https://docs.ray.io/en/latest/ray-core/scheduling/memory-management.html
  - https://docs.ray.io/en/latest/ray-core/objects.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object references and memory

```bash
ray memory                      # table of objects: size, reference type, call site
ray memory --stats-only
ray memory --group-by=STACK_TRACE --sort-by=OBJECT_SIZE   # find the line behind a leak; see ray memory --help
RAY_record_ref_creation_sites=1 ray start --head          # record call sites; set when the cluster starts
ray summary objects                                       # summarised by call site
```
Reference types in output: `LOCAL_REFERENCE` (held in your Python variables), `USED_BY_PENDING_TASK`, `CAPTURED_IN_OBJECT`, `PINNED_IN_MEMORY` (result of `ray.get` still in use). Actor handles are the fifth kind of reference that can pin an object.

```python
refs = [make.remote(i) for i in range(10_000)]
results = []
for r in refs:                  # holding all refs keeps all results alive
    results.append(ray.get(r))
del refs                        # drop refs so objects can be evicted
```

## Gotchas
- A numpy array from `ray.get` is a zero-copy view and pins the store object while it is alive; `del` the array to release.
- Any ref in scope in the cluster pins its object: local Python references, arguments to pending tasks and refs serialized inside other objects (`CAPTURED_IN_OBJECT`).
- An actor that stores a ref in a member variable keeps a `LOCAL_REFERENCE` after the task completes.
- `ray memory` output also gives object size, the process ID and IP where the reference was created, and the call site.

## Verify
After `del refs`, `ray memory` no longer lists those references.

## Checked
2026-11-03: checked against the Ray docs source `core/scheduling/memory-management.md` and `ray-observability/user-guides/cli-sdk.md`. Fixed: `RAY_record_ref_creation_sites` is set when the cluster starts. Removed the unsourced `ray.internal.free`, `ACTOR_HANDLE` and nested-list claims.
Method: documentation only; no commands were run.
