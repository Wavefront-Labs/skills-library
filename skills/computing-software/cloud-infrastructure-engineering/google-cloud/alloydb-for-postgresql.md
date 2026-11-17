---
id: computing-software.cloud-infrastructure-engineering.google-cloud.alloydb-for-postgresql
name: alloydb-for-postgresql
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, alloydb, alloydb-omni, postgresql, columnar-engine, read-pool, primary-instance, alloydb-auth-proxy, continuous-backup, cross-region-replication, secondary-cluster, alloydb-ai, pgvector, scann, psc-alloydb, managed-postgres, htap]
level: practitioner
status: gated
description: "Deploy AlloyDB when Cloud SQL Postgres is not enough: cluster, primary and read pools, columnar engine, continuous backup, secondary clusters for DR, Auth Proxy with IAM auth."
sources: ["https://cloud.google.com/alloydb/docs/overview", "https://cloud.google.com/alloydb/docs/cluster-create", "https://cloud.google.com/alloydb/docs/columnar-engine/about", "https://cloud.google.com/alloydb/docs/cross-region-replication/work-with-cross-region-replication", "https://cloud.google.com/alloydb/docs/backup/continuous-backup-overview", "https://cloud.google.com/alloydb/docs/ai/work-with-embeddings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AlloyDB for PostgreSQL

**Goal:** Postgres-compatible database with separated compute and storage, read pools that
scale horizontally, in-memory columnar acceleration for reporting queries, and a DR cluster in another region.

## 1. When AlloyDB over Cloud SQL
- Mixed OLTP + analytics on the same data (columnar engine gives 10-100× on scans/aggregates).
- Need >8 read replicas, or replicas that lag in the low milliseconds (shared storage, no replay).
- 99.99 % SLA with near-instant failover, larger instances (up to 128 vCPU), vector search at scale.
- Otherwise Cloud SQL Enterprise Plus is cheaper and simpler (see `cloud-sql-ha-replicas-and-connectivity`).

## 2. Topology
```bash
gcloud alloydb clusters create prod --region=europe-west1 --network=projects/<HOST>/global/networks/prod-vpc \
  --password=<FROM_SECRET_MANAGER> --continuous-backup-recovery-window-days=14 \
  --kms-key=projects/P/locations/europe-west1/keyRings/kr/cryptoKeys/alloydb
gcloud alloydb instances create prod-primary --cluster=prod --region=europe-west1 \
  --instance-type=PRIMARY --cpu-count=8 --availability-type=REGIONAL \
  --database-flags=alloydb.enable_pgaudit=on,google_columnar_engine.enabled=on
gcloud alloydb instances create prod-reads --cluster=prod --region=europe-west1 \
  --instance-type=READ_POOL --read-pool-node-count=3 --cpu-count=8
```
- **Cluster** = storage + config; **primary instance** = one writer (HA = standby in another zone, same endpoint); **read pool** = N identical nodes behind one IP, load-balanced, scale `--read-pool-node-count` without reconnect.
- Networking: private services access (`--network`) or **PSC** (`--enable-private-service-connect` + `--allowed-psc-projects` on instances). No public IP unless `--assign-inbound-public-ip` with authorized networks.
- Connect via **AlloyDB Auth Proxy** (`alloydb-auth-proxy projects/P/locations/R/clusters/prod/instances/prod-primary --auto-iam-authn`) or language connectors; IAM auth needs `alloydb.iam_authentication=on` and users created with `--type=IAM_BASED`.

## 3. Columnar engine
- Enable flag `google_columnar_engine.enabled=on` and size `google_columnar_engine.memory_size_in_mb` (default ~30 % of instance memory).
- Auto-columnarisation picks hot tables; or pin: `SELECT google_columnar_engine_add('schema.orders', 'order_date,customer_id,amount');`.
- Check `EXPLAIN (ANALYZE)` for `Custom Scan (columnar scan)`; `google_columnar_engine_recommend()` (gated: unconfirmed, source is paywalled or blocked) suggests columns from the query log.
- It accelerates scans/filters/aggregates, not point lookups or writes; keep it off on write-heavy instances.

## 4. Backups and DR
- **Continuous backup** (PITR): `clusters restore --point-in-time=…` into a *new* cluster; recovery window 1-35 days.
- On-demand/scheduled backups via `--automated-backup-*` flags; backups are cluster-level.
- **Secondary cluster** (cross-region): `gcloud alloydb clusters create-secondary prod-dr --primary-cluster=projects/P/locations/europe-west1/clusters/prod --region=europe-west4` + a secondary instance. Async replication; `clusters promote prod-dr` for DR, `clusters switchover` for planned, reversible moves.
- Secondary clusters support read pools — use them to serve nearby reads, not just as a standby.

## 5. AI features
- `pgvector` with Google's **ScaNN** index: `CREATE EXTENSION alloydb_scann; CREATE INDEX ON docs USING scann (embedding cosine) WITH (num_leaves=1000);` — far better recall/latency than IVFFlat at 10M+ rows.
- `google_ml_integration` lets SQL call Vertex AI embeddings: `SELECT embedding('text-embedding-005', 'query');` — grant the AlloyDB service agent `roles/aiplatform.user`.
- **AlloyDB Omni** is the same engine as a container for on-prem/other clouds/dev laptops (`docker run google/alloydbomni`).

## Gotchas
- Minimum footprint is 2 vCPU primary + storage; there is no "db-f1-micro" — dev environments should use Omni or Cloud SQL.
- Read pool nodes are in one region; latency from another region is the WAN, not AlloyDB.
- Extensions are allow-listed; check the supported list before migrating a Postgres with exotic extensions.
- Major-version upgrades are in-place with downtime; PITR restores produce new clusters with new IPs — automate the DNS/connection switch.
- Storage bills for used data **plus** continuous-backup log retention; a long window on a churny DB is not free.

## Verify
- [ ] `gcloud alloydb instances describe prod-primary` shows `availabilityType: REGIONAL`, private IP only; `prod-reads` shows the intended node count.
- [ ] A reporting query shows `columnar scan` in `EXPLAIN ANALYZE` and runs ≥5× faster than with the flag off.
- [ ] `clusters restore --point-in-time` of 10 minutes ago yields the expected data in a new cluster.
- [ ] Secondary cluster lag (`alloydb.googleapis.com/cluster/replication/lag` (gated: unconfirmed, source is paywalled or blocked)) stays within your agreed bound; `switchover` and back completes in a test window.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the 35-day backup window figure and the fixed replication-lag threshold. Gated: the columnar engine recommend function name and the replication lag metric name were not found in the fetched pages.

Method: documentation only; no commands were run.
