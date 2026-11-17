---
id: computing-software.cloud-infrastructure-engineering.aws.scheduled-lambda-with-eventbridge-scheduler
name: scheduled-lambda-with-eventbridge-scheduler
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, scheduled-lambda, eventbridge-scheduler, cron, idempotency]
level: practitioner
status: docs-checked
description: "Run Lambda functions on cron or rate schedules with EventBridge Scheduler: time zones, flexible windows, retries and DLQ, execution role and idempotent handlers."
sources: ["https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html", "https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/setting-up.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled Lambda functions via EventBridge Scheduler

## 1. Execution role
The schedule's role trusts `scheduler.amazonaws.com`, allows invoking the Lambda function, and allows
`sqs:SendMessage` on the dead-letter queue (see the Scheduler setup guide for the policy examples).

## 2. Create the schedule
```bash
aws scheduler create-schedule --name nightly-report --group-name default \
  --schedule-expression "cron(0 2 * * ? *)" --schedule-expression-timezone Europe/London \
  --flexible-time-window Mode=FLEXIBLE,MaximumWindowInMinutes=15 \
  --target '{"Arn":"arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:report:live",
    "RoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/scheduler-invoke",
    "Input":"{\"job\":\"nightly\"}",
    "RetryPolicy":{"MaximumRetryAttempts":2,"MaximumEventAgeInSeconds":3600},
    "DeadLetterConfig":{"Arn":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:scheduler-dlq"}}'
```
- Schedule types: `rate(...)` and `cron(...)` recurring schedules, and one-time `at(yyyy-mm-ddThh:mm:ss)`. Each is
  evaluated in the time zone you set with `--schedule-expression-timezone`; the docs cover daylight saving handling
  (a `rate(1 days)` is a 24-hour duration).
- `FlexibleTimeWindow` `Mode` is `OFF` or `FLEXIBLE`; `MaximumWindowInMinutes` is 1-1440. Use `OFF` when exact timing matters.
- `RetryPolicy`: `MaximumRetryAttempts` 0-185 and `MaximumEventAgeInSeconds` 60-86400.

## 3. Handler rules
- Scheduler invokes the function asynchronously, so a returned error is not seen by the scheduler. Make the job
  idempotent (date key in DynamoDB, conditional write) so a retry or duplicate is harmless.
- For long jobs, start a Step Functions execution from the function instead.

## 4. Failure visibility
Watch the Scheduler CloudWatch metrics, the Lambda asynchronous invocation failure destinations, and an alarm on DLQ depth.

## Verify
- [ ] `aws scheduler get-schedule --name nightly-report` shows `State: ENABLED` and the right time zone.
- [ ] A forced failure lands in the DLQ after retries.

## Checked

2026-10-28. Confirmed against the EventBridge Scheduler User Guide pages schedule-types and setting-up, the Lambda guide page with-eventbridge-scheduler (asynchronous invocation), and the botocore scheduler model (FlexibleTimeWindow modes and range, RetryPolicy ranges, DeadLetterConfig, ScheduleState).
Removed: the aws:SourceAccount trust condition, the lambda:InvokeFunction alias-ARN detail, the "one of dom/dow must be ?" rule, "old EventBridge rules were UTC only", at-least-once delivery wording, the 15-minute Lambda limit, alias-targeting advice, and the AWS/Scheduler and Lambda metric names.
Method: documentation only; no commands were run.
