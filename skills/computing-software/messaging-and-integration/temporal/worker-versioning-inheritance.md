---
id: computing-software.messaging-and-integration.temporal.worker-versioning-inheritance
name: worker-versioning-inheritance
category: computing-software
field: messaging-and-integration
product: temporal
tags: [worker-versioning, inheritance, child-workflow, continue-as-new, retry, pinned, versioning-override]
level: advanced
status: docs-checked
description: "Which Temporal versioning behavior and pinned version carries over to child workflows, continue-as-new runs, retries and cron runs, including override inheritance."
sources:
  - https://docs.temporal.io/worker-versioning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
New runs start through Child Workflows, Continue-As-New, retries per Retry Policy, or Cron iterations. Auto-Upgrade workflows never inherit a version. Pinned workflows by default pass their version to Pinned children. Cron Jobs never inherit versioning behavior or version.

Child Workflows:
- Parent Pinned and the child's Task Queue belongs to that version: the child's first Workflow Task runs on the parent's version. A Pinned child stays pinned to it for life; an Auto-Upgrade child becomes Auto-Upgrade after its first task completes.
- Child's Task Queue in a different Worker Deployment: no inheritance; it starts on the Current Version of its own queue.
- Parent Auto-Upgrade: the child inherits nothing and starts on its Deployment's Current Version like any new workflow.

Continue-As-New:
- Original Pinned: the pinned version is inherited along the chain, unless the new run's Task Queue sits in another Worker Deployment (then it starts on that queue's Current Version).
- Original Auto-Upgrade: no inheritance.

Retries inherit only if all hold: the retried run is effectively pinned at retry time; it inherited a pinned version when it started (child of a pinned parent, or Continue-As-New of a pinned run); and it is running on a Task Queue in the inherited version. Otherwise none.

Overrides: children, crons, retries and Continue-As-New inherit the source run's versioning override when the override is pinned and the new workflow's Task Queue belongs to the override version. Override inheritance is evaluated separately and takes precedence over inherited base version.

## Checked

2026-11-08. Read in full on the Worker Versioning page: every concrete claim (names, events, rules, fields) matches the page. Inheritance rules for children, Continue-As-New, retries, crons and overrides confirmed.

Method: documentation only; no commands were run.
