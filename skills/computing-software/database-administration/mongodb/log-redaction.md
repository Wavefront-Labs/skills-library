---
id: computing-software.database-administration.mongodb.log-redaction
name: log-redaction
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, log-redaction, redactclientlogdata, mongodb-security, mongodb-logs, pii]
level: practitioner
status: docs-checked
description: "Keep personal data out of MongoDB logs with redactClientLogData, slow query log settings and audit filters, and know what redaction does and does not cover."
sources:
  - https://www.mongodb.com/docs/manual/administration/monitoring/#log-redaction
  - https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-security.redactClientLogData
  - https://www.mongodb.com/docs/manual/reference/log-messages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log redaction

**Goal:** slow-query and error logs regularly print full documents and query values (emails, card fragments); keep that out of log files and log pipelines.

## Enable (Enterprise and Atlas)
```yaml
security:
  redactClientLogData: true
```
At runtime without restart:
```javascript
db.adminCommand({ setParameter: 1, redactClientLogData: true })
```
The message accompanying each log event is redacted: values in logged commands and documents become `"###"` (including the value of the command name key such as the collection in `insert`), while field names, error and operation codes, line numbers and source file names stay visible. Diagnosis can be harder because less data is logged. Set it at startup with `security.redactClientLogData` or `--redactClientLogData` (not `--setParameter`).

## What it does not cover
- The setting redacts the diagnostic log; review other outputs separately: the profiler's `system.profile` collection, the audit log (use audit filters to limit what is captured) and driver/application logs.
- FTDC never contains query samples or data from user collections.
- `redactClientLogData` is available in MongoDB Enterprise and Atlas only. Without it, reduce exposure with a higher `slowms`, lower log verbosity and scrubbing in the log shipper.
- Queryable Encryption has its own redaction parameter (`redactEncryptedFields`, 6.1+).

## Supporting settings
```javascript
db.setProfilingLevel(0, { slowms: 200, sampleRate: 0.1 })   // fewer slow-op entries
db.setLogLevel(0)                                            // avoid debug levels in prod
```
Keep log verbosity low in production; higher verbosity logs more events.

## Gotchas
- Redaction makes reproducing a slow query harder: capture query shapes from `$queryStats` (enabled on Atlas M10 and above) or the plan cache instead.
- Turning it on does not clean old logs; rotate (`db.adminCommand({logRotate: 1})`) and purge historical files under your retention policy.

## Verify
Run a query on a known value, then `grep` the log: the value should appear as `###`.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: security.redactClientLogData and the redactClientLogData parameter (Enterprise; Atlas and Enterprise per the log redaction page), runtime setParameter on a running process and not via --setParameter at startup, redacted values replaced with ### while field names, codes and source locations remain, FTDC excludes query and user data, redactEncryptedFields (6.1) for Queryable Encryption, setProfilingLevel slowms and sampleRate, $queryStats available on Atlas M10 and above, logRotate. Removed unconfirmed profiler-content, namespace-retention and $queryStats version claims.

Method: documentation only; no commands were run.
