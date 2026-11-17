---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spanner-import-export-with-dataflow
name: spanner-import-export-with-dataflow
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spanner, spanner-import-export, dataflow-spanner, avro, backup]
level: practitioner
status: docs-checked
description: "Export a Spanner database to Avro in Cloud Storage and import it back with the Dataflow templates: sizing, priority, CSV imports, and the failure modes that waste hours."
sources: ["https://docs.cloud.google.com/spanner/docs/export", "https://docs.cloud.google.com/spanner/docs/import", "https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/main/v1/README_Cloud_Spanner_to_GCS_Avro.md", "https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/main/v1/README_GCS_Avro_to_Cloud_Spanner.md", "https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/main/v1/README_GCS_Text_to_Cloud_Spanner.md", "https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/main/v1/README_Spanner_to_GCS_Text.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spanner import and export with Dataflow

Export/import is a logical copy (Avro files plus a manifest) run as a Dataflow job. Use it to move a
database between projects or instances, seed non-prod, or keep an off-Spanner archive. For recovering a database in the same instance, consider backups or point-in-time recovery, which do not need a Dataflow job.

## 1. Export to Avro
```bash
gcloud dataflow jobs run spanner-export \
  --gcs-location=gs://dataflow-templates-<REGION>/latest/Cloud_Spanner_to_GCS_Avro \
  --region=<REGION> --staging-location=gs://<BUCKET>/staging \
  --service-account-email=df-spanner@<P>.iam.gserviceaccount.com \
  --parameters=instanceId=<INST>,databaseId=<DB>,outputDir=gs://<BUCKET>/exports,spannerPriority=LOW,snapshotTime=<RFC3339_TIME_WITHIN_RETENTION>
```
- `snapshotTime` (RFC 3339 UTC, in the past, subject to maximum timestamp staleness) reads the database at an earlier time; the default is the time of the job.
- `spannerPriority` accepts `HIGH`, `MEDIUM` (default) and `LOW`; `dataBoostEnabled=true` uses Spanner Data Boost and needs the `spanner.databases.useDataBoost` permission.
- `tableNames=` exports a subset; include all related tables (parents and foreign-key referenced tables) or set `shouldExportRelatedTables=true`.
- The console export option launches a Dataflow job for the same purpose; the output folder is named from the instance ID, database name and job timestamp and contains `spanner-export.json`, a `TableName-manifest.json` per table and Avro data files.

## 2. Import from Avro
```bash
gcloud dataflow jobs run spanner-import \
  --gcs-location=gs://dataflow-templates-<REGION>/latest/GCS_Avro_to_Cloud_Spanner \
  --region=<REGION> --staging-location=gs://<BUCKET>/staging \
  --parameters=instanceId=<INST>,databaseId=<NEW_DB>,inputDir=gs://<BUCKET>/exports/<INST>-<DB>-<JOBID>
```
- The target database must be **new**: the Spanner import documentation says the name cannot already exist in the instance, and the import creates the database and schema from the export.
- Foreign keys are created after the data load. Indexes are created after the load unless the template runs many DDL statements: with more than the `earlyIndexCreateThreshold` (default 40) indexes and foreign keys it creates indexes first. `waitForIndexes` and `waitForForeignKeys` default to `false`, so the job can finish while they are still building.
- Change streams are created after the data is imported and contain no change records.
- If instance CPU is above 65%, the job runs slower; consider adding compute capacity temporarily.

## 3. CSV import/export
Use the `GCS_Text_to_Cloud_Spanner` template (`gs://dataflow-templates-<REGION>/latest/GCS_Text_to_Cloud_Spanner`) with `importManifest=gs://<B>/manifest.json` (plus options such as `columnDelimiter`, `fieldQualifier`, `nullString`, `dateFormat`, `invalidOutputPath`). The `Spanner_to_GCS_Text` template exports one table (`spannerTable`, `textWritePrefix`, `spannerProjectId`, `spannerInstanceId`, `spannerDatabaseId`).

## Gotchas
- The Dataflow worker service account needs `roles/spanner.viewer`, `roles/dataflow.worker`, `roles/storage.admin` and `roles/spanner.databaseReader`, plus `roles/spanner.databaseAdmin` for import jobs.
- Run the Dataflow job in the same region as the Cloud Storage bucket (and pick a region matching the instance configuration) to avoid transfer charges.
- Stored generated column values are not exported (only the definition); exported change streams contain only their schema; sequences are exported with a counter buffer of 1000.

## Verify
- [ ] Job ends `JOB_STATE_DONE`; the `spanner-export.json` manifest exists in the output folder.
- [ ] Row counts per table match (`SELECT COUNT(*)` on both sides at the snapshot time).

## Checked
Checked 2026-10-24 against the Spanner export and import documentation (docs.cloud.google.com) and the GoogleCloudPlatform/DataflowTemplates v1 READMEs for `Cloud_Spanner_to_GCS_Avro`, `GCS_Avro_to_Cloud_Spanner`, `GCS_Text_to_Cloud_Spanner` and `Spanner_to_GCS_Text` (template names, `gs://dataflow-templates-REGION/latest/` path form, parameter names and defaults). Wrong claims fixed: the CSV templates are named `GCS_Text_to_Cloud_Spanner` and `Spanner_to_GCS_Text` (not `Text_Files_To_Cloud_Spanner` or `Cloud_Spanner_to_GCS_Text`); the import target must be a new database; index creation is conditional on the early-index threshold; the worker roles were listed incompletely. Removed the dialect-mismatch and 1-hour default snapshot claims, which are not documented.
Method: documentation only; no commands were run.
