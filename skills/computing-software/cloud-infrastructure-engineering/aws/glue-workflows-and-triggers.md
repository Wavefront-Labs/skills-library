---
id: computing-software.cloud-infrastructure-engineering.aws.glue-workflows-and-triggers
name: glue-workflows-and-triggers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, glue, glue-workflows, glue-triggers, conditional-trigger, event-trigger, etl-orchestration]
level: practitioner
status: docs-checked
description: "Orchestrate Glue jobs and crawlers with triggers (scheduled, conditional, on-demand, EventBridge) and workflows with run properties, resume, and when Step Functions fits better."
sources: ["https://docs.aws.amazon.com/glue/latest/dg/workflows_overview.html", "https://docs.aws.amazon.com/glue/latest/dg/about-triggers.html", "https://docs.aws.amazon.com/glue/latest/dg/starting-workflow-eventbridge.html", "https://docs.aws.amazon.com/glue/latest/dg/trigger-job.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Glue workflows and triggers

## Trigger types
| Type | Fires |
|---|---|
| `SCHEDULED` | cron (`cron(15 2 * * ? *)`) |
| `CONDITIONAL` | when watched jobs reach SUCCEEDED / STOPPED / FAILED / TIMEOUT, or crawlers reach SUCCEEDED / FAILED / CANCELLED (`AND` or `ANY`) |
| `ON_DEMAND` | manual `start-trigger` or workflow start |
| `EVENT` | EventBridge events, with batch size and batch window |

Event trigger batching: batch size defaults to 1 (fires on the first event); with a batch size
of 10 and no window, it fires on 10 events or 15 minutes after the first event, whichever comes
first. Glue gives no guaranteed delivery or deduplication of EventBridge messages, so make
the workflow idempotent. A run is not started if it would exceed the workflow's concurrency limit.

## Workflow example
```bash
aws glue create-workflow --name nightly-orders --max-concurrent-runs 1
aws glue create-trigger --name start --workflow-name nightly-orders --type SCHEDULED \
  --schedule "cron(0 2 * * ? *)" --actions CrawlerName=raw-orders-crawler --start-on-creation
aws glue create-trigger --name after-crawl --workflow-name nightly-orders --type CONDITIONAL \
  --predicate '{"Conditions":[{"LogicalOperator":"EQUALS","CrawlerName":"raw-orders-crawler","CrawlState":"SUCCEEDED"}]}' \
  --actions JobName=orders-curate --start-on-creation
aws glue create-trigger --name on-fail --workflow-name nightly-orders --type CONDITIONAL \
  --predicate '{"Logical":"ANY","Conditions":[{"LogicalOperator":"EQUALS","JobName":"orders-curate","State":"FAILED"}]}' \
  --actions JobName=notify-failure --start-on-creation
```

## Run properties
Share state between steps of one run:
```python
glue = boto3.client("glue")
props = glue.get_workflow_run_properties(Name=args["WORKFLOW_NAME"], RunId=args["WORKFLOW_RUN_ID"])["RunProperties"]
glue.put_workflow_run_properties(Name=args["WORKFLOW_NAME"], RunId=args["WORKFLOW_RUN_ID"],
                                 RunProperties={"batch_date": "2026-10-18"})
```
`args` comes from the job's resolved arguments; check the workflow run-properties page for how
a workflow-started job obtains its workflow name and run id.

## Operate
- `aws glue get-workflow-run --name nightly-orders --run-id ... --include-graph` shows node states.
- **Resume** a failed run after fixing the job: `aws glue resume-workflow-run --name ... --run-id ... --node-ids <node ids to resume>` (`--node-ids` is required).

## When to use Step Functions or MWAA instead
- Branching logic, retries with backoff, calls to non-Glue services, human approvals, cross-account steps: Step Functions.
- Large DAG estates with existing Airflow skills: MWAA.
Glue workflows suit simple crawler -> job chains entirely inside Glue.

## Verify
- [ ] Workflow graph shows expected edges; a forced job failure fires the failure path and alert.
- [ ] Resume of a failed run completes the remaining nodes.

## Checked

2026-10-28. Confirmed against the Glue developer guide pages on workflows, triggers and EventBridge event triggers and the glue botocore model: trigger types (SCHEDULED, CONDITIONAL, ON_DEMAND, EVENT), watched job and crawler states, event batch size and window defaults, no guaranteed delivery or deduplication, workflow concurrency limit behaviour, ResumeWorkflowRun requiring NodeIds, GetWorkflowRun IncludeGraph, CLI shapes. Removed (unconfirmed): WORKFLOW_NAME/WORKFLOW_RUN_ID argument claim, completed-nodes-not-rerun claim, Glue job state change event and bookmarks bullets, glue:startJobRun.sync name. Read end to end.

Method: documentation only; no commands were run.
