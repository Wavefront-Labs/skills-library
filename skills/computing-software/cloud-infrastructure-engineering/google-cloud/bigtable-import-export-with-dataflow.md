---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigtable-import-export-with-dataflow
name: bigtable-import-export-with-dataflow
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigtable, bigtable-import-export, bigtable-dataflow, sequencefile, hbase-migration]
level: practitioner
status: docs-checked
description: "Move Bigtable data with the Dataflow templates: export to Avro, Parquet or SequenceFile, import into a pre-created table, HBase snapshot imports, and throughput tuning."
sources: ["https://docs.cloud.google.com/bigtable/docs/import-export", "https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/main/v1/README_Cloud_Bigtable_to_GCS_Avro.md", "https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/main/v1/README_GCS_Avro_to_Cloud_Bigtable.md", "https://github.com/googleapis/cloud-bigtable-cbt-cli/blob/main/cbtdoc.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bigtable import and export with Dataflow

## 1. Export
```bash
gcloud dataflow jobs run bt-export --region=<R> \
  --gcs-location=gs://dataflow-templates-<R>/latest/Cloud_Bigtable_to_GCS_Avro \
  --parameters=bigtableProjectId=<P>,bigtableInstanceId=<I>,bigtableTableId=events,outputDirectory=gs://<B>/bt/events/,filenamePrefix=events-
```
Templates exist for Avro, Parquet, SequenceFile and JSON exports. The optional `bigtableAppProfileId` parameter selects the app profile (the instance default is used otherwise); point it at an app profile that routes to a dedicated cluster so exports do not hurt serving latency.

## 2. Import
Create the table and column families first, matching the source:
```bash
cbt -project=<P> -instance=<I> createtable events "families=cf1:maxversions=1,cf2:maxage=30d"
gcloud dataflow jobs run bt-import --region=<R> \
  --gcs-location=gs://dataflow-templates-<R>/latest/GCS_Avro_to_Cloud_Bigtable \
  --parameters=bigtableProjectId=<P>,bigtableInstanceId=<I>,bigtableTableId=events,inputFilePattern=gs://<B>/bt/events/events-*
```
- `cbt createtable` also accepts `splits=<row-key>,...` to pre-split the table on the source's row-key boundaries.
- Watch Bigtable CPU during the load and add nodes if needed.

## 3. From HBase
Export the HBase data to SequenceFiles in Cloud Storage, then run the `GCS_SequenceFile_to_Cloud_Bigtable` template (its parameters are `bigtableProject`, `bigtableInstanceId`, `bigtableTableId` and `sourcePattern`). For snapshot-based and online migrations follow the Bigtable HBase migration guide.

## Gotchas
- Garbage-collection policies apply after import: a `maxage` shorter than the data age can delete it later.
- Running Dataflow in another region than Bigtable adds network transfer and latency.

## Verify
- [ ] `cbt count events` (or a sampled read) matches the source.

## Checked
Checked 2026-10-24 against the GoogleCloudPlatform/DataflowTemplates v1 READMEs (`Cloud_Bigtable_to_GCS_Avro`, `GCS_Avro_to_Cloud_Bigtable`, `GCS_SequenceFile_to_Cloud_Bigtable`: template names, `gs://dataflow-templates-REGION/latest/...` path form, parameter names, `bigtableAppProfileId`), the cbt CLI documentation (`createtable` families and splits syntax, `count`) and the Bigtable import and export overview (docs.cloud.google.com). Removed the Data Boost export claim, rebalance-time figure, CPU threshold, overwrite semantics and HBase snapshot tooling details, which were not confirmed.
Method: documentation only; no commands were run.
