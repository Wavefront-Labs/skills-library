---
id: computing-software.cloud-infrastructure-engineering.datadog.log-archives
name: log-archives
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, log-archives, s3-archive, rehydration, log-forwarding]
level: practitioner
status: docs-checked
description: "Archive all ingested logs to your own object storage and rehydrate them on demand."
sources: ["https://docs.datadoghq.com/logs/log_configuration/archives/", "https://docs.datadoghq.com/logs/log_configuration/rehydrating/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log archives and rehydration
Goal: cheap long-term retention and audit.

```
# Logs > Configuration > Archives > New Archive
Destination: S3 bucket example-logs-archive, optional prefix /datadog/
Query: * (all logs)
Advanced: include all log tags (on by default), encryption, storage class
```

IAM policy sketch for the archive role (placeholders):

```json
{"Effect":"Allow","Action":["s3:PutObject","s3:GetObject"],"Resource":["arn:aws:s3:::example-logs-archive/*"]}
{"Effect":"Allow","Action":"s3:ListBucket","Resource":"arn:aws:s3:::example-logs-archive"}
```

- Archives take all ingested logs, indexed or not, so excluded logs are archived too (an archive's query filters what goes in).
- Files are compressed JSON (zstd `.json.zst` by default, or gzip `.json.gz`) under `dt=<YYYYMMDD>/hour=<HH>/` directories below your prefix.
- `PutObject` is enough for uploading; `GetObject` and `ListBucket` are needed for rehydration and Archive Search.
- Rehydration brings archived logs into the Log Explorer as a historical index (up to 1 billion events per historical view), which is the way to analyse old logs or logs excluded from indexing. A new view stays PENDING until ready. All scanned and indexed logs are billed.
- Order archives carefully: the first matching archive wins, so a catch-all `*` placed first receives everything.
- Other targets: Azure Storage and Google Cloud Storage.

Gotcha: a permissions or bucket mistake leaves the archive in an error state and nothing is written. Check the archive status after creating it (hover for error details; an event is also generated that you can monitor) and set an S3 lifecycle configuration for retention. Tags you use in rehydration queries must be archived with the logs.

Test a rehydration before you need it in an incident. Optionally set a max scan size per archive to limit Archive Search and rehydration cost.

## Verify
- Archive state shows no error and objects appear in the bucket; the docs say to check back in 15 minutes.

## Checked
2026-11-09. Confirmed against the Log Archives and Rehydrating pages (all ingested logs forwarded, indexed or not; zstd default and gzip; dt/hour directory layout; PutObject, GetObject and ListBucket roles; 15-minute check; error details and events; archive ordering; SSE options; lifecycle configuration; max scan size; 1 billion event limit; PENDING state; billing note). Removed: the claim "encrypt the bucket" as a requirement (encryption is optional in the docs), the claim that archive tag `team:platform` is added by a "Tags added" field (replaced by the documented include-all-tags setting), the "within about 15 minutes" guarantee (the docs only say frequency can vary and to check back in 15 minutes), "per-environment prefixes" advice, and the compliance-retention advice.
Method: documentation only; no commands were run.
