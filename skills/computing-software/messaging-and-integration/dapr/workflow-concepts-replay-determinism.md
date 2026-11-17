---
id: computing-software.messaging-and-integration.dapr.workflow-concepts-replay-determinism
name: workflow-concepts-replay-determinism
category: computing-software
field: messaging-and-integration
product: dapr
tags: [workflow, replay, determinism, event-sourcing, activities, child-workflows, durable-timers, continue-as-new, retry-policy]
level: advanced
status: docs-checked
description: "Dapr Workflow concepts: replay and the determinism rule, at-least-once activities, child workflows, continue-as-new, durable timers, code retries vs Resiliency."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/workflow/workflow-features-concepts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Dapr workflow is a function you write that defines tasks in order; the engine handles scheduling, failures and retries. Task kinds: activities (custom logic), durable timers, child workflows and external event waiters.

Identity: a workflow has a type name and each execution a unique instance ID, which your code may generate (for example an order ID). Only one instance with a given ID exists at a time; a completed or failed instance's ID can be reused, but the new instance replaces the old one's state.

Replay: state is kept by event sourcing, an append-only history. When a workflow awaits a task it unloads from memory; on completion the function runs again from the start, and for tasks already completed the engine returns the stored result instead of rescheduling, until the next await point. This requires deterministic workflow code: the same inputs must produce the same actions. Changing deployed workflow code needs extreme care for the same reason.

Activities are the unit of work with no restrictions (network calls, CPU work, return data). They run at least once, so write them to be idempotent.

Long histories: avoid infinite loops and thousands of scheduled tasks in one workflow. Use continue-as-new, which restarts the workflow with a new input and truncated history (good for eternal monitors), or distribute tasks across child workflows, each with its own instance ID, history and status. Terminating a parent terminates its children.

Retry policies are set in code, are durable across restarts and trigger on unhandled errors, unlike Resiliency YAML which is operator configured, not durable and triggered by timeouts and connectivity faults. Parameters: maximum attempts, first retry interval, backoff coefficient, maximum retry interval and retry timeout. Do not change a policy after workflows have run.

## Checked

Replay, identity, activity guarantees, continue-as-new, child workflows and the retry policy comparison confirmed on the Workflow features and concepts page.

Method: docs-checked 2026-11-09 against raw v1.15 workflow-features-concepts.md (read in full); no commands were run.
