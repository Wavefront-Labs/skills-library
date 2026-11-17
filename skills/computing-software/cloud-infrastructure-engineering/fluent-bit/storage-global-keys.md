---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.storage-global-keys
name: storage-global-keys
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, storage, filesystem-buffering, storage-path, max-chunks-up, checksum, sync]
level: advanced
status: docs-checked
description: "Configure Fluent Bit's global storage.* keys: path, sync, checksum, max_chunks_up, backlog and inherited storage type."
sources: ["https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/yaml/service-section"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global storage keys

Storage keys sit in the `service` section and control the filesystem buffer used by inputs with filesystem storage.

| Key | Default | Meaning |
| --- | --- | --- |
| `storage.path` | none | where streams and chunks are stored; without it inputs cannot use filesystem buffering |
| `storage.sync` | `normal` | `normal` or `full`; `full` guarantees data is synced even if Fluent Bit crashes (on Linux it corresponds to `MAP_SYNC`) |
| `storage.checksum` | `off` | CRC32 integrity check on write and read |
| `storage.max_chunks_up` | `128` | chunks that can be `up` in memory for filesystem inputs |
| `storage.type` | none | default input storage type: `memory`, `filesystem`, `memrb` |
| `storage.inherit` | `off` | inputs without their own `storage.type` take the global one |
| `storage.trim_files` | `off` | trim chunk files after flush to reclaim disk space |
| `storage.delete_irrecoverable_chunks` | `off` | delete irrecoverable chunks at runtime and startup |
| `storage.metrics` | `off` | registers a storage metrics endpoint when `http_server` is on |
| `storage.backlog.mem_limit` | `5M` | memory used by `storage_backlog` when promoting leftover chunks |
| `storage.backlog.flush_on_shutdown` | `off` | try to flush all backlog chunks during shutdown, which can lengthen it |

```yaml
service:
  storage.path: /var/lib/fluent-bit/storage
  storage.sync: normal
  storage.checksum: on
  storage.max_chunks_up: 128
```

Buffering semantics are in `computing-software.cloud-infrastructure-engineering.fluent-bit.buffering-modes`.

## Checked

2026-11-03. Confirmed on the Fluent Bit YAML Service section page (Storage configuration): every key, default and meaning in the table. Fixed: storage.sync default is `normal` and storage.backlog.mem_limit default is `5M`.

Method: documentation only; no commands were run.
