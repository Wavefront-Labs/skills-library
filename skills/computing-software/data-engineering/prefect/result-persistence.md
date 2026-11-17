---
id: computing-software.data-engineering.prefect.result-persistence
name: result-persistence
category: computing-software
field: data-engineering
product: prefect
tags: [results, persist-result, serializer, result-storage, resultstore]
level: advanced
status: docs-checked
description: "Persist Prefect results with persist_result, result_storage, result_serializer and result_storage_key, global settings, precedence and ephemeral storage caveats."
sources:
  - https://docs.prefect.io/v3/advanced/results
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: persist task and flow return values deliberately.

Keywords on `@task` or `@flow` (any non-null value enables persistence): `persist_result`, `result_storage` (saved block instance or `"block-type-slug/block-name"`), `result_serializer`, `result_storage_key` (for example `"hello-{parameters[name]}.pickle"`). If both `result_storage_key` and `cache_key_fn` are set, only the key is used. Flow-level settings cascade to tasks; explicit task settings win.

Settings: `PREFECT_RESULTS_PERSIST_BY_DEFAULT`, `PREFECT_TASKS_DEFAULT_PERSIST_RESULT`, `PREFECT_RESULTS_DEFAULT_STORAGE_BLOCK`, `PREFECT_RESULTS_LOCAL_STORAGE_PATH` (default `~/.prefect/storage/`), `PREFECT_RESULTS_DEFAULT_SERIALIZER` (default `pickle`; built-ins `pickle`, `json`, `compressed/pickle`, `compressed/json`).

Server-side default storage (beta): `prefect experimental result-storage set | inspect | clear`. A local `PREFECT_RESULTS_DEFAULT_STORAGE_BLOCK` overrides it.

Filenames: task results use a hash of the cache policy unless `result_storage_key` is set; flow results use a random UUID.

Caveats:
- Local default storage does not persist across runs on ephemeral infrastructure such as Kubernetes or Docker; use a remote block or shared volume.
- A custom serializer must be importable wherever results are read, or `read` raises `RuntimeError`.
- `ResultStore` needs an explicit `result_storage`.
- `cache_result_in_memory=False` drops a result from memory after commit.

```python
from prefect.results import ResultStore
store = ResultStore(result_storage=block)
record = store.read(key="my-result")
```

## Checked

2026-11-08. Persistence keywords and settings, local storage default, serializer defaults and options, server-side default (beta) commands, filenames, ephemeral-infrastructure caveat, RuntimeError note and ResultStore usage confirmed against the full results page.

Method: documentation only; no commands were run.
