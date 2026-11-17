---
id: computing-software.messaging-and-integration.temporal.activity-definition-idempotency
name: activity-definition-idempotency
category: computing-software
field: messaging-and-integration
product: temporal
tags: [activity-definition, idempotency, activity-type, worker-registration, retries, activity]
level: practitioner
status: docs-checked
description: "Define Temporal activities that survive retries: idempotency keys, granular steps, registration with a Worker, activity type naming and timeouts."
sources:
  - https://docs.temporal.io/activity-definition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An Activity Definition is an ordinary function or method doing one well-defined action. Once a Worker registers it, the same Activity can run as a step in a Workflow or as a Standalone Activity with no code change.

Registration maps the Activity Type (a name) to your function; the Worker must be polling the Task Queue the Activity Tasks go to. In Go, `w.RegisterActivity(fn)`, in Python `activities=[fn]`. Go and TypeScript can set the Activity Type at registration; other SDKs set it on the definition (Python: `@activity.defn(name="your_activity")`).

Idempotency: Activities may run more than once, so any that writes should be idempotent. Completed Activities are not re-executed on replay, but nothing reaches Event History until the Activity returns or errors; if a Worker crashes after the work finishes but before reporting, the Activity is retried.

Idempotency keys are enforced by the called service. A good key is Workflow Run ID plus Activity ID: stable across retries, unique across executions.

Keep Activities granular. A three-step Activity (database lookup, microservice call, file write) re-runs all steps if the last fails; make it three Activities, balancing against more history.

Retry rules: with a Retry Policy allowing retries, the Activity is observed as completed exactly once but may execute many times, partially. Do not hand-write retry loops inside Activities; that lengthens timeouts, hides failure metrics and complicates debugging.

Practice: serialisable arguments and results, finish within minutes or heartbeat, and set at least one timeout, typically Start-To-Close; shorter timeouts detect problems sooner.

## Checked

2026-11-08. Read in full on the Activity Definition page: every concrete claim (names, events, rules, fields) matches the page.

Method: documentation only; no commands were run.
