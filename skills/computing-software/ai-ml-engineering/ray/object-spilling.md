---
id: computing-software.ai-ml-engineering.ray.object-spilling
name: object-spilling
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, object-spilling, spill-to-disk, object-store-full, object-spilling-directory]
level: practitioner
status: docs-checked
description: "Configure Ray object spilling to disk when the object store fills: spill directory, store size, spill statistics and diagnosing ObjectStoreFullError."
sources:
  - https://docs.ray.io/en/latest/ray-core/objects/object-spilling.html
  - https://docs.ray.io/en/latest/ray-core/scheduling/memory-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object spilling

Ray spills objects to a directory on the local filesystem once the object store is full. By default the directory is under the temporary directory (a `/tmp/ray/session_...` folder).

Each node's object store defaults to 30% of its available memory, capped at 200 GB and, on Linux, at 95% of the size of `/dev/shm`. Override the size with `object_store_memory` (bytes) or the env vars `RAY_DEFAULT_OBJECT_STORE_MEMORY_PROPORTION` and `RAY_DEFAULT_OBJECT_STORE_MAX_MEMORY_BYTES`, which must be set on every node before Ray starts.

```python
import ray
ray.init(object_spilling_directory="/path/to/spill/dir",   # where spilled objects go
         object_store_memory=8 * 1024**3)                   # bytes
```

```bash
ray start --head --object-spilling-directory=/path/to/spill/dir --object-store-memory=8000000000
```

The Ray docs leave advanced spilling customisation to the Ray team; this skill covers only the directory option.

## Statistics

The raylet logs `Spilled ... MiB` / `Restored ... MiB` lines at INFO level (for example in `raylet.out` under the session logs). Cluster-wide totals: `ray memory`, or `ray memory --stats-only` for just the stats.

## Gotchas
- Spilling is a safety valve: restoring objects from disk slows tasks, so release references and stream data where you can.
- `ObjectStoreFullError` can come from object refs that are still in scope; use `ray memory` to find which references pin objects (see object-references-and-memory).
- If `--object-store-memory` is larger than `/dev/shm`, Ray writes the plasma store to disk instead, which can cause significant performance problems; in Docker, size `/dev/shm` with `--shm-size` (Ray's cluster launcher sets it unless `docker.disable_shm_size_detection` is true).

## Verify
`ray memory --stats-only` shows non-zero `Spilled` bytes after the store fills, and files appear in the spill directory.

## Checked
2026-11-03: checked against the Ray docs source `core/objects/object-spilling.md`, `core/scheduling/memory-management.md`, `cluster/vms/user-guides/large-cluster-best-practices.md`, `cluster/vms/references/ray-cluster-configuration.md` and the `ray.init` docstring in `python/ray/_private/worker.py`. Removed the `object_spilling_config` JSON, `local_fs_capacity_threshold`, `smart_open`/S3 and `buffer_size` settings, which the current docs do not document, and the unsourced `ObjectStoreFullError` disk-full claim.
Method: documentation only; no commands were run.
