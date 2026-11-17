---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-redriving-failed-executions
name: step-functions-redriving-failed-executions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, sfn-redrive, redrive-execution, distributed-map-redrive, failure-recovery, idempotency]
level: practitioner
status: docs-checked
description: "Recover failed Step Functions Standard executions with redrive: eligibility, what reruns, Distributed Map child redrive, bulk redrive scripts and idempotency rules."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/redrive-executions.html", "https://docs.aws.amazon.com/step-functions/latest/dg/procedure-cw-metrics.html", "https://docs.aws.amazon.com/step-functions/latest/dg/service-quotas.html", "https://docs.aws.amazon.com/step-functions/latest/apireference/API_ListExecutions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redriving failed Step Functions executions

## 1. What redrive does
`RedriveExecution` restarts an unsuccessful **Standard** execution from the state(s) that
failed, reusing the same execution ARN and the saved input/output of the successful
steps. Steps that succeeded are not rerun.
```bash
aws stepfunctions redrive-execution --execution-arn <arn>
aws stepfunctions describe-execution --execution-arn <arn> \
  --query '{status:status,redriveCount:redriveCount,redriveStatus:redriveStatus,reason:redriveStatusReason}'
```

## 2. Eligibility
- Status `FAILED`, `TIMED_OUT` or `ABORTED`.
- Started on or after 15 November 2023, within **14 days** of the execution's stop (redrivable period), still within the one-year open limit, and with an event history under 24,999 events (the redrive appends events).
- Not for Express workflows (rerun them with a new StartExecution).
- The redrive uses the **original** definition (same version or alias association, even if the alias moved); you cannot redrive with a
  fixed definition. Fix external causes (permissions, downstream outage, bad data in a
  dependency) then redrive; if the bug is in the definition, start a new execution.
- Redrive needs the `states:RedriveExecution` permission on the execution; a redrive counts as state transitions for billing.

## 3. What reruns exactly
- The failed Task (or the state where a Catch did not handle the error) reruns with the
  same input. Retry counters reset.
- Inside Parallel: only failed or aborted branches rerun. Inside Map (inline): failed or aborted iterations
  rerun. If the state failed with `States.DataLimitExceeded`, the whole Parallel or Map reruns, including parts that had succeeded.
- Choice states are re-evaluated, Wait states with a timestamp in the past are skipped, and the state machine level timeout and task `TimeoutSeconds` reset.
- Distributed Map: redriving the parent redrives the Map Run, which reruns only **failed
  child executions**; succeeded children are kept (the Map Run's `manifest.json` references successful children across attempts).

## 4. Bulk redrive after an outage
```bash
aws stepfunctions list-executions --state-machine-arn <sm> --status-filter FAILED \
  --query 'executions[].executionArn' --output text |
  tr '\t' '\n' | while read arn; do
    aws stepfunctions redrive-execution --execution-arn "$arn" && sleep 0.2
  done
```
Throttle the loop: `RedriveExecution` is rate limited (token bucket) and downstream systems
just recovered. The `--redrive-filter` option of `list-executions` (`REDRIVEN`/`NOT_REDRIVEN`) is for the child executions of a Distributed Map and cannot be combined with a state machine ARN; to avoid redriving twice, check `redriveCount` in `describe-execution`.
EventBridge `Step Functions Execution Status Change` events with status `FAILED` can feed
an automated redrive Lambda for known transient errors, with a cap on redrive count.

## 5. Idempotency
The redriven task may have partially executed before failing (e.g. Lambda wrote to the DB
then timed out). Tasks must be idempotent: idempotency keys derived from execution name +
state name, conditional writes, Powertools idempotency utility.

## Gotchas
- A redrive resets the state machine level timeout and rerun task timeouts, so a task that times out because of its own `TimeoutSeconds` can time out again; fix the cause first.
- Callback and activity tasks that rerun are scheduled again, so external workers need the task token of the new attempt.
- CloudWatch metrics count redriven executions separately (`ExecutionsRedriven`,
  `RedrivenExecutionsSucceeded`, `RedrivenExecutionsFailed`); a redriven execution also emits the normal `Executions*` metric.

## Verify
- [ ] A test execution failed by a temporary permission removal, then redriven after restoring permission, completes without rerunning earlier steps (check history).
- [ ] Bulk script is rate limited and skips executions already redriven.
- [ ] Redriven tasks proven idempotent.

## Checked
Checked 2026-10-24 against the Step Functions developer guide (redrive, service quotas, CloudWatch metrics) and the ListExecutions API reference.
Confirmed: Standard-only, eligibility (started on or after 15 Nov 2023, 14 days, history under 24,999 events), same definition and version/alias, per-state redrive behaviour including DataLimitExceeded exception, retry counter and timeout reset, RedriveExecution permission, redrive metric names.
Corrected: the bulk loop used --redrive-filter with a state machine ARN, which the API rejects (the filter is for Distributed Map child executions with a Map Run ARN). Removed as unconfirmed: the 1,000 redrives per execution limit, behaviour of new task tokens, tolerated failure re-application.

Method: documentation only; no commands were run.
