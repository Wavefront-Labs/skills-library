---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-rule-monitoring-and-debugging
name: eventbridge-rule-monitoring-and-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, matchedevents, eventbridge-debugging, failedinvocations, invocation-metrics, rule-not-firing]
level: practitioner
status: docs-checked
description: "Debug EventBridge rules that do not fire or targets that fail: MatchedEvents vs Invocations vs FailedInvocations, catch-all log rules, target permissions and DLQ inspection."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-troubleshooting.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-monitoring.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge rule monitoring and debugging

## 1. Metrics per rule (namespace `AWS/Events` for the default and Classic custom buses; the new Custom Event Bus uses `AWS/EventsV2`)
Rule-only `RuleName` dimension means the default bus; `EventBusName` plus `RuleName` means a Classic custom bus. Delivery of metrics is best effort.
| Metric | Tells you |
|---|---|
| `MatchedEvents` | events that matched the pattern |
| `TriggeredRules` | rules that ran and matched an event (absent until a rule triggers) |
| `Invocations` | target invocation attempts |
| `FailedInvocations` | invocations that failed permanently (excludes retried ones and those counted in `DeadLetterInvocations`); only sent when non-zero |
| `InvocationsFailedToBeSentToDlq`, `InvocationsSentToDlq` | DLQ health |
| `ThrottledRules` | rule throttled by invocation quotas |
| `InvocationAttempts`, `RetryInvocationAttempts`, `SuccessfulInvocationAttempts`, `IngestiontoInvocationStartLatency` (documented spelling), `IngestionToInvocationSuccessLatency` | delivery behaviour and latency |
| `DeadLetterInvocations` | target not invoked, including invocations that would re-run the same rule in a loop |
Diagnosis:
- `MatchedEvents` = 0: the event never arrived on this bus or the pattern does not match.
- Matched but `FailedInvocations` > 0: target permission or target-side error.
- Matched, invoked, no failures, but nothing happened: target received it; check target logs
  and input transformer output.

## 2. Is the event arriving at all?
- Wrong bus: AWS service events go to the **default** bus in the region where they happen. Per the troubleshooting page, API-call events from global services such as IAM and Route 53 are available only in US East (N. Virginia).
- "AWS API Call via CloudTrail" events need an enabled CloudTrail trail with logging. Read-only management events match only rules in state `ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS`; see the CloudTrail events page.
- Custom events: `PutEvents` returns `FailedEntryCount` and per-entry `ErrorCode`;
  producers must check it.
- Debug aid: a temporary rule with a broad pattern targeting a CloudWatch Logs group shows exactly what arrives; the EventBridge Sandbox can also test patterns against sample events.

## 3. Does the pattern match?
```bash
aws events test-event-pattern --event-pattern file://pattern.json --event file://sample.json
```
`test-event-pattern` takes `--event-pattern` and `--event`. Compare the pattern structure against a real captured event, including the exact `detail-type` string.

## 4. Target failures
- Lambda: the function's resource policy must allow `events.amazonaws.com` with the rule ARN as `AWS:SourceArn` (check with `aws lambda get-policy`).
- SQS/SNS: the queue or topic policy must allow EventBridge; KMS-encrypted queues and topics need a key policy statement for `events.amazonaws.com` with `kms:Decrypt` and `kms:GenerateDataKey`.
- A rule's IAM role is supported for all target types; if it seems ignored, check that its trust policy allows `events.amazonaws.com` and that its permission policy grants the target action.
- Attach a DLQ to each target. DLQ messages carry attributes `RULE_ARN`, `TARGET_ARN`, `ERROR_CODE` and `ERROR_MESSAGE`; example codes include `NO_PERMISSIONS`, `NO_RESOURCE`, `THROTTLING` and `TIMEOUT`.
- Retry policy: by default EventBridge retries for 24 hours and up to 185 times with exponential backoff and jitter; lower the limits for time-sensitive events.

## 5. Alarms
`FailedInvocations > 0`, `InvocationsFailedToBeSentToDlq > 0` and, for critical rules,
`MatchedEvents` below expected rate (anomaly detection) catch silent breakage.

## Verify
- [ ] `test-event-pattern` returns true for a captured real event.
- [ ] Rule metrics show MatchedEvents = Invocations and zero FailedInvocations.
- [ ] DLQ configured per target; alarm on DLQ depth.

## Checked
2026-10-27. Documentation: Amazon EventBridge User Guide (monitoring metrics, troubleshooting, dead-letter queues, CloudTrail events), read this date. Confirmed: AWS/Events metric names and semantics (the draft's IngestionToInvocationStartLatency is spelled IngestiontoInvocationStartLatency in the docs), DLQ attributes and error codes (RESOURCE_NOT_FOUND in the draft is NO_RESOURCE), Lambda SourceArn policy, KMS key policy actions, default retry policy, global-service events only in us-east-1. Confirmed from the API model: TestEventPattern parameters and PutEvents FailedEntryCount/ErrorCode. Removed the wrong claim that CloudTrail API-call events arrive without a trail, and unconfirmed pattern-mistake and catch-all-pattern claims.
Method: documentation only; no commands were run.
