---
id: computing-software.cloud-infrastructure-engineering.google-cloud.security-log-sinks-and-siem-export
name: security-log-sinks-and-siem-export
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, log-sinks, log-router, aggregated-sinks, log-retention, log-buckets, siem, security-operations, google-secops, chronicle, splunk-export, pubsub-sink, bigquery-sink, gcs-sink, log-views, locked-buckets, log-analytics, security-logging, centralized-logging, sink-writer-identity]
level: practitioner
status: docs-checked
description: "Centralise security logs: org-level aggregated sinks to locked log buckets, BigQuery, GCS and Pub/Sub for a SIEM, log views for least privilege, and retention that matches policy."
sources: ["https://docs.cloud.google.com/logging/docs/export/aggregated_sinks", "https://docs.cloud.google.com/logging/docs/routing/overview", "https://docs.cloud.google.com/logging/docs/buckets", "https://docs.cloud.google.com/logging/docs/logs-views", "https://docs.cloud.google.com/logging/docs/export/configure_export_v2"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Security log sinks and SIEM export

**Goal:** every audit log (and any other log class you choose) from every project lands
in one immutable place with the retention compliance demands, and a copy streams to the SIEM — configured once at org level, impossible for a project owner to switch off.

## 1. Central logging project and buckets
```bash
gcloud logging buckets create sec-audit --location=europe-west1 --project=prj-c-logging \
  --retention-days=400 --enable-analytics --cmek-kms-key-name=projects/prj-p-kms/.../cryptoKeys/logs
gcloud logging buckets update sec-audit --location=europe-west1 --project=prj-c-logging --locked   # irreversible: no deletion, no retention decrease
```
- `--enable-analytics` upgrades the bucket so you can run SQL over it in Observability Analytics and, via a link, query it from BigQuery as a read-only linked dataset. The upgrade cannot be undone.
- Locking a bucket is irreversible: the bucket cannot be deleted until every entry has met its retention period. Lock only after you have tested the filter — a locked bucket full of junk is forever.

## 2. Org-level aggregated sinks (`--include-children`)
```bash
gcloud logging sinks create org-audit-to-bucket \
  logging.googleapis.com/projects/prj-c-logging/locations/europe-west1/buckets/sec-audit \
  --organization=<ORG_ID> --include-children \
  --log-filter='logName:"cloudaudit.googleapis.com"'   # add other log classes with their own log-name terms
gcloud logging sinks create org-security-to-siem pubsub.googleapis.com/projects/prj-c-logging/topics/siem \
  --organization=<ORG_ID> --include-children --log-filter='<same or narrower>'
```
- Each sink gets a **writer identity** (a service account email, shared by all sinks of the same organization); grant it `roles/logging.bucketWriter` on the bucket, `pubsub.publisher` on the topic, `bigquery.dataEditor` on the dataset, `storage.objectCreator` on the GCS bucket. `gcloud logging sinks describe` prints it.
- **Intercepting sinks** (`--intercept-children`) stop matching entries from being sent to the sinks in child resources (the entry still goes to the `_Required` sink where it originates) — use to keep sensitive logs out of project-level view.
- Sink filters are evaluated per entry; exclusions (`--exclusion=name=...,filter=...`) inside the sink drop noise (health-check probes, `k8s_container` debug).
- Organization and folder default resource settings control the system-created `_Default` sink for new resources (for example to disable it or change its filters).

## 3. Destinations compared
| Destination | Use | Notes |
|---|---|---|
| **Log bucket** (+ Log Analytics) | primary retention, investigations | locked, CMEK, views |
| **BigQuery** dataset | long-term analytics joins, dashboards | partitioned tables per log type; `--use-partitioned-tables` on the sink |
| **Cloud Storage** | cold archive, legal hold | hourly batches; bucket with retention policy/lock |
| **Pub/Sub** | SIEM streaming | size the subscription retention for SIEM outages |

## 4. Least-privilege access with log views
```bash
gcloud logging views create payments-view --bucket=sec-audit --location=europe-west1 --project=prj-c-logging \
  --log-filter='resource.labels.project_id="prj-p-payments"'
# grant roles/logging.viewAccessor on the view, not the bucket:
gcloud projects add-iam-policy-binding prj-c-logging --member=group:payments-sec@example.com --role=roles/logging.viewAccessor \
  --condition='expression=resource.name=="projects/prj-c-logging/locations/europe-west1/buckets/sec-audit/views/payments-view",title=payments-view'
```
Security team gets the bucket's `_AllLogs` view; application teams get project-scoped views. Every log bucket has an automatic `_AllLogs` view.

## 5. Retention and cost control
- Decide retention per log class from your regulator's requirement, and use different buckets per class so retention and lock differ.
- A log routed to several sinks is stored at each destination; see the Cloud Logging pricing page for what each costs.

## Gotchas
- Grant the sink's writer identity access on the destination right after creating the sink; the same service account is used for all sinks in the underlying resource.
- Aggregated sinks cover only the folder or organization they are created in; folder sinks serve delegated teams.
- The per-project `_Required` bucket is not your central evidence store (its retention cannot be changed).
- Locked bucket + wrong location = cannot move; location choice is also a residency decision.
- The Pub/Sub to SIEM path loses messages when the SIEM is down longer than the subscription retention; alert on the subscription's unacked backlog.

## Verify
- [ ] Create a project anywhere in the org and run `gcloud projects get-iam-policy`: the `SetIamPolicy` entry appears in `sec-audit` with no per-project config.
- [ ] `gcloud logging buckets describe sec-audit` shows the bucket locked, 400 days retention and the CMEK key.
- [ ] A payments engineer sees only `prj-p-payments` entries through the view; `_AllLogs` is denied.
- [ ] SIEM shows the same `SetIamPolicy` event; the sink shows no export errors.

## Checked
2026-10-31. Confirmed on the Cloud Logging routing overview, buckets, log views, aggregated sinks and sink-export pages: lock irreversibility and deletion block, Observability Analytics upgrade permanent, read-only linked dataset, intercepting sinks still reach `_Required`, default resource settings for `_Default`, `_Required` retention fixed, shared writer service account per resource, destination roles (bucketWriter, publisher, dataEditor, objectCreator), `viewAccessor` with an IAM condition per view, automatic `_AllLogs` view, hourly Cloud Storage sinks. Removed: firewall/DNS/IAP/VPC-SC filter terms, literal writer-identity format, cross-project routing row, Pub/Sub metric name, Logs Explorer menu path (unconfirmed). Commands checked with check_commands.py. Chronicle ingestion and pricing pages are not relied on.
Method: documentation only; no commands were run.
