---
id: computing-software.data-engineering.snowflake.snowflake-notebooks
name: snowflake-notebooks
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-notebooks, snowsight, container-runtime, scheduling]
level: practitioner
status: docs-checked
description: "Use Snowflake Notebooks: warehouse vs container runtime, packages, session idle timeout, EXECUTE NOTEBOOK and its warehouse and compute-pool behaviour."
sources:
  - https://docs.snowflake.com/en/user-guide/ui-snowsight/notebooks
  - https://docs.snowflake.com/en/user-guide/ui-snowsight/notebooks-on-spcs
  - https://docs.snowflake.com/en/sql-reference/sql/execute-notebook
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowflake Notebooks

**Goal:** interactive SQL/Python analysis and lightweight scheduled pipelines inside Snowflake.

Status note from the docs: the original notebooks were renamed Legacy Notebooks, with a next-generation Notebooks in Workspaces experience being rolled out; accounts created after April 2026 cannot create Legacy Notebooks. Check which experience your account has before following steps below.

## Runtimes (Legacy Notebooks)
| | Warehouse runtime | Container runtime |
|---|---|---|
| Kernel runs on | the notebook warehouse | a compute pool node (Snowpark Container Services) |
| Extra libraries | Snowflake Anaconda or a Snowflake stage | pip, conda, or a Snowflake stage |
| Good for | the fastest start, SQL-heavy and Snowpark work | ML training and tuning (CPU and GPU runtime images) and flexible workloads |
For both runtimes, SQL and Snowpark queries always execute on the warehouse. Git integration and scheduling were listed as Preview features for both.

## Cells
- Python, SQL and Markdown cells; reference SQL cell output from Python cells and vice versa.
- Python session: `from snowflake.snowpark.context import get_active_session; session = get_active_session()`, then `df.to_pandas()` as needed.

## Container runtime notes
- Snowflake provisions two system compute pools per account, `SYSTEM_COMPUTE_POOL_CPU` and `SYSTEM_COMPUTE_POOL_GPU`.
- Each compute node runs one notebook per user at a time, so create notebook compute pools with `MAX_NODES` greater than one.
- Install extra packages with `!pip install ...` in a code cell. Reaching a package index needs an external access integration; changing the version of a pre-installed package needs a kernel restart.
- Idle timeout defaults to 1 hour and can be set up to 72 hours (UI setting, or the `IDLE_AUTO_SHUTDOWN_TIME_SECONDS` property via `CREATE NOTEBOOK` or `ALTER NOTEBOOK`). A session can run up to seven days before it may be shut down by SPCS maintenance.

## Running outside the editor
```sql
ALTER NOTEBOOK analytics.nb.daily_report SET QUERY_WAREHOUSE = report_wh;
EXECUTE NOTEBOOK analytics.nb.daily_report();
EXECUTE NOTEBOOK analytics.nb.daily_report('target_database=PROD_DB');
```
- `EXECUTE NOTEBOOK` runs the latest code of all cells and requires `QUERY_WAREHOUSE` to be set, otherwise it errors.
- Python cells run on the compute pool set by the `RUNTIME` parameter; SQL and Snowpark queries run on the warehouse. Query History may show a warehouse for the command; it initialises the environment and, per the docs, consumes no warehouse credits for the Python work.
- Arguments are strings only (other types become NULL) and appear in `sys.argv` in a Python cell.
- You need OWNERSHIP on the notebook.
- You can nest `EXECUTE NOTEBOOK` in a task, but a task configured `EXECUTE AS USER` fails when it runs, with no error at creation.
- The notebook toolbar Scheduler button schedules a run as a task.

## Cost hygiene
End sessions you are not using and keep the idle timeout short; use a small dedicated warehouse for notebooks rather than a shared BI or ETL warehouse.

## Verify
`EXECUTE NOTEBOOK` completes (directly or from a task run), task history shows success, and the output table updates.

## Checked
2026-11-09. Confirmed against the Snowflake docs "About Legacy Snowflake Notebooks", "Notebooks on Container Runtime" and the EXECUTE NOTEBOOK reference: runtime comparison, system compute pools, one notebook per node per user, pip installs, idle timeout default and maximum, seven-day session limit, EXECUTE NOTEBOOK requirements, sys.argv arguments, OWNERSHIP, and the EXECUTE AS USER task failure. Removed as unconfirmed: Jinja variable syntax, the CREATE NOTEBOOK ... FROM git repository and ADD LIVE VERSION statements, the Anaconda package picker detail, output truncation, and the scheduled-run role claim.
Method: documentation only; no commands were run.
