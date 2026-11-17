---
id: computing-software.cloud-infrastructure-engineering.google-cloud.log-sink-filters-cross-project-routing-and-errors
name: log-sink-filters-cross-project-routing-and-errors
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-logging, log-sinks, sink-filters, inclusion-exclusion-filters, cross-project-sinks, project-sink-to-central, sink-errors, export-errors]
level: practitioner
status: docs-checked
description: "Route logs with sinks: inclusion and exclusion filters, sampling, project sinks into a central project or bucket, writer-identity grants, and detecting sink export errors."
sources: ["https://cloud.google.com/logging/docs/export/configure_export_v2", "https://cloud.google.com/logging/docs/export/aggregated_sinks", "https://cloud.google.com/logging/docs/export/troubleshoot", "https://cloud.google.com/logging/docs/routing/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log sinks: filters, cross-project routing and errors

## 1. Filters
Each sink has an inclusion filter and optional exclusion filters; an entry is routed when it
matches the inclusion filter and none of the exclusion filters.
```bash
gcloud logging sinks create errors-to-central \
  logging.googleapis.com/projects/<CENTRAL>/locations/europe-west2/buckets/app-errors \
  --project=<P> --log-filter='severity>=ERROR' \
  --exclusion=name=healthchecks,filter='httpRequest.requestUrl:"/healthz"'
# reduce what the _Default sink stores
gcloud logging sinks update _Default --project=<P> \
  --add-exclusion=name=gke-debug,filter='resource.type="k8s_container" AND severity<=DEBUG'
```
To route a random sample, add `sample(insertId, 0.10) AND ...` to the filter: that routes ten
percent of the matching entries. You cannot exclude entries from the `_Required` sink or disable
it; think twice before excluding anything from your security sink.

## 2. Into a central project
| Destination | Form | Grant the sink's writer identity |
|---|---|---|
| central log bucket | `logging.googleapis.com/projects/<C>/locations/<L>/buckets/<B>` | `roles/logging.bucketWriter` |
| central project (its sinks route further) | `logging.googleapis.com/projects/<C>` | `roles/logging.logWriter` |
| BigQuery dataset | BigQuery URL | `roles/bigquery.dataEditor` |
| Cloud Storage bucket | bucket URL | `roles/storage.objectCreator` |
| Pub/Sub topic | topic URL | `roles/pubsub.publisher` |

Per the docs every destination needs the Logs Writer role (`roles/logging.logWriter`, permission
`logging.logEntries.route`) in addition to the destination-specific role.
```bash
WI=$(gcloud logging sinks describe errors-to-central --project=<P> --format='value(writerIdentity)')
gcloud projects add-iam-policy-binding <CENTRAL> --member=$WI --role=roles/logging.bucketWriter
```
For many projects, use one **aggregated sink** at folder or organization level with `--include-children`.

## 3. Detect errors
- Metric `logging.googleapis.com/exports/error_count`: log entries that failed to export; alert on it.
- A misconfigured sink writes log entries describing the error and emails the Essential Contacts for the resource.
- Sink errors are logged under `logName:"logging.googleapis.com%2Fsink_error"`.
- BigQuery destinations get an `export_errors` table (date-sharded: `export_errors_YYYYMMDD`).
```bash
gcloud logging read 'logName:"logging.googleapis.com%2Fsink_error"' --project=<P> --limit=10
```
Sinks cannot retroactively route entries received before they were created or while misconfigured.

## Verify
- [ ] A test entry (`gcloud logging write test-log "test" --severity=ERROR --project=<P>`) appears in the central bucket.
- [ ] `exports/error_count` is zero across sinks and an alert exists.

## Checked
2026-10-28. Confirmed against Route logs to supported destinations, Aggregated sinks, Troubleshoot routing and the Log routing overview, plus the Logging query language page (`sample`): inclusion/exclusion semantics, destination formats, required roles, `--include-children`, `exports/error_count`, `sink_error` log name, `export_errors` tables, Essential Contacts email, no retroactive routing. gcloud commands checked with check_commands.py. Removed: cost and billing claims, 15-minute alert window, schema-conflict and drop behaviour, `--unique-writer-identity` gotcha, Console path.
Method: documentation only; no commands were run.
