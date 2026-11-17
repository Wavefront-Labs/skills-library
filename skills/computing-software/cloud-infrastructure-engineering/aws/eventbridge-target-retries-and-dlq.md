---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-target-retries-and-dlq
name: eventbridge-target-retries-and-dlq
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, eb-dlq, failed-invocations, retry-policy, dead-letter-config, maximum-event-age, maximum-retry-attempts, invocations-sent-to-dlq, target-permissions, throttled-rules, event-driven, reliability]
level: practitioner
status: docs-checked
description: "Make EventBridge rule targets reliable: per-target RetryPolicy and SQS DeadLetterConfig, the difference between retryable and permanent failures, DLQ message attributes, alarms and redrive."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html", "https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_RetryPolicy.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-monitoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge target retries and dead-letter queues

**Goal:** no event silently vanishes because a target was throttled, misconfigured or down —
every failure either retries to success or lands in a queue someone is alarmed on.

## 1. Default behaviour (what you get without configuring anything)
EventBridge retries events that fail because of retriable errors (for example the target is unavailable
or network conditions) for **24 hours and up to 185 times** by default, using exponential backoff with jitter.
When all attempts are used the event is **dropped** unless a DLQ is configured. Some errors are not retried:
missing permissions to a target, a target resource that no longer exists, or a target that cannot be found
(invalid address, DNS lookup failure). Those events go straight to the target's DLQ, if one is set, until
you fix the cause. A failed delivery publishes a CloudWatch metric (`FailedInvocations` counts permanent failures).

## 2. Configure per target
```json
{"Id":"fn","Arn":"arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:consumer",
 "RetryPolicy":{"MaximumRetryAttempts":10,"MaximumEventAgeInSeconds":1800},
 "DeadLetterConfig":{"Arn":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:eb-rule-dlq"}}
```
- Retries continue until the maximum attempts are made or `MaximumEventAgeInSeconds` is reached. `MaximumEventAgeInSeconds`
  is 60 to 86,400; `MaximumRetryAttempts` is 0 to 185. For time-sensitive events (alerts) use a short age
  so stale events go to the DLQ instead of arriving an hour late.
- The DLQ must be a **standard** SQS queue (FIFO queues are not supported) in the same Region as the rule;
  a queue in another account is allowed with a manually attached resource policy. The queue policy must grant
  `events.amazonaws.com` `sqs:SendMessage` with `aws:SourceArn` = the **rule** ARN:
```json
{"Effect":"Allow","Principal":{"Service":"events.amazonaws.com"},"Action":"sqs:SendMessage",
 "Resource":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:eb-rule-dlq","Condition":{"ArnEquals":{"aws:SourceArn":"arn:aws:events:<REGION>:<ACCOUNT_ID>:rule/<bus>/<rule>"}}}
```
  (The console adds this policy for a same-account queue; `PutTargets` through the API/CLI/IaC does not, and
  neither does a queue in another account. Failures to deliver to the DLQ show in `InvocationsFailedToBeSentToDlq`.)
- Lambda targets: EventBridge's retry policy covers delivering the invocation to the target. Errors raised
  inside the function are governed by Lambda's own asynchronous-invocation settings (retries and
  on-failure destination); check the Lambda documentation and configure a destination there too.

## 3. What a DLQ message contains
The message body is the event that could not be delivered. Each message carries custom attributes
`RULE_ARN`, `TARGET_ARN`, `ERROR_CODE`, `ERROR_MESSAGE`, `EXHAUSTED_RETRY_CONDITION` (`MaximumRetryAttempts` or
`MaximumEventAgeInSeconds`) and `RETRY_ATTEMPTS`. Sample `ERROR_CODE` values from the docs: `NO_PERMISSIONS`,
`NO_RESOURCE`, `THROTTLING`, `TIMEOUT`, `SDK_CLIENT_ERROR`, `INVALID_JSON`, `FAILED_TO_ASSUME_ROLE`,
`CONNECTION_FAILURE`, `ERROR_FROM_TARGET`, `CROSS_ACCOUNT_INGESTION_FAILED`. Use `receive-message --message-attribute-names All`
to inspect them.

## 4. Alarms
- `AWS/Events` by `RuleName`: `FailedInvocations` (permanent failures) > 0, `InvocationsSentToDlq` > 0,
  `InvocationsFailedToBeSentToDlq` > 0 (events lost even to the DLQ), `ThrottledRules` > 0 (rule execution was
  throttled, invocations may be delayed), `RetryInvocationAttempts` to watch retries. EventBridge sends some of
  these only when non-zero, and CloudWatch delivery is best effort and not a complete accounting.
- SQS DLQ `ApproximateNumberOfMessagesVisible` > 0.

## 5. Redrive
AWS describes two ways to drain a DLQ: set it as the event source of a Lambda function, or write your own SQS
consumer that polls, processes and deletes the messages (for example re-sending the event with `put-events`).
The SQS message-move (redrive) task supports only DLQs whose sources are SQS queues, so it does not apply here.
If only one target failed, call that target directly instead of re-publishing to the bus, because a re-published
event matches all rules again.

## Gotchas
- `RetryPolicy` and `DeadLetterConfig` are **per target**, not per rule: set them on every target.

## Verify
- [ ] Remove the Lambda target's resource policy: next event produces a DLQ message with `ERROR_CODE=NO_PERMISSIONS` within seconds and `InvocationsSentToDlq` = 1.
- [ ] Set reserved concurrency 0 on the function: events retry (`RetryInvocationAttempts` grows) and reach the DLQ with `EXHAUSTED_RETRY_CONDITION` after the configured cap.
- [ ] Remove the DLQ queue policy: `InvocationsFailedToBeSentToDlq` increments (then restore).

## Checked

Date 2026-10-23. Documentation release: current Amazon EventBridge User Guide and API Reference, SQS StartMessageMoveTask reference.
Confirmed: default 24 hours / 185 attempts with exponential backoff and jitter; drop after exhaustion; non-retried error classes go to the DLQ; `RetryPolicy` ranges (60 to 86,400 s; 0 to 185); DLQ same Region, standard queue only, cross-account needs a manual policy; queue policy shape (`events.amazonaws.com`, `aws:SourceArn` rule ARN); the console adds the policy but `PutTargets` does not; DLQ message attributes and sample error codes; metric names `FailedInvocations`, `InvocationsSentToDlq`, `InvocationsFailedToBeSentToDlq`, `ThrottledRules`, `RetryInvocationAttempts`; two documented ways to drain a DLQ.
Corrected: FIFO queues are NOT supported as EventBridge DLQs (the draft said standard or FIFO); error codes are `THROTTLING` and `NO_RESOURCE` (the draft's `THROTTLED` and `TARGET_NOT_FOUND` are not listed); SQS `start-message-move-task` does not support non-SQS-fed DLQs.
Removed (not in docs): per-error retry classification lists, Lambda async retry count, input-transformation remark on the DLQ body, 256 KB failure remark, API destination and FIFO group notes, in-flight policy-change remark.
Sources: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html ; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html ; https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_RetryPolicy.html ; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-monitoring.html ; https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_StartMessageMoveTask.html

Method: documentation only; no commands were run.
