---
id: computing-software.messaging-and-integration.temporal.workflow-timeouts
name: workflow-timeouts
category: computing-software
field: messaging-and-integration
product: temporal
tags: [workflow-timeouts, workflow-execution-timeout, workflow-run-timeout, workflow-task-timeout, temporalreportedproblems]
level: practitioner
status: docs-checked
description: "Temporal workflow execution, run and task timeouts: defaults, what each bounds, 120 second task limit and detecting task failures with TemporalReportedProblems."
sources:
  - https://docs.temporal.io/encyclopedia/detecting-workflow-failures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Temporal generally advises against workflow timeouts, since workflows are meant to be long-running and resilient; to act after a delay, use a Timer. All three are set when starting the execution.

Workflow Execution Timeout: the maximum time an execution may stay open, including retries and every Continue-As-New. Default infinite. On expiry the status is Timed Out. Most common use: stopping a Temporal Cron Job after some total time.

Workflow Run Timeout: limits one run only (a single Workflow ID may span several runs, each with its own Run ID, through retries or Continue-As-New), excluding retries and Continue-As-New. Default equals the Execution Timeout. Most common use: bounding one cron iteration. Reaching it also yields Timed Out.

Workflow Task Timeout: the time a Worker has to process a Workflow Task after pulling it from the Task Queue. Its purpose is to notice a dead Worker so another can recover the execution. Default 10 seconds, maximum 120 seconds. Raise it only if a very large Event History takes over 10 seconds to load, and going beyond the default is not recommended.

Detecting task failures: a failed Workflow Task does not fail the Workflow. Handled failures proceed; an unhandled one leaves the workflow running but unable to complete. Find these with the `TemporalReportedProblems` Search Attribute or the Web UI Task Failures View. That view must be enabled per Namespace through Dynamic Config.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: encyclopedia/detecting-workflow-failures (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
