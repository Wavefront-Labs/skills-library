---
id: computing-software.devops-ci-cd.rundeck.retry-failed-nodes
name: retry-failed-nodes
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, retry-failed-nodes, execution-plugin, job-retry, enterprise]
level: practitioner
status: docs-checked
description: "Make Rundeck job retries run only on nodes that failed or never started, using the Retry on failed nodes execution plugin (Enterprise)."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/job-retry-failed-nodes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The plugin reviews the previous execution's list of succeeded nodes and selects, for the next run, only the nodes that failed or were not started.

Requirement: it works together with the job's Retry setting, so Retry must be configured too.

Steps:
1. Edit or create the job and configure the Retry option (see the Retry section of the job creation docs).
2. On the Execution Plugins tab, tick the checkbox next to "Retry on failed nodes".
3. Save.

When the job fails, subsequent retry executions run only on nodes that did not succeed.

Example from the page: a job on 4 nodes had 2 succeed, 1 fail and 1 not start. The retry targeted only the remaining nodes.

This is an Enterprise feature.

## Checked

2026-11-04: the plugin behaviour, the Retry requirement, the Execution Plugins tab steps and the four-node example confirmed against the Rundeck Job Retry Failed Nodes page. Removed an unsourced verify step.

Method: documentation only; no commands were run.
