---
id: computing-software.messaging-and-integration.temporal.task-queues-and-partitions
name: task-queues-and-partitions
category: computing-software
field: messaging-and-integration
product: temporal
tags: [task-queue, partitions, sync-match, nexus-task-queue, not-found, task-ordering, worker-registration]
level: practitioner
status: docs-checked
description: "How Temporal Task Queues work: three types, on-demand creation, sync match, where to name them, identical registrations rule, Not Found errors and default 4 partitions."
sources:
  - https://docs.temporal.io/task-queue
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Task Queue is a lightweight, dynamically created queue that Workers poll. There are Workflow, Activity and Nexus Task Queues; naming one queue creates all three under that name. No registration is needed and the number of queues is unlimited.

Workers poll over synchronous RPC, so they pull only with spare capacity (natural load balancing), need no discovery or open ports, and enable Task Routing. Activity queues support server-side throttling. Workflow and Activity Tasks persist while Workers are down. Nexus and Query Tasks are not persisted; they are sync matched only when a Worker polls, and the caller retries (Nexus callers retry until Schedule-To-Close).

Rule: every Worker on a Task Queue must register the same Workflows, Activities and Nexus handlers. Exceptions are Worker Versioning during rollouts and dynamic Workflows or Activities. An unknown type fails the task as "Not Found": retryable for Workflow and Activity Tasks (the execution itself does not fail), non-retryable for Nexus handlers.

Five places to set the name: starting a Workflow (required); creating a Worker (required); starting an Activity (optional, inherits the workflow's); starting a Child Workflow (optional, inherits the parent's); creating a Nexus Endpoint.

Ordering: each queue has 4 partitions by default. One partition is almost always FIFO but limits throughput. With several, each task goes to a random partition and, once a backlog builds, sync match rate drops toward zero because backlog tasks dispatch first. This is task ordering only; event order in a history is fixed.

## Checked

2026-11-08. Read in full: the Task Queues page (docs.temporal.io/task-queue). Every remaining claim matches those pages. Nothing removed.

Method: documentation only; no commands were run.
