---
id: computing-software.data-engineering.prefect.task-caching-policies
name: task-caching-policies
category: computing-software
field: data-engineering
product: prefect
tags: [caching, cache-policy, cache-key, cache-expiration, isolation-level]
level: practitioner
status: docs-checked
description: "Configure Prefect task caching with cache policies, custom cache key functions, expiration, key storage and isolation levels."
sources:
  - https://docs.prefect.io/v3/concepts/caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make tasks reuse stored results safely.

A cached run enters `Completed` and returns the stored value without executing. Caching needs result persistence, which is off by default: `prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true`. `persist_result=False` on a task disables its caching. Default local storage is `~/.prefect/storage/`, filenames match cache keys.

Policies (`@task(cache_policy=...)`, from `prefect.cache_policies`):
- `DEFAULT`: inputs, code definition and flow run ID
- `INPUTS`: inputs only
- `TASK_SOURCE`: the task's own source lines
- `FLOW_PARAMETERS`: parent flow parameter values
- `NO_CACHE`: no caching or persistence

Add policies together (`TASK_SOURCE + INPUTS`); `INPUTS - 'debug'` excludes a named input from the key.

Expiry: `cache_expiration=timedelta(...)`, stored with the result record.

Custom key: `cache_key_fn(context, parameters) -> str`, where context is a `TaskRunContext` (`task_run_id`, `flow_run_id`, `task`) and parameters a dict keyed by name.

Record storage: `.configure(key_storage=...)` on a policy takes a directory path or storage block.

Isolation via `.configure`: `READ_COMMITTED` (default; same task may run concurrently) or `SERIALIZABLE` (one execution per record, needs a `lock_manager`). Lock managers: `MemoryLockManager` (threads), `FileSystemLockManager` (one machine), `RedisLockManager` (multiple machines).

## Checked

2026-11-08. Persistence requirement and setting, default storage path, the five policies, policy addition and input subtraction, cache_expiration, cache_key_fn arguments, key_storage, isolation levels and lock managers confirmed against the Caching page.

Method: documentation only; no commands were run.
