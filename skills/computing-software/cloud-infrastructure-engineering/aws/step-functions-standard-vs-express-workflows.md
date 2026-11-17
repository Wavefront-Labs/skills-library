---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-standard-vs-express-workflows
name: step-functions-standard-vs-express-workflows
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, standard-workflows, express-workflows, state-machine, workflow-orchestration, cost, serverless]
level: practitioner
status: docs-checked
description: "Choose Standard or Express Step Functions workflows by duration, execution semantics, integration patterns, history and cost, and nest Express inside Standard."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html", "https://docs.aws.amazon.com/step-functions/latest/dg/service-quotas.html", "https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html", "https://docs.aws.amazon.com/step-functions/latest/apireference/API_LoggingConfiguration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions: Standard vs Express workflows

**Goal:** pick the workflow type once, correctly — `type` is fixed at creation and cannot be
changed on an existing state machine (you create a new one and repoint callers).

## 1. Decision table
| | Standard | Express |
|---|---|---|
| Max duration | 1 year | 5 minutes |
| Semantics | exactly-once per execution | async: at-least-once; sync: at-most-once |
| Start rate | token bucket per account and Region (StartExecution bucket 1,300 / refill 300 per second in us-east-1, us-west-2 and eu-west-1; 800 / 150 elsewhere) | StartExecution bucket and refill 6,000 per second; no state transition limit |
| Billing | per state transition | per execution count, duration and memory |
| History | 90 days after close in console/API (`get-execution-history`) | none unless you enable CloudWatch Logs (best-effort delivery) |
| `.sync` / `.waitForTaskToken` | supported | **not supported** |
| Redrive failed execution | yes (14 days) | no |
| Distributed Map state | supported (children can be Standard or Express) | not supported as the parent |
| Activities | supported | not supported |

Rules of thumb:
- Human approval, long waits, `.sync` jobs (Glue, ECS, Batch), audit trail needed → **Standard**.
- High-volume event processing, IoT ingestion, API backends, < 5 min, idempotent steps → **Express**.
- Cost: Standard bills per state transition and Express per execution, duration and memory; compare them with your real state count and duration (see the Step Functions pricing page) before choosing.

## 2. Create each
```bash
aws stepfunctions create-state-machine --name orders-std --type STANDARD \
  --definition file://asl.json --role-arn arn:aws:iam::<ACCOUNT_ID>:role/sfn-orders
aws stepfunctions create-state-machine --name orders-exp --type EXPRESS \
  --definition file://asl.json --role-arn arn:aws:iam::<ACCOUNT_ID>:role/sfn-orders \
  --logging-configuration '{"level":"ERROR","includeExecutionData":true,"destinations":[{"cloudWatchLogsLogGroup":{"logGroupArn":"arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/aws/vendedlogs/states/orders-exp:*"}}]}'
```
Synchronous Express (API Gateway / caller waits for the result):
```bash
aws stepfunctions start-sync-execution --state-machine-arn "$EXP_ARN" --input '{"id":"42"}'
```

## 3. The nesting pattern
Run the orchestration as Standard (long-lived, auditable) and put the high-volume inner loop in a Distributed Map whose child workflows use `"ExecutionType": "EXPRESS"`. Express workflows cannot use `.sync` or `.waitForTaskToken`. You pay Express rates for the hot inner loop and keep exactly-once at the outer level.

## Gotchas
- Express at-least-once means a step can run twice: make every Task idempotent (conditional
  writes, idempotency keys) before choosing Express.
- Express without logging is a black box — failures show only in `ExecutionsFailed` metrics.
- Standard's 25,000-event history limit per execution bites long loops; split work into child
  executions or a Distributed Map.
- Starting a Standard execution with the same name as a running execution returns an idempotent response and does not start a second one; after it completes the same name raises an exception until its history is removed after 90 days. Express starts are not idempotent. Use the business key as the execution name to stop duplicate Standard starts.

## Verify
- [ ] `aws stepfunctions describe-state-machine --state-machine-arn ... --query type` shows the intended type.
- [ ] For Express, a forced failure appears in the vended log group with `includeExecutionData` payloads.
- [ ] Monthly cost estimate written down for both types with real transitions/duration numbers.

## Checked
Checked 2026-10-24 against the Step Functions developer guide (choosing workflow type, service quotas, CloudWatch Logs) and the LoggingConfiguration API reference.
Confirmed: type is immutable, Standard one year and exactly-once, Express five minutes with at-least-once (async) and at-most-once (sync) semantics, billing bases, 90-day history, Express history only via CloudWatch Logs, .sync and .waitForTaskToken unsupported on Express, Distributed Map and activities Standard-only, redrive 14 days Standard-only, StartExecution quotas, same-name idempotency, logging configuration fields (level, includeExecutionData, destinations).
Removed as unconfirmed: start rate multipliers, cost crossover figures, the Express-child .sync:2 nesting pattern.

Method: documentation only; no commands were run.
