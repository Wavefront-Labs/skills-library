---
id: computing-software.data-engineering.data-warehouse-architecture.data-retention-policies
name: data-retention-policies
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-governance, data-retention-policy, storage-limitation, legal-hold, right-to-erasure, partition-expiration, time-travel, data-deletion, partition-retention]
level: practitioner
status: verified
description: "Define and implement data retention: retention schedule per data class, legal holds, automated deletion per platform, time travel and backup side effects, erasure requests and proof of deletion."
sources:
  - https://gdpr-info.eu/art-5-gdpr/
  - https://gdpr-info.eu/art-12-gdpr/
  - https://docs.snowflake.com/en/user-guide/data-failsafe
  - https://docs.snowflake.com/en/user-guide/tables-temp-transient
  - https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
  - https://kafka.apache.org/documentation/#topicconfigs
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Data retention policies

**Goal:** keep data exactly as long as it's needed or legally required, delete it reliably afterwards everywhere it was copied, and be able to prove it.

## 1. Retention schedule
Build with legal/compliance and data owners; one row per data class:
| Data class | Retention | Trigger | Basis | Action at end |
|---|---|---|---|---|
| Raw clickstream with IPs | 90 days | event date | legitimate interest, minimisation | delete |
| Customer account data | account life + 2 years | account closure | contract | delete or anonymise |
| Financial transactions | jurisdiction-specific statutory period (often 6-10 years) | fiscal year end | tax/accounting law | delete |
| Aggregated KPIs (no personal data) | indefinite | — | — | keep |
GDPR's storage-limitation principle (Art. 5(1)(e): kept in identifiable form "no longer than is necessary", with exceptions for archiving, research and statistics) requires personal data not be kept longer than necessary — "keep everything forever" is not a policy. Anonymised aggregates are outside personal-data rules if truly non-identifying.

## 2. Implement per platform
- **BigQuery**: `partition_expiration_days` on tables (e.g. `ALTER TABLE ... SET OPTIONS (partition_expiration_days = 5)`; NULL removes it), default table/partition expiration on datasets.
- **Snowflake**: scheduled task `DELETE ... WHERE event_date < DATEADD(day, -90, CURRENT_DATE)`; deleted data remains in Time Travel (`DATA_RETENTION_TIME_IN_DAYS`) and then Fail-safe (7 days, non-configurable, permanent tables) — account for that in "deleted by" commitments; transient tables have no Fail-safe and Time Travel of at most 1 day.
- **Delta/Databricks**: `DELETE` then `VACUUM` after the retention window — until VACUUM, deleted rows are still in old files reachable by time travel.
- **Iceberg**: `DELETE` + `expire_snapshots` + `remove_orphan_files`.
- **Object storage**: lifecycle expiration rules on raw prefixes (never under table-format paths).
- **Kafka**: `retention.ms` per topic; compacted topics need tombstones per key, which are kept for `delete.retention.ms` (both are Kafka topic configs).
Partition by the retention trigger date so deletion is a cheap partition drop rather than a scan-and-rewrite.

## 3. Copies and side effects
Inventory where each data class flows: replicas, dev/test copies, extracts, BI caches/imports, ML training sets, backups, logs. Retention must apply to each (backups usually expire on their own cycle — document that erasure completes when the last backup ages out).

## 4. Legal holds
A legal hold suspends deletion for specified data (litigation, investigation). Implement as a hold table consulted by deletion jobs (`WHERE customer_id NOT IN (SELECT id FROM gov.legal_holds WHERE active)`), with owner and expiry review. Object storage: S3 Object Lock offers retention periods and legal holds (a version can have either or both). Not run here: the platform statements (BigQuery, Snowflake, Delta, Iceberg, Kafka, S3) are from their documentation; this is not legal advice, so have counsel confirm retention periods and basis for your jurisdiction.

## 5. Erasure requests (right to erasure)
- Map subject identifiers to every table holding them (via PII classification tags + lineage).
- Pipeline: request → verify → delete/anonymise across all layers → VACUUM/expire → confirm. Track SLA (GDPR Art. 12(3): one month from receipt, extendable by two further months where necessary, with notice to the data subject within the first month).
- Rebuild aggregates if they'd remain identifying.

## 6. Prove it
Deletion jobs log (table, criteria, rows deleted, run time). Monthly control: query for records older than retention per class — result must be zero (excluding holds).

## Verify
- [ ] Every data class in the catalog has a retention rule and an automated job.
- [ ] Control queries find no data beyond retention.
- [ ] Time travel / Fail-safe / backup lag is documented in the policy.
