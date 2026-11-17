---
id: computing-software.software-engineering.python.tuning-the-garbage-collector-with-gc
name: tuning-the-garbage-collector-with-gc
category: computing-software
field: software-engineering
product: python
tags: [python, py-memory, garbage-collector-tuning, gc, reference-cycles, gc-freeze, gc-collect, memory-leaks, generations]
level: advanced
status: docs-checked
description: "Find and fix reference cycles and GC pauses with the gc module: thresholds, gc.freeze before fork, DEBUG_SAVEALL and the 3.14 threshold change."
sources: ["https://docs.python.org/3/library/gc.html", "https://docs.python.org/3/library/gc.html#gc.freeze"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuning the garbage collector with gc

CPython frees most objects immediately by reference counting. The cyclic GC only exists for **reference cycles** (A -> B -> A) and container objects.

```python
import gc
gc.get_threshold()              # (threshold0, threshold1, threshold2)
gc.get_stats(); gc.get_count()
gc.collect()                    # full collection now; returns unreachable object count
gc.disable(); ...; gc.enable()  # only when you control allocation bursts, and never forever
gc.freeze()                     # move all current objects to a permanent generation: ignored by GC
```

## Common recipes
- **Processes that `fork()` without `exec()`**: the docs recommend `gc.disable()` early in the parent, `gc.freeze()` right before `fork()`, and `gc.enable()` early in the children. This avoids freed "holes" in memory pages and stops child collections touching the `gc_refs` counter of long-lived parent objects, maximising copy-on-write sharing.
- **Batch jobs creating many long-lived containers**: raising the gen0 threshold (`gc.set_threshold(50_000, 20, 20)`) or `gc.disable()` plus a manual `gc.collect()` between batches may help; measure first.
- **Latency-sensitive paths**: `gc.disable()` at request start and `gc.collect(0)` after is possible; measure first.

## Version notes
- The collector uses three generations (0 to 2); a generation is examined once the previous one has been examined more than its threshold times.
- Python 3.14: `set_threshold`'s *threshold2* is ignored, and `gc.collect(1)` performs an increment of collection; both changed again in 3.14.5 (*threshold2* restored, `generation=1` collects the middle generation).
- Re-measure after upgrading and do not copy thresholds across versions.

## Finding leaks and cycles
```python
gc.set_debug(gc.DEBUG_SAVEALL)      # keep unreachable objects in gc.garbage for inspection
gc.collect(); print(len(gc.garbage), gc.garbage[:3])
```
Break cycles with `weakref` links where one side can be weak.

## Gotchas
- Since 3.4 (PEP 442) objects with `__del__` no longer end up in `gc.garbage`; it should be empty except for C extension types with a non-NULL `tp_del`.
- `gc.collect()` while a collection is already running has undefined effect.
- Do not call `gc.collect()` in a loop to "fix" memory use; find the cycle.

## Verify
- [ ] Before/after numbers: p99 latency or RSS with a documented workload and Python version.

## Checked

- 2026-11-03: checked against the CPython docs `library/gc.rst`: `collect`, `set_threshold`/`get_threshold`, `freeze` fork recipe, `DEBUG_SAVEALL` and `garbage`, PEP 442 note, 3.14 and 3.14.5 changes.
- Removed: the (700, 10, 10) default, the 3.13 incremental-GC and 3.14 two-generation descriptions, free-threaded collector remark, objgraph and tracemalloc recipes, cycle-maker list, allocator/RSS remark.

Method: documentation only; no commands were run.
- [ ] `gc.garbage` stays empty in production, and a unit test checks that closing the object releases it (`weakref.ref(obj)()` is `None` after `del` + `gc.collect()`).
