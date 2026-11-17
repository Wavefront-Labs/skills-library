---
id: computing-software.data-engineering.snowflake.troubleshooting-snowpipe
name: troubleshooting-snowpipe
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowpipe, pipe-status, copy-history, validate-pipe-load, auto-ingest, sqs, event-notifications]
level: practitioner
status: docs-checked
description: "Debug Snowpipe auto-ingest that is not loading: SYSTEM$PIPE_STATUS, COPY_HISTORY, VALIDATE_PIPE_LOAD, notification channel checks, stale pipes and backfilling with REFRESH."
sources:
  - https://docs.snowflake.com/en/user-guide/data-load-snowpipe-ts
  - https://docs.snowflake.com/en/sql-reference/functions/system_pipe_status
  - https://docs.snowflake.com/en/sql-reference/functions/copy_history
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Snowpipe

**Goal:** find out quickly whether files are not arriving, notifications are not reaching Snowflake, or loads are failing.

## 1. Pipe status
```sql
select parse_json(system$pipe_status('raw.ingest.orders_pipe')) s;
```
Key fields: `executionState` (`RUNNING`, `PAUSED`, and `STOPPED_*` / `STALLED_*` states such as `STALLED_STAGE_PERMISSION_ERROR`; see the SYSTEM$PIPE_STATUS reference), `pendingFileCount`, `lastReceivedMessageTimestamp`, `lastForwardedMessageTimestamp`, `error`, `notificationChannelName`.
- `lastReceivedMessageTimestamp` old while files arrive -> notifications not reaching Snowflake.
- Received but not forwarded -> path/pattern mismatch between notification and pipe's stage path.

## 2. Load results
```sql
select file_name, status, row_count, first_error_message, last_load_time
from table(information_schema.copy_history(
  table_name => 'RAW.INGEST.ORDERS', start_time => dateadd(hour, -24, current_timestamp())))
order by last_load_time desc;

select * from table(information_schema.validate_pipe_load(
  pipe_name => 'raw.ingest.orders_pipe', start_time => dateadd(hour, -24, current_timestamp())));
```
`status`: `Loaded`, `Partially loaded`, `Load failed`. By default (ON_ERROR = SKIP_FILE) Snowpipe does not load a file that contains errors.

## 3. Notification path (S3 example)
- `notificationChannelName` in the pipe status identifies the channel; the bucket notification must send events there and its object prefix must cover the pipe's path.
- GCS: check the Pub/Sub subscription and notification integration; Azure: check the storage queue and notification integration.

## 4. Backfill / catch up
```sql
alter pipe raw.ingest.orders_pipe refresh;
```
Load any files the pipe missed as described in "Load missed files" in the Snowpipe troubleshooting docs; files that REFRESH does not cover can be loaded with a manual `COPY INTO`.

## 5. Pause / resume / stale
```sql
alter pipe orders_pipe set pipe_execution_paused = true;
select system$pipe_force_resume('raw.ingest.orders_pipe');
```
A pipe paused for more than 14 days, or whose ownership changed while it was paused, must be resumed with `SYSTEM$PIPE_FORCE_RESUME` ("Resume a stale pipe" in the Snowpipe troubleshooting docs); then load any missed files.

## Common causes
| Symptom | Cause |
|---|---|
| Nothing loaded, no messages | S3 event not configured / wrong prefix / wrong queue ARN |
| Messages, no loads | pipe `COPY` path or `PATTERN` does not match file keys |
| Load failed | file format mismatch, cast errors, encoding |
| Pipe owner changed while paused | resume with `SYSTEM$PIPE_FORCE_RESUME` |

## Verify
- [ ] `pendingFileCount` returns to 0, `copy_history` shows recent `Loaded` rows.
- [ ] Alert on `Load failed` rows in copy history (scheduled task or Snowflake alert).

## Checked
2026-10-28. Confirmed against the SYSTEM$PIPE_STATUS reference and the Snowpipe troubleshooting guide (executionState, pendingFileCount, lastReceivedMessageTimestamp, lastForwardedMessageTimestamp, notificationChannelName, COPY_HISTORY covers 14 days, STATUS values incl. Partially loaded, VALIDATE_PIPE_LOAD, ON_ERROR = SKIP_FILE default, 14-day pause and SYSTEM$PIPE_FORCE_RESUME). Removed: the staleness_check_override argument, the 7-day REFRESH window and prefix/modified_after example, the shared-SQS-queue remark, the duplicate-rows row and the notification_channel column of DESC PIPE.
Method: documentation only; no commands were run.
