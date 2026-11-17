---
id: computing-software.data-engineering.kestra.flowable-and-flow-retries
name: flowable-and-flow-retries
category: computing-software
field: data-engineering
product: kestra
tags: [retry, behavior, retry-flowable, flow-level-retry, subflow, parallel]
level: advanced
status: docs-checked
description: "Retry behaviour on Kestra flowable tasks and at flow level: RETRY_FAILED_TASK, RETRY_FLOWABLE, CREATE_NEW_EXECUTION, and effects on Loop and Subflow."
sources:
  - https://kestra.io/docs/workflow-components/retries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flowable tasks such as `Sequential` and `Parallel` accept `retry` with a `behavior`.

- `RETRY_FAILED_TASK` (default): only the failed child reruns; earlier tasks do not. The policy is also the default for children without their own `retry`.
- `RETRY_FLOWABLE`: the whole block reruns and previous child runs are discarded. In a `Loop`, only the failed iteration restarts. Rejected on runnable tasks and at flow level.
- A `Subflow` with `retry` starts a new execution on each retry.

Caveat: under `RETRY_FAILED_TASK`, a token that expires between tasks is not refreshed. Enterprise and Cloud Credentials handle refresh.

Flow-level retries use `behavior` too:

- `CREATE_NEW_EXECUTION`: starts a new execution and increases the execution attempt.
- `RETRY_FAILED_TASK`: retries only the failed task and increases the task run attempt.

Flow-level retries also restart Subflows as new executions.

## Checked

2026-11-04. Confirmed against the Kestra retries page: RETRY_FAILED_TASK default and RETRY_FLOWABLE on flowable tasks, Loop restarting only the failed iteration, rejection on runnable tasks and at flow level, Subflow retry creating a new execution, token refresh caveat and Credentials, flow-level CREATE_NEW_EXECUTION and RETRY_FAILED_TASK. Nothing removed.

Method: documentation only; no commands were run.
