---
id: computing-software.data-engineering.etl-pipeline-design.cloud-workflow-services-step-functions-and-workflows
name: cloud-workflow-services-step-functions-and-workflows
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, step-functions, cloud-workflows, orchestration, serverless]
level: advanced
status: docs-checked
description: "Orchestrate pipelines with cloud-native workflow services (AWS Step Functions, Google Cloud Workflows): state machines, retries, map states and limits."
sources:
  - https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html
  - https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html
  - https://cloud.google.com/workflows/docs/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud-native workflow services

**Goal:** serverless orchestration for event-driven or small pipelines without running Airflow.

## AWS Step Functions
```json
{
  "StartAt": "StartGlueJob",
  "States": {
    "StartGlueJob": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {"JobName": "orders-transform", "Arguments": {"--date.$": "$.date"}},
      "Retry": [{"ErrorEquals": ["States.ALL"], "IntervalSeconds": 60, "MaxAttempts": 3, "BackoffRate": 2.0}],
      "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "NotifyFailure"}],
      "Next": "LoadPartitions"
    },
    "LoadPartitions": {
      "Type": "Map", "ItemsPath": "$.partitions", "MaxConcurrency": 10,
      "ItemProcessor": {"StartAt": "Load", "States": {"Load": {"Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke", "Parameters": {"FunctionName": "load-partition", "Payload.$": "$"}, "End": true}}},
      "End": true
    },
    "NotifyFailure": {"Type": "Task", "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {"TopicArn": "arn:aws:sns:eu-west-1:123:data-alerts", "Message.$": "$.Cause"}, "End": true}
  }
}
```
- `.sync` (Run a Job) integrations wait for the job to finish. The service integration table lists which services support it, and only on Standard workflows (for example Athena, AWS Batch, ECS/Fargate and EMR); `.waitForTaskToken` is a separate callback pattern.
- Standard workflows: exactly-once workflow execution, up to one year. Express workflows: high event rate, at-least-once execution (one or more steps can run more than once), up to five minutes.
- Distributed Map is a Map variant with its own failure thresholds. Check its current limits and the payload size limit between states in the Step Functions quotas page, and pass references (S3 keys) rather than large data.

## Google Cloud Workflows
Fully managed orchestration; workflows are written in YAML or JSON and can combine Cloud Run or Cloud Run functions, Google Cloud services such as BigQuery, and any HTTP-based API. Connectors simplify calling Google Cloud APIs. A workflow can hold state, retry, poll, or wait for up to a year. Parallel steps run a branch or loop concurrently, and Cloud Scheduler can run a workflow on a schedule. For logic too complex for Workflows expressions, the docs advise putting the work in a Cloud Run service or function.

## When to use vs Airflow/Dagster
| Workflow services | Airflow/Dagster |
|---|---|
| event-driven, per-file or per-request | many scheduled DAGs, backfills, cross-team lineage |
| few steps, cloud-service calls | rich operators, data-aware scheduling, UI for data teams |
| no infrastructure | needs a platform (or managed service) |
Backfills and date-partitioned reruns are clumsy in workflow services; build an input list and use Map.

## Verify
Execution history shows retries working on a forced failure, the Catch path notifies, and Map concurrency stays within downstream limits.

## Checked
Date: 2026-11-09. Confirmed from the Step Functions welcome page (Standard vs Express guarantees and durations, Run a Job .sync vs .waitForTaskToken, Retry/Catch) and Handling errors page (Retry/Catch fields, Distributed Map failure thresholds), and the Google Workflows overview (YAML/JSON, connectors, parallel steps, Cloud Scheduler, up to a year). The JSON example is illustrative (its ARNs, account placeholders and the `--date` argument are not from the pages). Removed: per-transition pricing, the millions-of-objects Distributed Map claim, the 256 KB payload figure (not on the read pages), Azure Logic Apps (no source), Dataflow/Eventarc/callback claims for Google Workflows. Not read: Step Functions quotas page.
Method: documentation only; no commands were run.
