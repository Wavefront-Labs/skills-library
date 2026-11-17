---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-sql-import-export-clones-and-failover-tests
name: cloud-sql-import-export-clones-and-failover-tests
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-sql, cloud-sql-import-export, sql-dump-gcs, cloud-sql-clone, instance-clone, point-in-time-recovery, cloud-sql-failover-test, manual-failover]
level: practitioner
status: docs-checked
description: "Move and protect Cloud SQL data: SQL/CSV import and export via Cloud Storage with offload, point-in-time clones, and scheduled HA failover tests."
sources: ["https://cloud.google.com/sql/docs/postgres/import-export", "https://cloud.google.com/sql/docs/mysql/import-export/import-export-sql", "https://cloud.google.com/sql/docs/postgres/clone-instance", "https://cloud.google.com/sql/docs/mysql/configure-ha#test"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud SQL import/export, clones and failover tests

## 1. Export and import via GCS
```bash
SA=$(gcloud sql instances describe db1 --format='value(serviceAccountEmailAddress)')
gcloud storage buckets add-iam-policy-binding gs://<B> --member=serviceAccount:$SA --role=roles/storage.objectAdmin
gcloud sql export sql db1 gs://<B>/exports/app-$(date +%F).sql.gz --database=app --offload
gcloud sql export csv db1 gs://<B>/exports/orders.csv --database=app --query="SELECT * FROM orders WHERE created > now() - interval '1 day'"
gcloud sql import sql db2 gs://<B>/exports/app-2026-10-16.sql.gz --database=app --user=app_owner
```
- `--offload` makes it a serverless export on a temporary instance, so other operations (edit, import, failover, daily automated backups) can run meanwhile; it costs extra, see the vendor's pricing page.
- A `.gz` extension compresses an export; importing a `.gz` file decompresses it automatically.
- Only one import or export operation runs per instance at a time (a second returns HTTP 409), and a long non-serverless one blocks other operations such as daily automated backups.

## 2. Clones
```bash
gcloud sql instances clone db1 db1-investigate                         # now
gcloud sql instances clone db1 db1-before-bad-deploy --point-in-time='2026-10-16T08:55:00Z'   # PITR, needs PITR enabled
```
Clones are independent instances with new IP addresses, ideal for forensic queries, upgrade
rehearsals, or restoring a dropped table without touching prod. Delete them afterwards.

## 3. Failover test (HA instances)
```bash
gcloud sql instances describe db1 --format='value(settings.availabilityType,gceZone,secondaryGceZone)'
gcloud sql instances failover db1      # primary moves to the standby zone
```
Let any previous failover finish before triggering another. Measure from the app side: connection
errors, reconnect time, pool behaviour. Run on a schedule and after driver/pool changes.

## Gotchas
- Every database user that owns objects or holds grants in the dump must already exist on the target, or the import fails to recreate ownership and permissions; create the users first.
- After an import, disk usage can be much higher if point-in-time recovery is on; disabling PITR lets the logs be deleted (provisioned storage does not shrink).
- A PITR clone needs PITR enabled on the source.

## Verify
- [ ] Monthly: an export restores into a scratch instance and row counts match.
- [ ] Failover drill recorded with downtime seconds and error counts; within the SLO budget.

## Checked
2026-10-31. Confirmed against the Cloud SQL import/export (PostgreSQL and MySQL), clone and HA failover-test pages: `serviceAccountEmailAddress` and `roles/storage.objectAdmin` grant, `--offload` serverless behaviour, `.gz` handling, one operation at a time, clone new IPs and PITR via cloning, `gcloud sql instances failover`, import ownership failures, PITR disk usage after import. Removed: parallel/threads and pg_dump/mydumper advice, SQL Server bak, promote-replica and switchover, reconnect-time figure, users/roles-exclusion claim.
Method: documentation only; no commands were run.
