---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-sql-ha-replicas-and-connectivity
name: cloud-sql-ha-replicas-and-connectivity
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-sql, cloud-sql-ha, cloud-sql-proxy, cloud-sql-auth-proxy, read-replicas, cross-region-replica, private-ip, private-services-access, psc-cloud-sql, automated-backups, point-in-time-recovery, pitr, iam-database-authentication, maintenance-window, cloud-sql-insights, enterprise-plus, postgres, mysql, sql-server]
level: practitioner
status: docs-checked
description: "Run Cloud SQL in production: regional HA failover, read and cross-region replicas, private IP or PSC, Auth Proxy with IAM database auth, backups with PITR, maintenance windows."
sources: ["https://cloud.google.com/sql/docs/postgres/high-availability", "https://cloud.google.com/sql/docs/postgres/replication", "https://cloud.google.com/sql/docs/postgres/connect-overview", "https://cloud.google.com/sql/docs/postgres/sql-proxy", "https://cloud.google.com/sql/docs/postgres/backup-recovery/pitr", "https://cloud.google.com/sql/docs/postgres/maintenance", "https://cloud.google.com/sql/docs/postgres/editions-intro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud SQL HA, replicas and connectivity

**Goal:** a managed Postgres/MySQL/SQL Server that survives a zone loss without paging you,
scales reads, is reachable only privately with IAM identities, and can be rewound to any minute.

## 1. Create it right
```bash
gcloud sql instances create prod-pg --database-version=POSTGRES_16 --edition=ENTERPRISE_PLUS \
  --tier=db-perf-optimized-N-8 --region=europe-west1 --availability-type=REGIONAL \
  --network=projects/<HOST>/global/networks/prod-vpc --no-assign-ip --enable-google-private-path \
  --backup-start-time=02:00 --enable-point-in-time-recovery --retained-backups-count=14 --retained-transaction-log-days=7 \
  --maintenance-window-day=SUN --maintenance-window-hour=03 --maintenance-release-channel=production \
  --deletion-protection --storage-auto-increase --storage-type=SSD --storage-size=100GB \
  --database-flags=cloudsql.iam_authentication=on,log_min_duration_statement=500 \
  --insights-config-query-insights-enabled --disk-encryption-key=projects/P/locations/europe-west1/keyRings/kr/cryptoKeys/sql
```
- **Enterprise Plus** edition: near-zero-downtime maintenance and scaling, data cache. Compare SLA and PITR log retention per edition on the editions page; pick by SLA, not by instinct.
- `REGIONAL` = synchronous standby in another zone, same IP; failover is automatic. Zonal = single VM.
- Private IP requires **private services access** on the VPC (a reserved range, `gcloud services vpc-peerings connect`) — or **Private Service Connect** (`--enable-private-service-connect --allowed-psc-projects`) which avoids peering limits and works across VPCs; prefer PSC for new estates.

## 2. Connectivity
| Path | How | Notes |
|---|---|---|
| **Cloud SQL Auth Proxy** | `cloud-sql-proxy --private-ip --auto-iam-authn <P>:<R>:prod-pg` as sidecar/daemon | TLS + IAM, no client certs, works from GKE (sidecar), Cloud Run (`--add-cloudsql-instances`), VMs |
| Language connectors | Cloud SQL language connector libraries | same as proxy, in-process |
| Direct private IP | `psql -h 10.x.x.x` | needs SSL mode `--ssl-mode=ENCRYPTED_ONLY` or `TRUSTED_CLIENT_CERTIFICATE_REQUIRED` on the instance |
| Public IP | avoid; if forced, `--authorized-networks` + SSL required | org policy `sql.restrictPublicIp` blocks it |

**IAM database authentication**: `gcloud sql users create app-sa@P.iam --instance=prod-pg --type=CLOUD_IAM_SERVICE_ACCOUNT`, grant `roles/cloudsql.instanceUser` + `roles/cloudsql.client`; inside the DB `GRANT` privileges to the user `app-sa@P.iam`. Tokens replace passwords; rotate nothing.

## 3. Replicas
- **Read replica** (same region or `--region=<OTHER>` cross-region): `gcloud sql instances create prod-pg-r1 --master-instance-name=prod-pg --replica-type=READ --availability-type=REGIONAL`. Async; lag visible as `database/replication/replica_lag`.
- **Cross-region replica as DR**: `gcloud sql instances promote-replica prod-pg-dr` makes it standalone (new primary, old one stays — repoint apps, rebuild replica). Enterprise Plus supports **switchover** (planned, keeps replication direction reversible).
- Replicas need their own HA flag, backups off (backups come from primary), and private IP in their region.
- External replicas / external primaries (`--source-ip-address`) for migrations; use Database Migration Service instead for anything non-trivial.

## 4. Backups and recovery
- Automated daily + transaction logs → PITR: `gcloud sql instances clone prod-pg prod-pg-pitr --point-in-time=2026-10-14T09:30:00Z` creates a *new* instance; never restores over the primary. On-demand backups `gcloud sql backups create`;
- Backups live in the instance's region by default; set `--backup-location=eu` for cross-region copies. Deleting the instance deletes its backups — export critical ones (`gcloud sql export sql`) to a locked GCS bucket.

## 5. Operate
- Maintenance: Cloud SQL restarts the instance for maintenance. Set a maintenance window and a deny-maintenance period for freezes; test failover with `gcloud sql instances failover prod-pg`.
- Query Insights: per-query latency, tags via `/* application=... */` comments, lock waits. Flags: `max_connections` is derived from memory and resized when you change tier; use PgBouncer/proxy pooling for serverless clients.
- Storage auto-increase never shrinks; export/import to a new smaller instance to reclaim.

## Gotchas
- Failover keeps the IP but drops connections; apps must reconnect with backoff (the Auth Proxy handles it, bare drivers often do not).
- `deletion-protection` is an instance flag, not an IAM constraint; also protect with org policy / Terraform lifecycle protection.
- Private services access range must be allocated in the **host** VPC of a Shared VPC, and the service project needs `roles/compute.networkUser` on it.
- Major version upgrades are in-place (`--database-version` change) with downtime; test on a clone first and check extension compatibility.

## Verify
- [ ] `gcloud sql instances describe prod-pg --format='value(settings.availabilityType,ipAddresses,settings.backupConfiguration.pointInTimeRecoveryEnabled)'` shows REGIONAL, private IP only, PITR true.
- [ ] `gcloud sql instances failover` completes and the app reconnects within your agreed recovery objective.
- [ ] `psql "host=127.0.0.1 user=app-sa@P.iam dbname=app"` through the proxy with `--auto-iam-authn` works with no password.
- [ ] PITR clone to 10 minutes ago contains the expected rows; replica lag stays within your agreed bound under normal load.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: SLA percentages, failover and maintenance timings, replica count limit, 35-day log retention, 90-day deny-maintenance cap, replica lag thresholds, the connector package name, the reserved-range size and the billing remark on cross-region replicas.

Method: documentation only; no commands were run.
