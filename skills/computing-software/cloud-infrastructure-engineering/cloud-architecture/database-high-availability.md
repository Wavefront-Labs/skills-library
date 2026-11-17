---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.database-high-availability
name: database-high-availability
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, database-high-availability, multi-az-database, synchronous-replication, automatic-failover, zone-redundant-database]
level: practitioner
status: docs-checked
description: "Configure managed database HA: multi-AZ/zone-redundant options, synchronous vs async replicas, failover time and client behaviour, maintenance and testing failover."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html", "https://learn.microsoft.com/azure/reliability/reliability-postgresql-flexible-server", "https://cloud.google.com/sql/docs/postgres/high-availability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database high availability configuration

## Managed options
| Service | HA mechanism | Failover time stated by the vendor |
|---|---|---|
| RDS Multi-AZ DB instance | One standby for failover, does not serve read traffic | see the RDS Multi-AZ page |
| RDS Multi-AZ DB cluster | Two standbys that provide failover and can serve read traffic | see the RDS Multi-AZ page |
| Azure Database for PostgreSQL flexible server, zone-redundant HA | Synchronous replication to a standby in another zone; the standby serves no client traffic | typically within 60-120 s |
| Cloud SQL HA (regional) | Standby in a second zone, takes over on the shared static IP | about 60 s unavailable, can differ by environment |

## Client-side
- Connect via the service endpoint/DNS name, never instance IP.
- Short DNS caching in clients, retries with backoff on connection loss, idempotent writes. The Azure page says clients that retry after a short period typically avoid significant impact.

## Steps
1. Enable HA for production tiers; same-zone app placement preference to reduce latency.
2. Configure maintenance windows and read the vendor's note on what planned operations do to the standby.
3. Test failover: `aws rds reboot-db-instance --force-failover`, Azure forced failover,
   `gcloud sql instances failover`; measure app error duration.
4. Pair with backups/PITR and cross-region replica for DR (HA is not DR).

## Gotchas
- HA standby doesn't protect against bad writes or deletion: Azure states user errors such as an accidental table drop replicate to the standby, so recover with point-in-time restore.
- Long-running transactions extend failover/recovery.

## Checked
2026-10-28. Confirmed: RDS Multi-AZ page (one standby not serving reads versus two standbys that can serve reads), Azure reliability page for PostgreSQL flexible server (synchronous replication, 60-120 s zone-redundant failover, standby serves no traffic, errors replicate), Cloud SQL HA page (about sixty seconds, shared static IP). Both CLI commands exist (check_commands: `aws rds reboot-db-instance --force-failover`, `gcloud sql instances failover`). Removed: RDS and Aurora failover figures, semi-sync wording, Aurora row, RDS Proxy and JDBC wrapper claims, the long-transaction gotcha (not in the sources).
Method: documentation only; no commands were run.

## Verify
- [ ] Measured failover impact on the app within RTO for zone failure.
