---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigtable-change-streams
name: bigtable-change-streams
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigtable, bigtable-change-streams, cdc, dataflow, bigquery]
level: advanced
status: docs-checked
description: "Enable Bigtable change streams with a retention period and consume them with Dataflow templates to BigQuery or Pub/Sub, handling partitions, GC mutations and costs."
sources: ["https://docs.cloud.google.com/bigtable/docs/change-streams-overview", "https://docs.cloud.google.com/sdk/gcloud/reference/bigtable/instances/tables/update", "https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/main/v2/googlecloud-to-googlecloud/README_Bigtable_Change_Streams_to_BigQuery.md", "https://github.com/apache/beam/blob/master/sdks/java/io/google-cloud-platform/src/main/java/org/apache/beam/sdk/io/gcp/bigtable/BigtableIO.java"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bigtable change streams

## 1. Enable
```bash
gcloud bigtable instances tables update events --instance=<I> --change-stream-retention-period=3d
# disable: --clear-change-stream-retention-period
```
Retention is 1 to 7 days (`5d` and `48h` are valid forms). Change records cost storage (the docs estimate roughly 1.5 times the size of the data written that day) and some CPU (about 10% more for enabling, 20 to 30% more for processing).

## 2. Consume
Prebuilt Dataflow flex templates (streaming): change streams to BigQuery, Pub/Sub, Cloud Storage, Vector Search and HBase. Example to BigQuery:
```bash
gcloud dataflow flex-template run bt-cdc --region=<R> \
  --template-file-gcs-location=gs://dataflow-templates-<R>/latest/flex/Bigtable_Change_Streams_to_BigQuery \
  --parameters=bigTableReadInstanceId=<I>,bigTableReadTableId=events,bigTableChangeStreamAppProfile=cdc,bigQueryDataset=bt_cdc
```
- The app profile must use **single-cluster routing** and allow single-row transactions (change streams require single-cluster routing).
- Custom pipelines use Beam `BigtableIO.readChangeStream()` (Java), which creates and manages a metadata table for its state.

## 3. Record semantics
- Records cover cell writes, cell deletions (by column and timestamp range) and column-family deletions; row deletions are expanded into family deletions. Each change is typed as user-initiated or **garbage collection** (filter GC out if you only want user changes). `DropRowRange` deletions are included, and records carry only the new value, not the old one.
- Ordered by commit timestamp per row key and per cluster; no ordering across row keys or clusters. Partitions split and merge automatically in the Java client, Beam connector and Dataflow templates.
- In replicated instances each cluster with the table stores its own copy of the stream data; a lagging partition stalls the stream-wide low watermark.

## Gotchas
- Reads can only start from a point within the retention period.
- Avoid `DropRowRange` on change-stream tables: it can take a long time and raises CPU use.
- Schema changes and replication topology changes are not tracked.

## Verify
- [ ] A test write appears in the sink and the Dataflow job's data freshness metric stays low.

## Checked
Checked 2026-10-24 against the googleapis `google/bigtable/admin/v2/table.proto` (ChangeStreamConfig retention 1 to 7 days), the gcloud `bigtable instances tables update` reference, the Bigtable change streams overview and the GoogleCloudPlatform/DataflowTemplates README for `Bigtable_Change_Streams_to_BigQuery` (parameter names, single-cluster routing, `latest/flex` path form) and Apache Beam `BigtableIO.readChangeStream()` with its metadata table. Removed the claim that a table cannot be deleted while a stream is enabled and the claim about replicated instances emitting each change once, neither of which the documentation confirms.
Method: documentation only; no commands were run.
