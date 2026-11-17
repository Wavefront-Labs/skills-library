---
id: computing-software.cybersecurity-defensive.pomerium.databroker-storage-backends
name: databroker-storage-backends
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [databroker, storage-backend, postgres, in-memory, shared-secret-mismatch]
level: practitioner
status: docs-checked
description: "Pick and configure the Pomerium databroker backend (in-memory, file, Postgres), its HA properties, encryption caveats and common failure."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/data-storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `databroker` is the only stateful component. Losing its data forces users to log in again when their session next expires; most other data is recoverable from external sources.

| Backend | Broker HA | Store HA | Persistent |
|---|---|---|---|
| In-memory (default) | no | no | no |
| File | no | no | yes |
| Postgres | yes | yes | yes |

- **In-memory**: running more than one instance is unsupported and behaves non-deterministically.
- **File**: single instance.

```yaml
databroker_storage_type: file
databroker_storage_connection_string: file:///var/pomerium/databroker
```

- **Postgres** (dedicated instance recommended):

```yaml
databroker_storage_type: postgres
databroker_storage_connection_string: postgres://user:pass@dbhost.internal.mydomain.com/pomerium?sslmode=disable
```

The string follows libpq conventions. With several hosts set `target_session_attrs=read-write` so writes avoid a read-only replica.

Encryption: Pomerium does not encrypt record values for any of the three backends; use encryption at rest such as full-disk encryption.

Troubleshooting: most databroker problems are a `shared_secret` mismatch between services. Production should use a persistent backend. Custom backends can implement the databroker gRPC interface.

## Checked

2026-11-04. Confirmed against the Persistence and Data storage page: backend HA and persistence table, in-memory multi-instance warning, file and Postgres configuration examples, libpq conventions, target_session_attrs, no record value encryption, shared_secret troubleshooting, custom gRPC databroker. Nothing removed.

Method: documentation only; no commands were run.
