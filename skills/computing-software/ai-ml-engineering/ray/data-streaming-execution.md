---
id: computing-software.ai-ml-engineering.ray.data-streaming-execution
name: data-streaming-execution
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, streaming-execution, ray-data-memory, backpressure-policy, execution-options]
level: practitioner
status: docs-checked
description: "Tune Ray Data streaming execution: ExecutionOptions resource_limits, preserve_order, block size, object store spilling and ds.stats()."
sources:
  - https://docs.ray.io/en/latest/data/performance-tips.html
  - https://docs.ray.io/en/latest/data/execution-configurations.html
  - https://docs.ray.io/en/latest/data/key-concepts.html
  - https://docs.ray.io/en/latest/data/data-internals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming execution and memory

Ray Data is lazy: nothing runs until you consume or materialize the dataset, then operators run pipelined in a streaming fashion and can scale independently.

```python
import ray
ctx = ray.data.DataContext.get_current()
ctx.execution_options.resource_limits = ctx.execution_options.resource_limits.copy(
    cpu=10, gpu=5, object_store_memory=10e9)
ctx.execution_options.preserve_order = True         # deterministic block order, may be slower
ctx.target_max_block_size = 128 * 1024 * 1024       # bytes; also target_min_block_size
```

## Facts from the docs
- `resource_limits` is a soft limit, auto-detected by default: CPU and GPU limits equal the cluster size and the object store limit is half the total object store. Lower it when running several jobs on a cluster or when loading training data (the docs suggest e.g. 2 GB).
- `preserve_order` is off by default; turning it on preserves block order and may reduce performance.
- Blocks are bounded between 1 MiB and 128 MiB by default (`target_min_block_size`, `target_max_block_size`). Check with `ds.stats()` that each operator's output blocks are at least 1 MB, ideally over 100 MB; use `repartition(n)` for exact block counts (an all-to-all op that materializes all blocks in memory).
- Spilling to disk is expected when the dataset exceeds object store capacity and you run an all-to-all shuffle or call `ds.materialize()`. Otherwise raise the number of read output blocks (`override_num_blocks`) or make each task read less.
- Shuffle during iteration with `local_shuffle_buffer_size` in `iter_batches`; `random_shuffle` is slow because it shuffles all rows.
- `ds.stats()` reports per-operator information; the iteration breakdown includes `In batch formatting`.

## Verify
After a run, `print(ds.stats())` (on a materialized or consumed dataset) shows per-operator output block sizes.

## Checked
2026-11-03. Confirmed in Ray repo docs `data/performance-tips.md`, `execution-configurations.md`, `key-concepts.md`, `internals.md`, `shuffling-data.md`, `iterating-over-data.md`. Removed: `resource_limits.cpu = 32` direct assignment and `object_store_memory` GiB example, `preserve_order = False` as an optimisation, `prefetch_batches` snippet, actor placement `num_cpus=1` claim, explode block-size advice, "confirm attribute name" marker (attribute is documented).
Method: documentation only; no commands were run.
