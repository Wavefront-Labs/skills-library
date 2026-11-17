---
id: computing-software.messaging-and-integration.temporal.application-failures-handling
name: application-failures-handling
category: computing-software
field: messaging-and-integration
product: temporal
tags: [application-failure, failure-types, non-retryable, workflow-task-failure, error-propagation, failure-converter]
level: practitioner
status: docs-checked
description: "How Temporal classifies and propagates failures: Application Failure fields, workflow task vs execution failure, error wrapping that loses non-retryable flags."
sources:
  - https://docs.temporal.io/encyclopedia/application-failures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Platform failures (crashes, outages) are recovered by forward recovery with no code. Application failures come from your logic and may need backward recovery (compensation, such as releasing reserved inventory).

SDK failure types: Application, Activity (wraps Activity error in `cause`), Child Workflow, Timeout, Cancelled, Terminated, Server. Only Application Failure is created by you, with `message`, `type`, `non_retryable` and `details`. Never subclass the failure classes; custom subclasses can break protobuf serialisation. A non-Temporal error thrown from an Activity becomes an Application Failure with `non_retryable` false.

Workflow code outcomes:
- Non-Temporal error (null reference, nondeterminism) fails the Workflow Task: retried automatically, state preserved, fix and redeploy. The Worker evicts the cached execution and replays from history.
- Temporal failure (Application Failure) fails the Workflow Execution permanently. Cancelled Failure yields Cancelled state instead.

Propagation: an Activity error reaches the Workflow as an Activity Failure whose `cause` is the original (a Timeout Failure on timeout); Child Workflow errors arrive likewise.

Trap: the Service inspects only the outermost `failure_info` for retry decisions. If you catch a non-retryable Application Failure and rethrow it inside a generic error (`Error`, `Exception`, `fmt.Errorf`), the SDK emits a retryable failure and the flag is lost. Wrap only in another Application Failure that keeps `non_retryable`.

History: success writes `ActivityTaskScheduled`, `ActivityTaskStarted`, `ActivityTaskCompleted`; final failure adds `ActivityTaskFailed`, timeout adds `ActivityTaskTimedOut`; `ActivityTaskStarted` appears only at close. A failed workflow adds `WorkflowExecutionFailed`. The default Failure Converter stores messages and stacks as plain text; use a codec to encrypt them.

## Checked

2026-11-08. Read in full on the Application failures page: every concrete claim (names, events, rules, fields) matches the page.

Method: documentation only; no commands were run.
