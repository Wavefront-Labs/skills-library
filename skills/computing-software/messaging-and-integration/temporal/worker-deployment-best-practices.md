---
id: computing-software.messaging-and-integration.temporal.worker-deployment-best-practices
name: worker-deployment-best-practices
category: computing-software
field: messaging-and-integration
product: temporal
tags: [worker-best-practices, worker-tuning, schedule-to-start-latency, task-slots, sticky-cache, poller-autoscaling, continue-as-new, claim-check]
level: practitioner
status: docs-checked
description: "Temporal Worker production practices: two Workers per queue, separate Task Queues, tuning slots, cache and pollers, Schedule-to-Start latency, Event History limits."
sources:
  - https://docs.temporal.io/best-practices/worker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

- Run at least two Worker Processes, on separate hosts and ideally separate Availability Zones, per shared always-on Task Queue; never scale below two (autoscaler minimum too). Count per Worker Deployment Version, since pinned Workflows cannot move to another version. Exceptions: host-specific queues, Serverless Workers, scale-to-zero. Roll out one Worker at a time to avoid emptying every sticky cache.
- Separate Task Queues by workload to control rate limiting and starvation. Define the queue name as a shared constant: a mismatch silently creates a second queue that no Worker polls.
- Default to Worker Versioning for Workflow code changes; use Patching only as a fallback.
- Keep Event History to a few thousand Events, well below the 51,200 hard limit, because replay slows and may time out. Use Continue-As-New (SDKs expose a suggestion, such as Python `is_continue_as_new_suggested()`). A payload over 2 MB or history over 50 MB can terminate the Workflow; apply the claim check pattern.

Tune rather than trust defaults: task slots (Slot Suppliers), sticky cache size, and poller counts (prefer Poller Autoscaling).

Dashboard: CPU and memory, `workflow_task_schedule_to_start_latency`, `activity_task_schedule_to_start_latency`, `worker_task_slots_available`, and `temporal_long_request_failure`, `temporal_request_failure`, `temporal_long_request_latency`, `temporal_request_latency`. Reading latency:
- High latency, high CPU or memory: saturated; add Workers (or Workers blocked on Activities).
- High latency, low CPU: raise pollers or slots; if long-request latency or failures are high, Workers struggle to reach the Service.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: best-practices/worker (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
