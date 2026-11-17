---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-pipes-with-enrichment
name: eventbridge-pipes-with-enrichment
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, eventbridge-pipes, pipes, enrichment, point-to-point, sqs-to-step-functions, dynamodb-streams-pipe, kinesis-pipe, pipe-filtering, pipe-batching, pipe-logging, pipe-dlq, event-driven]
level: practitioner
status: docs-checked
description: "Build EventBridge Pipes: source (SQS, Kinesis, DynamoDB Streams, MSK, MQ) to target with filtering, enrichment, batching, concurrency limits, logging and metrics."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-filtering.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-logs.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-batching-concurrency.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-monitoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge Pipes with enrichment

**Goal:** a managed point-to-point integration (queue/stream → target) with filtering and a
transform/enrich step, replacing the "poller Lambda that calls another service then starts a
workflow" boilerplate.

## 1. Anatomy
`Source` (API model: SQS, Kinesis, DynamoDB Streams, Amazon MQ ActiveMQ and RabbitMQ, MSK, self-managed Kafka) → optional
**filter** (EventBridge pattern syntax on the source record) → optional **enrichment**
(the Pipes overview example uses an API destination; Lambda and Step Functions are documented as batch-capable enrichments) → **target** (see the supported targets list in the Pipes guide).
You are charged only for events that match the filter. If events are batched, enrichment keeps their order.

```bash
aws pipes create-pipe --name orders-to-sfn --role-arn arn:aws:iam::<ACCOUNT_ID>:role/pipes-orders \
  --source arn:aws:sqs:<REGION>:<ACCOUNT_ID>:orders \
  --source-parameters '{"SqsQueueParameters":{"BatchSize":10,"MaximumBatchingWindowInSeconds":5},
                        "FilterCriteria":{"Filters":[{"Pattern":"{\"body\":{\"type\":[\"order.paid\"]}}"}]}}' \
  --enrichment arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:lookup-customer \
  --enrichment-parameters '{"InputTemplate":"{\"orderId\": <$.body.orderId>}"}' \
  --target arn:aws:states:<REGION>:<ACCOUNT_ID>:stateMachine:fulfil \
  --target-parameters '{"StepFunctionStateMachineParameters":{"InvocationType":"FIRE_AND_FORGET"}}' \
  --log-configuration '{"CloudwatchLogsLogDestination":{"LogGroupArn":"arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/aws/pipes/orders"},"Level":"ERROR","IncludeExecutionData":["ALL"]}'
```
The pipe role needs permissions for the source, the enrichment and the target; take the exact action lists from the Pipes permissions page for each service.

## 2. Filtering
Same pattern language as rules, applied to the **source record shape**. Content is either JSON-escaped (the SQS `body` field) or base64-encoded (the Kinesis `data` field); if the data is valid JSON, patterns can reference its fields. A message that does not match an SQS filter is removed from the queue automatically, so several pipes competing on one SQS queue drop each other's unmatched messages. For Kafka and Amazon MQ sources, a filter change can take up to 15 minutes to apply. A pipe accepts at most 5 filters (API model).

## 3. Enrichment
- When batching is on at the source, arrays of JSON records go through the pipe. Input transformers apply to each record separately, not to the array.
- Lambda and Step Functions enrichments receive the whole JSON array in one request (even for batch size 1). Enrichment can return an array shorter or longer than the input, but if it is larger than the target's batch limit the pipe does not invoke the target.
- Include the original item identifiers (SQS `messageId`; Kinesis and DynamoDB `eventID`) in the enrichment output so partial batch failures can be handled. Partial batch failure handling of the enrichment itself is not supported.
- Metric `TargetStageSkipped` counts target stages skipped, for example when the enrichment returns an empty payload.
- Input templates run per record; check the input-transformation page before relying on array references.

## 4. Batching, concurrency, ordering
- You cannot configure a larger source batch size than the target supports (SQS, SNS and EventBridge bus targets accept 10, Kinesis and Firehose 500, CloudWatch Logs 10,000). If the enrichment or target cannot batch, you cannot turn batching on at the source.
- Kinesis source parameters (API model): `BatchSize` up to 10,000, `ParallelizationFactor` 1-10, `StartingPosition` (`TRIM_HORIZON`, `LATEST`, `AT_TIMESTAMP`), `MaximumRetryAttempts`, `MaximumRecordAgeInSeconds`, `OnPartialBatchItemFailure: AUTOMATIC_BISECT`, `DeadLetterConfig`. SQS source parameters: `BatchSize` (1-10,000 in the API model) and `MaximumBatchingWindowInSeconds` (0-300).
- Partial batch failure: for SQS and stream sources, if a batching target succeeds for only part of the batch the pipe retries the remainder through the whole pipe, including the enrichment. Lambda and Step Functions targets can return `batchItemFailures` with `itemIdentifier`.
- Default maximum concurrency per pipe: SQS 1250, Amazon MQ 5, Kafka up to the partition count (max 1000), Kinesis and DynamoDB `ParallelizationFactor` x shards. Execution (enrichment plus target) is limited to 5 minutes. Ordered sources (FIFO, Kinesis, DynamoDB, Kafka) cannot exceed their ordering concurrency.

## 5. Logging and metrics
Log `Level` is one of `OFF`, `ERROR`, `INFO`, `TRACE`; `IncludeExecutionData: ["ALL"]` adds payloads. Log destinations are CloudWatch Logs, Firehose and S3. A log record covers one batch (up to 10,000 events).
Metrics (Pipes monitoring page; best-effort delivery, dimension `PipeName`): `Invocations`, `EventCount`, `Duration`, `ExecutionFailed`, `ExecutionPartiallyFailed`, `ExecutionThrottled`, `ExecutionTimeout`, `EnrichmentStageFailed`, `EnrichmentStageDuration`, `TargetStageFailed`, `TargetStagePartiallyFailed`, `TargetStageDuration`, `TargetStageSkipped`, `Concurrency`.
Pipe states in the API model include `RUNNING`, `STOPPED`, `CREATING`, `CREATE_FAILED`, `UPDATE_FAILED` and `START_FAILED`; check `describe-pipe` after creating a pipe.

## Gotchas
- The target gets records in the **enrichment output's shape**; forgetting to echo item identifiers breaks partial-failure handling.
- Step Functions state machine target `InvocationType` is `REQUEST_RESPONSE` or `FIRE_AND_FORGET` (API model). Which state machine type each mode supports, and whether Standard workflows can act as enrichment, is not confirmed here; check the Pipes target and enrichment pages.
- Set the SQS visibility timeout with the 5-minute execution limit in mind.

## Verify
- [ ] Send a matching message: pipe log shows source → enrichment → target stages and the state machine starts with enriched input.
- [ ] A non-matching message is consumed (queue drains) and no target invocation occurs.
- [ ] An enrichment failure increments `EnrichmentStageFailed` in `PipeName` metrics.

## Checked
2026-10-27. Documentation: Amazon EventBridge User Guide (Pipes overview, event filtering, logging, batching and concurrency, monitoring), read this date. Confirmed: batch targets and sizes, partial batch failure behaviour and batchItemFailures format, default concurrency per source and 5-minute execution limit, filtering behaviour for SQS and Kafka/MQ, log levels and destinations, metric names (the draft's EnrichmentFailed, TargetFailed and ConcurrentExecutions are not the documented names; the real ones are EnrichmentStageFailed, TargetStageFailed and Concurrency). Confirmed from the Pipes API model (botocore pipes 2015-10-07): at most 5 filters, SQS BatchSize 1-10,000 (the draft said up to 10), Kinesis parameter names and ranges, LogLevel enum, pipe state values (the draft's RUNNING/STOPPED/FAILED is incomplete). Removed unconfirmed enrichment type rules, IAM action lists and stack-specific gotchas.
Method: documentation only; no commands were run.
