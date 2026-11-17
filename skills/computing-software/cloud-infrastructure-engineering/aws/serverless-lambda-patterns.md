---
id: computing-software.cloud-infrastructure-engineering.aws.serverless-lambda-patterns
name: serverless-lambda-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, serverless, event-driven, sqs, event-source-mapping, partial-batch-response, reportbatchitemfailures, dead-letter-queue, on-failure-destination, idempotency, snapstart, provisioned-concurrency, reserved-concurrency]
level: practitioner
status: docs-checked
description: "Build reliable AWS Lambda systems: invocation models, SQS partial batch failure handling, idempotency, reserved and provisioned concurrency, SnapStart limits and payload limits."
sources:
  - https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html
  - https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html
  - https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html
  - https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html
  - https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html
  - https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html
  - https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html
  - https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serverless Lambda patterns — design around the invocation model

**Goal:** Lambda functions whose failure, retry and concurrency behaviour you chose on purpose, so a bad message, a burst or a downstream outage degrades gracefully instead of looping, duplicating or overwhelming a database.

## 1. Know which invocation model you are in
- **Synchronous** (for example API Gateway, ALB, function URL): the caller sees the error and owns the retry.
- **Asynchronous** (for example S3, SNS, EventBridge): Lambda queues the event and retries on error; throttling (429) and system (500-series) errors return the event to the queue. Events that expire or fail all attempts are discarded unless you configure an on-failure destination or dead-letter queue (see "Error handling" for async invocation).
- **Poll-based** (event source mappings such as SQS): events are processed at least once and duplicates can occur.
Design every handler to be idempotent.

## 2. SQS consumer pattern
- Messages stay in the queue, hidden for the queue's visibility timeout, while Lambda processes a batch; Lambda deletes them only if the whole batch succeeds. Set the visibility timeout well above the function timeout (read the SQS page for the current guidance).
- Turn on partial batch responses by specifying `ReportBatchItemFailures` on the event source mapping and returning a `batchItemFailures` list of failed message IDs, so one bad record does not re-drive the whole batch.
- Put a dead-letter queue (redrive policy) on the source queue and alarm on its depth.
- Limit how hard the function hits downstream systems with the mapping's maximum concurrency setting rather than relying only on reserved concurrency.

## 3. Idempotency
Use a key from the event (message ID, order ID) and record completion in a durable store with a conditional write. Lambda's own guidance for event source mappings is to make function code idempotent because duplicates can occur.

## 4. Concurrency
- The default account concurrency limit is 1,000 per Region (raisable).
- Reserved concurrency guarantees a function capacity and also caps it; you can reserve up to the unreserved account concurrency minus 100.
- Provisioned concurrency keeps execution environments initialized for latency-sensitive paths.
- SnapStart does not support provisioned concurrency, Amazon EFS, or ephemeral storage above 512 MB, and only works with the runtimes listed on the SnapStart page.

## 5. Limits that shape design
- Maximum function timeout is 900 seconds (15 minutes).
- Invocation payload: 6 MB for request and response (synchronous); 1 MB (asynchronous). Pass S3 pointers for anything bigger.

## Gotchas
- Unhandled async failures without a destination or DLQ are discarded after retries.
- A recursive loop (function writes to the queue or bucket that triggers it) multiplies cost fast; use separate prefixes or buckets.

## Verify
- [ ] Each function's invocation model, retry behaviour and failure destination is written down.
- [ ] SQS mappings use `ReportBatchItemFailures`, and the source queue has a DLQ with an alarm.
- [ ] Replaying the same event twice produces one side effect.
- [ ] Critical functions have reserved concurrency; downstream databases are protected.

## Checked
2026-10-28. Confirmed in the Lambda Developer Guide pages for asynchronous error handling, SQS (with-sqs and error handling), concurrency, provisioned concurrency, SnapStart and quotas: queue-and-retry behaviour for async events, discard after expiry or failure, partial batch responses via `ReportBatchItemFailures` and `batchItemFailures`, at-least-once SQS processing and the idempotency recommendation, the 1,000 default concurrency and the reserve-minus-100 rule, SnapStart exclusions (provisioned concurrency, EFS, ephemeral storage above 512 MB), 900-second timeout.
Corrected: asynchronous payload limit is 1 MB, not 256 KB.
Removed as unconfirmed: the retry count and 6-hour event age, the 6x visibility timeout figure, `maxReceiveCount` values, `MaximumConcurrency` minimum, stream-mapping parameters, reserved concurrency 0 as a kill switch, arm64 and memory-tuning advice, the SnapStart runtime list, Step Functions, VPC and RDS Proxy notes, the 29-second API Gateway cap and the /tmp sizing.
Method: documentation only; no commands were run.
