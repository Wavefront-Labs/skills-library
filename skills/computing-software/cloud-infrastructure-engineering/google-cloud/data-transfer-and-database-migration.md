---
id: computing-software.cloud-infrastructure-engineering.google-cloud.data-transfer-and-database-migration
name: data-transfer-and-database-migration
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, storage-transfer-service, transfer-appliance, database-migration-service, dms, data-migration, gcloud-storage-rsync, transfer-agents, posix-transfer, s3-to-gcs, azure-to-gcs, continuous-migration, cdc, homogeneous-migration, heterogeneous-migration, conversion-workspace, cutover, bandwidth-planning]
level: practitioner
status: docs-checked
description: "Move data into GCP: Storage Transfer Service for S3, Azure and on-prem, Transfer Appliance, gcloud storage rsync, and Database Migration Service for continuous migrations."
sources: ["https://cloud.google.com/storage-transfer/docs/overview", "https://cloud.google.com/storage-transfer/docs/on-prem-overview", "https://cloud.google.com/transfer-appliance/docs/4.0/overview", "https://cloud.google.com/database-migration/docs/overview", "https://cloud.google.com/database-migration/docs/postgres/quickstart", "https://cloud.google.com/architecture/migration-to-google-cloud-transferring-your-large-datasets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data transfer and database migration

**Goal:** bytes arrive complete and verified, within the window the bandwidth allows, and
databases cut over with minutes of downtime because replication did the heavy lifting.

## 1. Size the problem first
`time = bytes / effective bandwidth`: work the figure out for your own link (Google's guide to transferring large datasets gives worked examples, e.g. 100 TB over 1 Gbps takes over 10 days online). Interconnect/VPN limits, source disk read speed and small-file overhead usually dominate. If the online estimate is unacceptably long, consider Transfer Appliance; otherwise use the network.

## 2. Storage Transfer Service (STS)
| Source | Setup |
|---|---|
| **S3 / Azure Blob / other GCS bucket / HTTP URL list** | agentless; `gcloud transfer jobs create s3://bucket gs://dest --source-creds-file=... --schedule-repeats-every=1d --overwrite-when=different --delete-from=destination-if-unique` (mirror) |
| **On-prem / POSIX filesystem, HDFS, S3-compatible** | run **transfer agents** (Docker) in an agent pool near the data: `gcloud transfer agents install --pool=onprem-pool --count=4 --mount-directories=/data`; then `gcloud transfer jobs create posix:///data gs://dest --source-agent-pool=onprem-pool` |
| GCS → POSIX (reverse) or POSIX → POSIX | same agents |
- Agents need outbound 443 to `storagetransfer.googleapis.com`, Pub/Sub and GCS (via PGA over Interconnect, or internet); scale throughput by adding agents/pools; cap with `--bandwidth-limit` per pool.
- Options that matter: `--include-prefixes`/`--include-modified-after-absolute`, `--overwrite-when=different` (checksum/mtime), `--preserve-metadata`, manifest files (`--manifest-file=gs://…csv`) for exact file lists, `--notification-pubsub-topic` for completion, event-driven transfers from S3 (SQS) / GCS (Pub/Sub) for continuous sync.
- STS verifies checksums (MD5/CRC32C) per object; the job's **transfer log** (`--log-actions=copy,delete,find --log-action-states=failed`) in Cloud Logging is your evidence.
- For < 1 TB or ad-hoc: `gcloud storage rsync -r /data gs://dest --checksums-only` (parallel). `gsutil` is legacy; `gcloud storage` is faster.

## 3. Transfer Appliance
Order the appliance size you need → Google ships → mount NFS/copy with the appliance's tooling (data encrypted with your key) → ship back → Google uploads to your bucket → you decrypt with the key you kept. Plan the delta sync with STS for data that changed while the appliance was in transit.

## 4. Database Migration Service (DMS)
- **Homogeneous** (MySQL→Cloud SQL MySQL, Postgres→Cloud SQL/AlloyDB Postgres, SQL Server→Cloud SQL SQL Server via backups): continuous CDC replication from source.
- **Heterogeneous** (Oracle→Postgres/AlloyDB, SQL Server→Postgres): **conversion workspace** converts schema (Ora2Pg-based), then continuous migration with Datastream-style CDC; expect manual fixes to PL/SQL.
Steps:
1. Prepare the source: binary logging (`binlog_format=ROW`, `expire_logs_days ≥ 7`) for MySQL; `wal_level=logical`, `pglogical` extension, replication user with `REPLICATION` and per-schema grants for Postgres; SQL Server needs full+log backups to GCS.
2. `gcloud database-migration connection-profiles create postgresql src --host=... --username=migrator --password=...` (or Secret Manager) and a destination profile that **creates the Cloud SQL instance** with HA, private IP, flags.
3. Connectivity: private IP over VPN/Interconnect with **private services access** peering (allow DMS's range in the source firewall), reverse SSH tunnel via a bastion VM, or IP allowlist for public sources. DMS tests connectivity before you can start.
4. `gcloud database-migration migration-jobs create pg-prod --type=CONTINUOUS --source=src --destination=dst --dump-type=LOGICAL`; `migration-jobs start`; watch `verify`/`describe` for the job phase (full dump, then CDC) and the **replication delay** metric.
5. Cutover: stop writes on the source, wait for delay = 0, `migration-jobs promote` (destination becomes a standalone primary), repoint apps, re-enable HA/backups settings you deferred.
- Postgres large objects, tables without primary keys (CDC cannot replicate deletes/updates reliably — add a PK or expect a full-dump-only table), DDL during migration (not replicated), and extensions not on the Cloud SQL allowlist are the typical blockers — DMS's pre-flight lists them.

## Gotchas
- STS to a bucket with **retention policy** or object holds fails on overwrite; CMEK on the destination needs the STS service agent on the key.
- Agents on a NAS mount: small-file throughput is bounded by NFS metadata ops, not bandwidth; run more agents, not bigger ones.
- DMS continuous jobs keep the Cloud SQL destination as a read replica until promote; backups/HA/PITR flags set at creation apply only after promotion — check them then.
- A promoted DMS destination keeps the migration user and `pglogical` artefacts; clean up.
- Transfer Appliance customs/export rules apply when crossing borders; order early.

## Verify
- [ ] STS job shows objects copied equals the source count and objects failed is 0 in the job's counters; a sampled `gcloud storage hash` matches on both sides.
- [ ] Agent pool throughput (`storagetransfer.googleapis.com/agent/transferred_bytes_count`) matches the planned rate.
- [ ] DMS job in `RUNNING`/CDC phase with replication delay near zero before cutover; a row written on the source appears on the destination within seconds.
- [ ] Post-promote: row counts and checksums (`pg_dump --schema-only` diff, `COUNT(*)` per table) match the source at the freeze point.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: worked transfer-time figures, the 20 TB appliance rule of thumb, appliance sizes and lead time, the rsync parallel-thread flag, DMS phase name, STS counter field names, 20 percent and 24 hour thresholds.

Method: documentation only; no commands were run.
