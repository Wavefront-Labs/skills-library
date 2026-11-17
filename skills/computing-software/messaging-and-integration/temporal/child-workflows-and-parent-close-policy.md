---
id: computing-software.messaging-and-integration.temporal.child-workflows-and-parent-close-policy
name: child-workflows-and-parent-close-policy
category: computing-software
field: messaging-and-integration
product: temporal
tags: [child-workflows, parent-close-policy, continue-as-new, abandon, terminate, request-cancel]
level: practitioner
status: docs-checked
description: "Decide when to use Temporal child workflows versus activities, history partitioning limits, and Parent Close Policy values Abandon, Request Cancel and Terminate."
sources:
  - https://docs.temporal.io/child-workflows
  - https://docs.temporal.io/parent-close-policy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Child Workflow Execution is spawned by another Workflow in the same Namespace. The parent must await the child's start and may await its result. Children are not carried over when the parent uses Continue-As-New.

Do not use children only to organise code. Start with one workflow definition and Activities until there is a real need. Valid reasons:
- A separate service: children can run on different Workers but share no local state; communicate by Signals.
- Partitioning: one history cannot hold 100,000 Activity executions, but a parent can spawn 1,000 children with 1,000 Activities each. A parent should not spawn more than 1,000 children, because child status Events fill its history; children also record more Events than Activities.

Child versus Activity: a child can use Workflow APIs but obeys determinism; an Activity is the inverse. Child state changes are all in history, while an Activity records only input, output and retry attempts. An Activity is always cancelled with its Workflow; a child can continue if its Parent Close Policy is `ABANDON`. When in doubt, use an Activity.

Parent Close Policy decides what happens to a child when the parent reaches Completed, Failed or Timed Out:
- Abandon: child unaffected.
- Request Cancel: send a cancellation request.
- Terminate (default): forcefully terminate.

It is set per child and applies only to children, so you can opt out of propagation child by child, as when starting children asynchronously.

## Checked

2026-11-08. Read in full: the Child Workflows and Parent Close Policy pages (docs.temporal.io/child-workflows, docs.temporal.io/parent-close-policy). Every remaining claim matches those pages. Nothing removed.

Method: documentation only; no commands were run.
