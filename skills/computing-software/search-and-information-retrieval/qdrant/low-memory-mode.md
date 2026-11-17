---
id: computing-software.search-and-information-retrieval.qdrant.low-memory-mode
name: low-memory-mode
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [low-memory-mode, no-resident, no-populate, ram, config-lowmem]
level: advanced
status: docs-checked
description: "Run on constrained memory with low_memory_mode values disabled, no_resident and no_populate."
sources:
  - "https://qdrant.tech/documentation/ops-configuration/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`low_memory_mode` is a storage setting for load time. It only affects how segments are loaded on startup, does not change any persisted configuration, and is intended as a recovery knob when a node crash-loops on out-of-memory.

```yaml
storage:
  low_memory_mode: no_resident
```

Allowed values from the configuration reference:

- `disabled`, the default.
- `no_resident`: downgrade components to their on-disk variants where possible; quantization loads as if `always_ram=false`, payload field indexes as if `on_disk=true`, payload storage as mmap (not populated).
- `no_populate`: the same as `no_resident`, plus skip the mmap prefault on load for vectors, the HNSW graph and payload storage.

Related knobs for fitting data into memory:

- Memory tiers for each structure (pinned, cached, cold).
- Quantization to shrink the searched copy.
- `on_disk_payload`, true by default (indexed payload values stay in RAM); the docs mark it deprecated in favour of the `payload` memory setting.
- Quotas that cap resident memory (`max_resident_memory_percent`).

## Checked

2026-11-03. Confirmed on the Qdrant configuration page: `low_memory_mode` values and behaviour, `disabled` default, `on_disk_payload` default and deprecation note; on the quotas page: `max_resident_memory_percent`. Corrected the purpose (load-time recovery knob, not a general speed trade-off). Removed unconfirmed storage and capacity advice.

Method: documentation only; no commands were run.
