---
id: computing-software.search-and-information-retrieval.qdrant.config-defaults
name: config-defaults
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [defaults, ports, storage-path, wal, config-defaults]
level: practitioner
status: docs-checked
description: "Key Qdrant defaults: ports 6333, 6334 and 6335, storage paths, request size, WAL and snapshot settings."
sources:
  - "https://qdrant.tech/documentation/ops-configuration/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Selected defaults from the configuration reference:

Service:

- `service.http_port`: 6333 (REST)
- `service.grpc_port`: 6334
- internal peer-to-peer port: 6335 (cluster only)
- `host`: 0.0.0.0
- `max_request_size_mb`: 32
- `enable_cors`: true
- `enable_tls`: false

Storage:

- `storage_path`: `./storage`
- `snapshots_path`: `./snapshots`
- `snapshots_storage`: local, with s3, gcs or azure as alternatives
- `on_disk_payload`: true
- `node_type`: Normal (the other is Listener)
- WAL: `wal_capacity_mb` 32, `wal_segments_ahead` 0, `wal_retain_closed` 1

Cluster-level collection defaults: `replication_factor` 1 and `write_consistency_factor` 1.

Other settings: `max_collections` caps the number of collections, `low_memory_mode` accepts `disabled`, `no_resident` or `no_populate`, and a performance section covers `max_search_threads` (0 for automatic) and `optimizer_cpu_budget`.

The full default file is `config/config.yaml` in the Qdrant source. The docs note `on_disk_payload` is deprecated in favour of `payload.memory`, and that Qdrant Cloud does not allow modifying the configuration.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant configuration page (landing_page repo, ops-configuration/configuration.md), reading the full options YAML. Removed the unconfirmed advice to bind to 127.0.0.1 and the generic closing paragraph.
