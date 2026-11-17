---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-scheduler-schedules
name: eventbridge-scheduler-schedules
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, eventbridge-scheduler, scheduler, schedule-group, flexible-time-window, cron-expression, rate-expression, one-time-schedule, schedule-timezone, universal-targets, scheduler-dlq, action-after-completion, cron-jobs]
level: practitioner
status: docs-checked
description: "Create cron, rate and one-time schedules with EventBridge Scheduler: time zones, DST, flexible windows, groups, universal targets, retries and DLQ."
sources: ["https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-templated.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/configuring-schedule-dlq.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/monitoring-cloudwatch.html", "https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-flexible-time-windows.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge Scheduler

**Goal:** every "run X at Y" in the system lives in Scheduler — with time zones that survive
DST, a window that spreads load, retries and a DLQ — rather than in rule cron expressions,
cron on an instance, or `sleep` in a Lambda.

## 1. Scheduler vs scheduled rules
EventBridge Scheduler is a separate service from scheduled rules on an event bus. Scheduler gives you
`rate`, `cron` and one-time `at` schedules, evaluation in a time zone you choose, flexible time windows,
schedule groups, templated and universal targets, retry policies and DLQs, and a default quota of 10,000,000
schedules per Region (adjustable to billions). Prefer it for new scheduled work.

## 2. Create
```bash
aws scheduler create-schedule --name nightly-report --group-name reporting \
  --schedule-expression "cron(0 2 * * ? *)" --schedule-expression-timezone "Europe/London" \
  --flexible-time-window '{"Mode":"FLEXIBLE","MaximumWindowInMinutes":15}' \
  --target '{"Arn":"arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:report","RoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/scheduler-invoke",
             "Input":"{\"kind\":\"nightly\"}","RetryPolicy":{"MaximumRetryAttempts":3,"MaximumEventAgeInSeconds":3600},
             "DeadLetterConfig":{"Arn":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:scheduler-dlq"}}' \
  --start-date 2026-11-01T00:00:00Z --end-date 2027-11-01T00:00:00Z --state ENABLED
```
Expressions: `rate(value unit)` with units `minutes`, `hours`, `days`; `cron(minutes hours day-of-month month day-of-week year)`
(six fields; `?` is needed in one of day-of-month and day-of-week); `at(yyyy-mm-ddThh:mm:ss)` (no `Z`; evaluated in the
schedule's time zone, UTC by default). The execution role needs permission to call the target API
(for example `lambda:InvokeFunction`, `sqs:SendMessage`). `at` schedules ignore `StartDate` and `EndDate`;
all schedule types fire with 60-second precision. The `Input` payload is limited to 256 KB.

## 3. Time zones and DST
`--schedule-expression-timezone` (an IANA time zone) makes `cron(0 2 ...)` mean 02:00 local and adjusts for DST
automatically in zones that observe it. When clocks move forward and the time does not exist, that day's
invocation is skipped; when clocks move back, the schedule runs once and does not repeat. For
`rate(n days)` schedules a day is a fixed 24 hours. DST adjustments do not apply to UTC.

## 4. Flexible window
`Mode` is `FLEXIBLE` or `OFF` (you must specify one; `FLEXIBLE` requires `MaximumWindowInMinutes`). With a
flexible window EventBridge Scheduler invokes the target within the window after the scheduled time, which
disperses invocations; `OFF` for exact times. `MaximumWindowInMinutes` is 1 to 1440.

## 5. Targets
- **Templated** targets (the target ARN implies the API): CodeBuild `StartBuild`, CodePipeline
  `StartPipelineExecution`, ECS `RunTask` (`EcsParameters`), EventBridge `PutEvents` (`EventBridgeParameters`; no
  cross-Region delivery), Inspector `StartAssessmentRun`, Kinesis `PutRecord` (`KinesisParameters`), Firehose
  `PutRecord`, Lambda `Invoke`, SageMaker `StartPipelineExecution` (`SageMakerPipelineParameters`), SNS
  `Publish`, SQS `SendMessage` (`SqsParameters`), Step Functions `StartExecution`.
- **Universal** target: `Arn: arn:aws:scheduler:::aws-sdk:<service>:<apiAction>` with `Input` as the API request
  JSON, for example `aws-sdk:sqs:sendMessage` or `aws-sdk:sfn:startExecution`. The service name must match the
  AWS SDK service identifier (for example `cognitoidentityprovider`, not `cognito-idp`), and the execution role
  needs the matching IAM permission. Read-only actions with prefixes such as `get`, `describe`, `list`, `receive`,
  `query`, `scan` and `invokeModel` are not supported. Scheduler does not validate universal-target `Input` at
  creation: a schedule with bad input is created and fails on every invocation.
- Template context attributes usable in `Input`: `<aws.scheduler.schedule-arn>` and `<aws.scheduler.scheduled-time>`.

## 6. One-time schedules at scale
`at(...)` + `--action-after-completion DELETE` (`ActionAfterCompletion` is `NONE` or `DELETE`) is the pattern for
per-entity reminders. A completed one-time schedule still counts toward the 10,000,000-schedule quota until it is
deleted, so AWS recommends automatic deletion. There are up to 500 schedule groups per Region by default;
schedules are in the `default` group unless you set `--group-name`.

## 7. Retries, DLQ, observability
- `RetryPolicy` (`MaximumRetryAttempts`, `MaximumEventAgeInSeconds`) is set per target. The DLQ must be a
  **standard** SQS queue (FIFO is not supported) and the execution role needs `sqs:SendMessage` on it. A
  dead-letter event holds the schedule's `Input` (truncated if it exceeds the SQS size limit) plus attributes
  `ERROR_CODE`, `ERROR_MESSAGE`, `EXHAUSTED_RETRY_CONDITION` (`MaximumRetryAttempts` or `MaximumEventAgeInSeconds`),
  `RETRY_ATTEMPTS`, `EXECUTION_ID`, `SCHEDULE_ARN`, `SCHEDULED_TIME`, `TARGET_ARN`, `IS_PAYLOAD_TRUNCATED`.
- `AWS/Scheduler` metrics (dimension `ScheduleGroup`): `InvocationAttemptCount`, `TargetErrorCount`,
  `TargetErrorThrottledCount`, `InvocationThrottleCount` (your invocation quota was hit), `InvocationDroppedCount`
  (retry policy exhausted); with a DLQ also `InvocationsSentToDeadLetterCount` and
  `InvocationsFailedToBeSentToDeadLetterCount`. Delivery of metrics is best effort.

## Gotchas
- The default invocation throttle is 1,000 TPS in the main Regions (500 elsewhere, adjustable); beyond it
  invocations are delayed, not lost. A flexible window spreads load.
- `State` is `ENABLED` or `DISABLED`; `EndDate` is the date, in UTC, before which a recurring schedule can invoke
  its target, so a passed end date stops invocations.

## Verify
- [ ] `cron(0 2 * * ? *)` with `Europe/London` fires at 02:00 local on both sides of a DST change (check two dates in the target's logs/CloudTrail).
- [ ] A universal-target schedule stops a test instance and CloudTrail shows `StopInstances` by the scheduler role.
- [ ] A target that errors sends the input to the DLQ after `MaximumRetryAttempts`; `TargetErrorCount` metric increments.
- [ ] A one-time schedule with `ActionAfterCompletion=DELETE` disappears from `list-schedules` after firing.

## Checked

Date 2026-10-23. Documentation release: current EventBridge Scheduler User Guide and API Reference.
Confirmed: schedule expression syntax and units; `at` ignores StartDate/EndDate; 60-second precision; time zone and DST behaviour; templated target list and parameter names; universal target ARN format, SDK service identifier rule, unsupported read-only prefixes, no input validation; context attributes `<aws.scheduler.schedule-arn>` and `<aws.scheduler.scheduled-time>`; `ActionAfterCompletion` NONE|DELETE; quotas (10,000,000 schedules, 500 groups, 1,000/500 TPS invocation throttle, 256 KB Input); DLQ standard-queue-only, attributes and permissions; `AWS/Scheduler` metrics; flexible window modes.
Corrected: the schedule quota is 10,000,000 per Region (not 1 million); the DLQ must be a standard queue; `<aws.scheduler.execution-id>` and `<aws.scheduler.attempt-number>` are not documented placeholders; CodePipeline was missing from the templated list.
Removed (not in docs): the scheduled-rules comparison details, role trust note, at-least-once claim, Lambda async-retry remark, describe-schedule/CloudTrail remark, delete-group behaviour, 185-attempt default.
Also confirmed: `FlexibleTimeWindow` `Mode` OFF|FLEXIBLE and `MaximumWindowInMinutes` 1 to 1440 (API reference).
Sources: https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html ; https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html ; https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-templated.html ; https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html ; https://docs.aws.amazon.com/scheduler/latest/UserGuide/configuring-schedule-dlq.html ; https://docs.aws.amazon.com/scheduler/latest/UserGuide/monitoring-cloudwatch.html ; https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-flexible-time-windows.html

Method: documentation only; no commands were run.
