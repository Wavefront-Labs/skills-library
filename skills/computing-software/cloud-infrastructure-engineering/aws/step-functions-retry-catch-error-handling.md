---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-retry-catch-error-handling
name: step-functions-retry-catch-error-handling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, sfn-retry, sfn-catch, error-handling, backoff, redrive, state-machine]
level: practitioner
status: docs-checked
description: "Write Retry and Catch blocks in Step Functions: error names, backoff with jitter, timeouts and heartbeats, preserving input on failure, and redriving failed executions."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html", "https://docs.aws.amazon.com/step-functions/latest/dg/redrive-executions.html", "https://docs.aws.amazon.com/step-functions/latest/dg/workflow-variables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions Retry, Catch and error handling

**Goal:** transient faults retry with backoff, permanent faults route to a compensating path
with the original input intact, and nothing hangs forever.

## 1. A production Task
```json
"ChargeCard": {
  "Type": "Task",
  "Resource": "arn:aws:states:::lambda:invoke",
  "Arguments": {"FunctionName": "charge-card", "Payload": "{% $states.input %}"},
  "TimeoutSeconds": 30,
  "Retry": [
    {"ErrorEquals": ["Lambda.ServiceException",
                     "Lambda.SdkClientException", "Lambda.TooManyRequestsException"],
     "IntervalSeconds": 1, "MaxAttempts": 6, "BackoffRate": 2, "MaxDelaySeconds": 20,
     "JitterStrategy": "FULL"},
    {"ErrorEquals": ["PaymentGatewayTimeout"], "IntervalSeconds": 5, "MaxAttempts": 3},
    {"ErrorEquals": ["CardDeclined"], "MaxAttempts": 0}
  ],
  "Catch": [
    {"ErrorEquals": ["CardDeclined"], "Next": "NotifyDeclined",
     "Output": "{% $merge([$states.input, {'error': $states.errorOutput}]) %}"},
    {"ErrorEquals": ["States.ALL"], "Next": "CompensateOrder",
     "Output": "{% $merge([$states.input, {'error': $states.errorOutput}]) %}"}
  ],
  "Next": "ShipOrder"
}
```
JSONPath equivalent of keeping the input: `"ResultPath": "$.error"` in the Catcher. Without
it the failure output (`{"Error": ..., "Cause": ...}`) **replaces** your state, and the
compensation step has no order ID.

## 2. Field reference
- `IntervalSeconds` default 1, `MaxAttempts` default 3 (0 = never retry), `BackoffRate`
  default 2.0, `MaxDelaySeconds` (greater than 0) caps the backoff, `JitterStrategy` is `FULL` or `NONE` (default `NONE`); `FULL` randomizes each wait between 0 and the computed interval. Retries count as state transitions for billing.
- Retriers and catchers are evaluated **in order**; `States.ALL` must be alone and last.
- Built-in names include `States.TaskFailed` (any known error except `States.Timeout`), `States.Timeout`, `States.HeartbeatTimeout`,
  `States.Permissions`, `States.DataLimitExceeded`, `States.ExceedToleratedFailureThreshold`, `States.ItemReaderFailed`, `States.ResultWriterFailed` and
  `States.Runtime`. `States.ALL` does **not** catch `States.DataLimitExceeded` (name it explicitly to catch or retry it) or
  `States.Runtime` (never retriable; it always fails the execution; fix the definition or payload).
- Custom error names must not start with `States.`; they are matched exactly and case-sensitively. Newer Lambda runtimes report timeouts as `Sandbox.Timedout`; match `Lambda.Unknown`, `Sandbox.Timedout` and `States.TaskFailed` for unhandled Lambda errors.
- `TimeoutSeconds` (task wall clock) and `HeartbeatSeconds` (gap between
  `SendTaskHeartbeat` calls) — set both on any task that waits on something external. The
  default task timeout is effectively the workflow's (1 year for Standard).

## 3. Redrive instead of re-run (Standard only)
```bash
aws stepfunctions redrive-execution --execution-arn "$EXEC_ARN"
```
Restarts from the failed state, reusing successful steps' results; allowed within 14 days of
the failure and only for unsuccessful (failed, aborted or timed out) Standard executions; retry counters reset. Fix the root cause first.

## Gotchas
- Retrying a non-idempotent call (charge, email) without an idempotency key double-charges on
  a timeout that actually succeeded downstream.
- Lambda throttling (`TooManyRequestsException`) inside a Map with high concurrency needs
  generous backoff and jitter or the whole map fails together.
- Parallel/Map: one branch failing fails the state; catch inside the branch if partial
  success is acceptable, or use `ToleratedFailurePercentage` on Distributed Map.

## Verify
- [ ] Force each error (throw a custom error in a test Lambda) and confirm the execution history shows the expected number of `TaskFailed`/retry events and the right catcher.
- [ ] The compensation state's input still contains the business keys plus `error.Error`/`error.Cause`.
- [ ] `aws stepfunctions redrive-execution` on a fixed failure completes without re-running earlier successful states.

## Checked
Checked 2026-10-24 against the Step Functions developer guide (handling errors, redrive, JSONata data flow).
Confirmed: Retry fields, defaults and ranges (IntervalSeconds 1, MaxAttempts 3, BackoffRate 2.0, MaxDelaySeconds, JitterStrategy FULL/NONE default NONE), retrier and catcher ordering, States.ALL placement and exceptions, States.TaskFailed excluding States.Timeout, Catch Output with $states.errorOutput and JSONPath ResultPath default, Lambda error name guidance, redrive retry reset.
Corrected: States.ALL can be bypassed for States.DataLimitExceeded by naming it explicitly (the earlier text said such errors always fail the execution). Removed as unconfirmed: Lambda.AWSLambdaException, States.ResultPathMatchFailure, Python exception naming rule.

Method: documentation only; no commands were run.
