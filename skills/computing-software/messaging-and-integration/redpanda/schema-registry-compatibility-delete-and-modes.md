---
id: computing-software.messaging-and-integration.redpanda.schema-registry-compatibility-delete-and-modes
name: schema-registry-compatibility-delete-and-modes
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [schema-registry, compatibility, soft-delete, hard-delete, import-mode, readonly, migration]
level: practitioner
status: docs-checked
description: "Set Schema Registry compatibility levels, soft versus permanent deletes, and READWRITE, READONLY or IMPORT mode, including the 25.3 change on explicit IDs."
sources:
  - https://docs.redpanda.com/streaming/current/manage/schema-reg/schema-reg-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Compatibility** is applied per subject when a new schema is registered. Types: `BACKWARD` (default; consumers on the new schema read data from the previous one), `BACKWARD_TRANSITIVE` (all previous versions), `FORWARD`, `FORWARD_TRANSITIVE`, `FULL`, `FULL_TRANSITIVE` and `NONE` (no checks). Backward suits consumers that replay a topic from the start; forward suits real-time consumers; full is safest but limits changes.

```bash
rpk registry compatibility-level set sensor-value --level BACKWARD
```
This is `PUT /config/{subject}` with `{"compatibility": "BACKWARD"}`. An incompatible registration fails with "Schema being registered is incompatible with an earlier schema for subject".

**Deletion** uses `DELETE /subjects/{subject}/versions/{version}` or `/subjects/{subject}`. The `permanent` query parameter defaults to false (soft delete). A soft-deleted schema can be retrieved (list subjects with `deleted=true`) and re-registered; a hard delete cannot be recovered.

```bash
rpk registry schema delete sensor-value --schema-version 1
```

**Mode** via `/mode`:
- read-write (default): register and look up.
- read-only: lookups only; suited to disaster-recovery standby clusters.
- import: register schemas with explicit IDs and versions; suited to migration targets where IDs must be preserved.

```bash
rpk registry mode get --global
rpk registry mode set --mode <mode> --global
```
With authentication on, only superusers can change modes. Breaking change in 25.3: read-write mode errors if you register with a specific ID or version. Omit the ID and version, or switch the registry or subject to import mode.

## Checked

2026-11-04. Compatibility types, delete semantics, mode behaviour and the 25.3 caution were confirmed on the Schema Registry API page.

Method: documentation only; no commands were run.
