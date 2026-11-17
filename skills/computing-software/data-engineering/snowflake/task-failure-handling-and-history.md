---
id: computing-software.data-engineering.snowflake.task-failure-handling-and-history
name: task-failure-handling-and-history
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, tasks, task-history, suspend-task-after-num-failures, task-auto-retry, error-integration, task-graph, monitoring]
level: practitioner
status: docs-checked
description: "Monitor and harden Snowflake tasks: TASK_HISTORY queries, auto-suspend after N failures, TASK_AUTO_RETRY_ATTEMPTS, error notifications, and retrying failed task graphs."
sources:
  - https://docs.snowflake.com/en/user-guide/tasks-monitor
  - https://docs.snowflake.com/en/sql-reference/functions/task_history
  - https://docs.snowflake.com/en/user-guide/tasks-errors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task failure handling and TASK_HISTORY

**Goal:** failed Snowflake tasks are noticed, retried sensibly, and do not silently stop forever.

## Inspect runs
```sql
-- last 24h, recent first (information_schema table function)
select name, state, error_code, error_message, scheduled_time, completed_time, attempt_number, graph_run_group_id
from table(information_schema.task_history(
  scheduled_time_range_start => dateadd(hour, -24, current_timestamp()),
  result_limit => 200))
order by scheduled_time desc;

-- longer history (account_usage: 1 year, up to ~45 min latency)
select name, state, count(*) from snowflake.account_usage.task_history
where scheduled_time > dateadd(day, -30, current_timestamp()) group by 1,2;

-- graph runs
select * from table(information_schema.complete_task_graphs(result_limit => 20));
select * from table(information_schema.current_task_graphs());
```
States: `SCHEDULED`, `EXECUTING`, `SUCCEEDED`, `FAILED`, `SKIPPED` (the WHEN condition returned false), `CANCELLED`, `FAILED_AND_AUTO_SUSPENDED`.

## Hardening settings
```sql
alter task etl.root_task set
  suspend_task_after_num_failures = 3        -- auto-suspend after consecutive failures (default 10)
  task_auto_retry_attempts = 2               -- root task: retry the task graph when a child fails
  user_task_timeout_ms = 3600000             -- kill runaway runs
  error_integration = my_sns_error_int;      -- notify through a notification integration
```
- `TASK_AUTO_RETRY_ATTEMPTS` is set on the root task; when a child task fails the entire task graph is retried up to that many times.
- `ERROR_INTEGRATION` sends notifications for task errors.
- Or attach a **finalizer task** to the root to always run cleanup/notification at graph end.

## Manual retry
```sql
execute task etl.root_task retry last;   -- rerun the last failed graph from failed tasks
execute task etl.root_task;              -- new run now
```
After auto-suspension: fix the cause, then `alter task etl.root_task resume;` (resume children first if they were suspended separately; `select system$task_dependents_enable('etl.root_task');` resumes the whole graph).

## Alerting via SQL alert
```sql
create or replace alert ops.task_failures
  warehouse = OPS_WH schedule = '10 minute'
  if (exists (select 1 from table(information_schema.task_history(
        scheduled_time_range_start => dateadd(minute, -10, current_timestamp())))
      where state = 'FAILED'))
  then call system$send_email('ops_email_int', 'data-oncall@example.com', 'Snowflake task failed', 'Check TASK_HISTORY');
alter alert ops.task_failures resume;
```

## Gotchas
- Resume tasks after creating them (`ALTER TASK ... RESUME`).
- Owner role needs `EXECUTE TASK` on account (and `EXECUTE MANAGED TASK` for serverless).
- Overlapping runs: see `OVERLAP_POLICY` in CREATE TASK (`ALLOW_OVERLAPPING_EXECUTION` is deprecated).

## Verify
- [ ] Error integration or alert fires on a forced failure (e.g. `select 1/0` task).
- [ ] No task in `FAILED_AND_AUTO_SUSPENDED` state without a ticket.

## Checked
2026-10-28. Confirmed against the CREATE TASK, TASK_HISTORY and task graph pages (task states incl. FAILED_AND_AUTO_SUSPENDED and SKIPPED, SUSPEND_TASK_AFTER_NUM_FAILURES default 10 on the root, TASK_AUTO_RETRY_ATTEMPTS retries the whole graph, USER_TASK_TIMEOUT_MS, ERROR_INTEGRATION, EXECUTE TASK ... RETRY LAST, SYSTEM$TASK_DEPENDENTS_ENABLE, EXECUTE MANAGED TASK, COMPLETE_TASK_GRAPHS, account_usage task_history 365 days with 45 minute latency, alerts created suspended). Fixed: auto retry reruns the whole graph, not only failed tasks; SKIPPED means WHEN was false; ALLOW_OVERLAPPING_EXECUTION is deprecated. Removed: 7-day information_schema retention, Snowpipe error remark and the suspend-root-first claim.
Method: documentation only; no commands were run.
