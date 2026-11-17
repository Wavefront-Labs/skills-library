---
id: computing-software.cloud-infrastructure-engineering.google-cloud.alloydb-cluster-setup-flags-iam-auth-and-maintenance
name: alloydb-cluster-setup-flags-iam-auth-and-maintenance
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, alloydb, alloydb-cluster-create, gcloud-alloydb, alloydb-flags, alloydb-database-flags, alloydb-iam-auth, alloydb-maintenance, read-pools]
level: practitioner
status: docs-checked
description: "Create AlloyDB clusters with gcloud (PSA or PSC networking, HA primary, read pools), set database flags, enable IAM database authentication, and control maintenance windows."
sources: ["https://docs.cloud.google.com/alloydb/docs/cluster-create", "https://docs.cloud.google.com/alloydb/docs/instance-configure-database-flags", "https://docs.cloud.google.com/alloydb/docs/manage-iam-authn", "https://docs.cloud.google.com/alloydb/docs/maintenance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AlloyDB: cluster setup, flags, IAM auth and maintenance

## 1. Create
```bash
# Private services access must exist on the VPC (allocated range + servicenetworking peering)
gcloud alloydb clusters create orders --region=europe-west2 \
  --network=projects/<HOST>/global/networks/prod --allocated-ip-range-name=psa-alloydb \
  --password="$(gcloud secrets versions access latest --secret=alloydb-postgres-pw)"
gcloud alloydb instances create orders-primary --cluster=orders --region=europe-west2 \
  --instance-type=PRIMARY --cpu-count=8 --availability-type=REGIONAL
gcloud alloydb instances create orders-rp --cluster=orders --region=europe-west2 \
  --instance-type=READ_POOL --cpu-count=4 --read-pool-node-count=2
```
PSC instead of PSA: `--enable-private-service-connect` on the cluster, then consumer endpoints per
VPC. Check backup settings with
`gcloud alloydb clusters describe orders --region=<R> --format='yaml(automatedBackupPolicy,continuousBackupConfig)'`
and the retention values in the cluster-create page.

## 2. Database flags
```bash
gcloud alloydb instances update orders-primary --cluster=orders --region=<R> \
  --database-flags=alloydb.iam_authentication=on,log_min_duration_statement=500,google_columnar_engine.enabled=on
```
The `--database-flags` list **overwrites** all previously set flags (unlisted ones reset to default), so include current and new flags. Some flags make AlloyDB restart the instance; the flags page lists which and the maintenance policies (low downtime or force apply) for primary and read pool.

## 3. IAM database authentication
```bash
gcloud alloydb users create alice@example.com --cluster=orders --region=<R> --type=IAM_BASED
gcloud alloydb users create app-sa@<P>.iam --cluster=orders --region=<R> --type=IAM_BASED   # SA without .gserviceaccount.com
gcloud projects add-iam-policy-binding <P> --member=user:alice@example.com --role=roles/alloydb.databaseUser
gcloud projects add-iam-policy-binding <P> --member=user:alice@example.com --role=roles/serviceusage.serviceUsageConsumer
./alloydb-auth-proxy "projects/<P>/locations/<R>/clusters/orders/instances/orders-primary" --auto-iam-authn
psql "host=127.0.0.1 user=alice@example.com dbname=postgres"
```
Then `GRANT` database privileges in SQL — IAM only authenticates.

## 4. Maintenance
```bash
gcloud alloydb clusters update orders --region=<R> --maintenance-window-day=SUNDAY --maintenance-window-hour=2
```
With no window set, non-emergency maintenance can occur at any time except 6 AM to 10 PM on weekdays (local time of the cluster's region). Emergency maintenance (urgent security patches) can occur outside windows and deny periods. Self-service maintenance lets you update ahead of the window and set a deny period.

## Gotchas
- A PSA range that is too small blocks new clusters/instances; size it for every service that shares it.
- Read pools replicate asynchronously; route read-your-writes queries to the primary.
- The shortened service-account identifier (email without `.gserviceaccount.com`) must not exceed 63 characters or IAM authentication fails.

## Checked
2026-10-31. Confirmed against the AlloyDB cluster-create, database-flags, manage-iam-authn and maintenance pages: `--database-flags` overwrite behaviour and restart policies, `alloydb.iam_authentication`, roles `alloydb.databaseUser` and `serviceusage.serviceUsageConsumer`, service-account name without `.gserviceaccount.com` (63-character limit), default maintenance hours, emergency maintenance and deny periods. Every gcloud command and flag checked against the gcloud reference. Removed: 14-day PITR default, /20 range size, downtime-seconds and replica-lag figures, OAuth-token claim.
Method: documentation only; no commands were run.

## Verify
- [ ] `gcloud alloydb instances list --cluster=orders --region=<R>` shows READY primary (REGIONAL) and read pool.
- [ ] Alice connects via `--auto-iam-authn`; a user without `databaseUser` is refused.
