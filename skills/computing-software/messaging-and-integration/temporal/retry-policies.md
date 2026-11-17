---
id: computing-software.messaging-and-integration.temporal.retry-policies
name: retry-policies
category: computing-software
field: messaging-and-integration
product: temporal
tags: [retry-policy, backoff-coefficient, initial-interval, maximum-attempts, non-retryable-errors, next-retry-delay]
level: practitioner
status: docs-checked
description: "Temporal retry policy defaults and fields: initial interval, backoff coefficient, maximum interval and attempts, non-retryable errors, next retry delay."
sources:
  - https://docs.temporal.io/encyclopedia/retry-policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Retry Policy is declarative: you state the behaviour and Temporal retries. Activities have one by default; Workflow Executions do not, and retrying a whole workflow is discouraged (replay would repeat the same logic). Workflow Tasks are not governed by it; they retry until the Workflow Execution Timeout (unlimited by default) with exponential backoff capped at 10 minutes.

Defaults:
- Initial Interval 1 second
- Backoff Coefficient 2.0 (1.0 keeps the interval constant)
- Maximum Interval 100 x Initial Interval
- Maximum Attempts unlimited (0 also means unlimited, 1 means no retries, negative is an error)
- Non-Retryable Errors none

Retry interval = the smaller of Initial Interval x Coefficient^retries and Maximum Interval. To cap total retry time, prefer Workflow Execution Timeout (workflows) or Schedule-To-Close Timeout (Activities) over Maximum Attempts.

Non-retryable errors: names matched against the `type` of the Application Failure. Either list them in the policy (the caller decides) or mark the failure itself non-retryable, which always wins, for example Python `ApplicationError(..., type="InvalidChargeAmount", non_retryable=True)`, TypeScript `nonRetryable: true`, Go `temporal.NewNonRetryableApplicationError(...)`, Java `ApplicationFailure.newNonRetryableFailure`. Use sparingly, for permanent failures such as bad input.

Per-error next retry delay: set the next Retry delay on an Application Failure to override the computed interval; Maximum Attempts and overall timeouts still apply.

History quirks: `ActivityTaskStarted` is not written until the Activity finishes or exhausts retries (use Describe for the pending attempt count). A failing workflow with a policy ends with `WorkflowExecutionFailed` (`retryState=IN_PROGRESS`, `newExecutionRunId` set); the new run records `first_workflow_task_backoff`.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: encyclopedia/retry-policies (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
