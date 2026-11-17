---
id: computing-software.data-engineering.snowflake.finalizer-tasks
name: finalizer-tasks
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, finalizer-task, task-graphs, cleanup, notifications]
level: practitioner
status: docs-checked
description: "Add a Snowflake finalizer task to a task graph to always run cleanup and notifications after the graph finishes, whether it succeeded or failed."
sources:
  - https://docs.snowflake.com/en/user-guide/tasks-graphs#finalizer-task
  - https://docs.snowflake.com/en/sql-reference/sql/create-task
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finalizer tasks

**Goal:** guaranteed cleanup (drop temp tables, release locks, send a summary) at the end of every task graph run, like a `finally` block.

## Define
```sql
CREATE OR REPLACE TASK pipeline_root
  WAREHOUSE = etl_wh SCHEDULE = 'USING CRON 0 2 * * * UTC'
AS CALL start_run();

CREATE OR REPLACE TASK pipeline_finalize
  WAREHOUSE = etl_wh
  FINALIZE = pipeline_root
AS CALL finish_run();

ALTER TASK pipeline_finalize RESUME;
ALTER TASK pipeline_root RESUME;    -- resume root last
```
- A finalizer is scheduled only when no other tasks of the graph run are running or queued (task graph docs).
- One finalizer per root task; it cannot have child tasks, cannot become a predecessor and cannot have a schedule.

## Inside the finalizer: inspect the run
```sql
CREATE OR REPLACE PROCEDURE finish_run() RETURNS STRING LANGUAGE SQL AS
$$
DECLARE failed INT;
BEGIN
  SELECT count(*) INTO :failed
  FROM TABLE(information_schema.task_history(
         scheduled_time_range_start => dateadd('hour', -24, current_timestamp())))
  WHERE graph_run_group_id = '<GRAPH_RUN_GROUP_ID>'   -- the current graph run, from SYSTEM$TASK_RUNTIME_INFO
    AND state = 'FAILED';
  DROP TABLE IF EXISTS staging.tmp_orders;
  CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
    SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('pipeline finished, failed tasks: ' || :failed),
    SNOWFLAKE.NOTIFICATION.INTEGRATION('ops_email_int'));
  RETURN 'done';
END;
$$;
```
`SYSTEM$TASK_RUNTIME_INFO` reports information about the current task run (see its reference for the task-graph options); `TASK_HISTORY` has a `graph_run_group_id` column.

## Gotchas
- The finalizer does not run if the root task itself was not started (e.g. skipped due to overlap).
- Keep it fast and failure-proof.
- Combine with task-level `SUSPEND_TASK_AFTER_NUM_FAILURES` and error integrations for alerting on the root.

## Verify
Force a child failure: the finalizer still runs and the notification reports the failure.

## Checked
2026-10-28. Confirmed against CREATE TASK and the task graph page (FINALIZE, one finalizer per root, no child tasks, cannot be a predecessor, no schedule, not started when the root is skipped, SYSTEM$TASK_RUNTIME_INFO, graph_run_group_id column) and the SYSTEM$SEND_SNOWFLAKE_NOTIFICATION page. Removed: the success-failure-cancel completion claim, the CURRENT_TASK_GRAPH_RUN_GROUP_ID option name (now a placeholder) and the graph-marked-failed claim.
Method: documentation only; no commands were run.
