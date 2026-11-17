---
id: computing-software.database-administration.cloudnative-pg.self-healing-primary-and-standby-failure
name: self-healing-primary-and-standby-failure
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [failover, self-healing, pg-rewind, primary-failure, standby-failure, promotion]
level: practitioner
status: docs-checked
description: "What CloudNativePG does when a primary or standby pod fails: promotion, service updates, pg_rewind, rebuild from backup."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/failure_modes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page leans on standard Kubernetes behaviour (storage classes, PVCs, nodes, Pods) and points to the instance manager's startup, liveness and readiness probes for the CloudNativePG-specific part.

**Primary pod failure**

- The operator promotes the most up-to-date standby, the one with the lowest replication lag.
- The `-rw` service is updated to point at the new primary.
- The failed Pod is removed from the `-r` and `-rw` services.
- Standbys start replicating from the new primary.
- The former primary re-synchronises with `pg_rewind` if its PVC is still available; otherwise a new standby is created from a backup of the new primary.

**Standby pod failure**

- The Pod is removed from `-r` and `-ro`.
- It restarts using its PVC if available; otherwise a new Pod is created from a backup of the current primary.
- Once ready it is re-added to `-r` and `-ro`.

Failure scenarios outside these paths need manual intervention, and the page advises not doing manual operations without professional support.

## Checked

2026-11-08. Primary and standby self-healing sequences confirmed on the Failure Modes page.

Method: documentation only; no commands were run.
