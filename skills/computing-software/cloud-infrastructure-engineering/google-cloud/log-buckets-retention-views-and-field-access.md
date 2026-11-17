---
id: computing-software.cloud-infrastructure-engineering.google-cloud.log-buckets-retention-views-and-field-access
name: log-buckets-retention-views-and-field-access
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-logging, log-buckets, log-bucket-regions, log-bucket-location, log-retention-config, retention-days, restricted-fields, field-level-access, log-view-access, log-views-iam, log-scopes, analytics-enabled-bucket, log-bucket-upgrade]
level: advanced
status: docs-checked
description: "Design Cloud Logging storage: bucket regions, retention days, Log Analytics upgrades, log views with conditional IAM, restricted fields, and log scopes for cross-project search."
sources: ["https://cloud.google.com/logging/docs/buckets", "https://cloud.google.com/logging/docs/regionalized-logs", "https://cloud.google.com/logging/docs/logs-views", "https://cloud.google.com/logging/docs/field-level-acl", "https://cloud.google.com/logging/docs/log-scope/create-and-manage", "https://cloud.google.com/logging/docs/analyze/query-and-view"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log buckets: location, retention, views and field access

## 1. Location (residency) — set before logs exist
```bash
gcloud logging settings update --organization=<ORG_ID> --storage-location=europe-west2   # default for new _Default buckets
gcloud logging buckets create app-logs --project=<P> --location=europe-west2 --retention-days=90 --enable-analytics
```
You cannot change the location of an existing bucket; `_Required` and `_Default` are created in `global` unless an organization policy sets a different default location. To move, create a regional bucket and route logs to it with a sink.

## 2. Retention
```bash
gcloud logging buckets update _Default --location=global --project=<P> --retention-days=60
```
Retention is 1 to 3650 days; the default is 30 days when you do not set one. A bucket `locked` setting means the retention period cannot be changed; treat locking as permanent.

## 3. Analytics (Log Analytics, called Observability Analytics in current docs)
```bash
gcloud logging buckets update _Default --location=global --project=<P> --enable-analytics   # one-way upgrade
gcloud logging links create default_bq --bucket=_Default --location=global --project=<P>  # BigQuery linked dataset
```
Once enabled, analytics cannot be disabled on the bucket. Upgrade and link need `roles/logging.configWriter`. Query upgraded buckets with SQL on the analytics page; you can still use Logs Explorer.

## 4. Log views + conditional IAM (team-scoped access)
```bash
gcloud logging views create payments --bucket=app-logs --location=europe-west2 --project=<P> \
  --log-filter='resource.type="k8s_container" AND resource.labels.namespace_name="payments"'
gcloud projects add-iam-policy-binding <P> --member=group:team-payments@example.com --role=roles/logging.viewAccessor \
  --condition='expression=resource.name == "projects/<P>/locations/europe-west2/buckets/app-logs/views/payments",title=payments-view'
```

## 5. Restricted fields
```bash
gcloud logging buckets update app-logs --location=europe-west2 --project=<P> \
  --restricted-fields=jsonPayload.customer_email,httpRequest.remoteIp
```
Logging hides restricted fields from users who lack `roles/logging.fieldAccessor` (or a role with similar permissions); users need that role as well as permission to view logs in the bucket.

## 6. Log scopes (search many projects at once)
```bash
gcloud logging scopes create sre-scope --project=<OPS_P> \
  --resource-names=projects/<P1>,projects/<P2>,projects/<P3>/locations/europe-west2/buckets/app-logs/views/_AllLogs
```
Select the scope in Logs Explorer.

## Gotchas
- `roles/logging.viewAccessor` granted on the project without a condition gives access to all views and logs in every bucket of the project; always attach the IAM condition for a single view. At most 20 role bindings in a project policy may share the same role and principal with different conditions.
- Every bucket gets an `_AllLogs` view, and `_Default` also has a `_Default` view; these automatic views cannot be modified.

## Verify
- [ ] `gcloud logging buckets describe app-logs --location=europe-west2 --format='yaml(retentionDays,analyticsEnabled,restrictedFields)'` matches design.
- [ ] A payments engineer sees only payments logs and cannot read the restricted fields.

## Checked

2026-10-28. Confirmed against: Cloud Logging API v2 discovery document (LogBucket fields `retentionDays`, `restrictedFields`, `locked`, `analyticsEnabled` irreversible), the log buckets page (1 to 3650 day retention, 30 day default, analytics upgrade one-way, `roles/logging.configWriter`), the regionalized logs page (location cannot change, `_Required` and `_Default` in global), the log views page (`roles/logging.viewAccessor` conditions, 20 binding limit, automatic views) and the field-level access page (`roles/logging.fieldAccessor`). Commands were checked against the gcloud reference.

Removed: the `_Required` 400-day figure and charging claim for retention over 30 days, the SQL example, the `--location` flag on `logging scopes create` (not a flag of that command), the redaction wording, and the `roles/logging.viewer`, export and BigQuery billing gotchas.

Method: documentation only; no commands were run.
