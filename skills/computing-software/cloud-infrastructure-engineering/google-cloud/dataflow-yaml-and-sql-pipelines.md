---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataflow-yaml-and-sql-pipelines
name: dataflow-yaml-and-sql-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataflow, dataflow-yaml, dataflow-sql, beam-yaml, low-code]
level: practitioner
status: docs-checked
description: "Write Beam YAML pipelines and run them on Dataflow with gcloud dataflow yaml run: sources, sinks, SQL and MapToFields transforms, providers, and when to move to code."
sources: ["https://cloud.google.com/dataflow/docs/guides/job-builder", "https://cloud.google.com/dataflow/docs/guides/yaml", "https://beam.apache.org/documentation/sdks/yaml/", "https://cloud.google.com/sdk/gcloud/reference/dataflow/yaml/run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataflow YAML and SQL pipelines

Legacy Dataflow SQL (the BigQuery UI editor) is deprecated; SQL now lives inside **Beam YAML** via the
`Sql` transform, and the console **Job builder** generates the same YAML.

## 1. A pipeline
`pipeline.yaml`:
```yaml
pipeline:
  type: chain
  transforms:
    - type: ReadFromPubSub
      config: {topic: projects/<P>/topics/orders, format: JSON,
               schema: {type: object, properties: {id: {type: string}, amount: {type: number}, country: {type: string}}}}
    - type: WindowInto
      windowing: {type: fixed, size: 60s}
    - type: Sql
      config: {query: "SELECT country, SUM(amount) AS revenue FROM PCOLLECTION GROUP BY country"}
    - type: WriteToBigQuery
      config: {table: <P>:mart.revenue_by_minute, write_disposition: WRITE_APPEND}
options:
  streaming: true
```
Other transforms: `Filter` (`keep: "amount > 0"`), `MapToFields` (expressions in `python`/`sql`/`javascript`),
`Join`, `Combine`, `ReadFromText`, `WriteToJson`, Kafka, Spanner, Iceberg.

## 2. Run
```bash
gcloud dataflow yaml run revenue-$(date +%s) --yaml-pipeline-file=pipeline.yaml \
  --region=<R> --service-account-email=df-runner@<P>.iam.gserviceaccount.com
# local check first
python -m apache_beam.yaml.main --yaml_pipeline_file=pipeline.yaml --runner=DirectRunner
```
Jinja templating (`--jinja_variables`) parameterises tables and topics per environment.

## 3. Graduate to code when
You need custom stateful DoFns, timers, complex error-handling branches, unit tests per transform, or
connectors YAML lacks. YAML supports `error_handling: {output: errors}` on many transforms for dead-letter routing.

## Gotchas
- Schemas are required for SQL: sources without schema (raw text) need `MapToFields` first.
- Cross-language transforms (Java Kafka/BigQuery) start an expansion service; first run is slower.

## Verify
- [ ] DirectRunner run on sample data produces expected rows before the Dataflow launch; the Dataflow job graph shows each YAML transform.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the BigQuery read transform name and the create_disposition setting.

Method: documentation only; no commands were run.
