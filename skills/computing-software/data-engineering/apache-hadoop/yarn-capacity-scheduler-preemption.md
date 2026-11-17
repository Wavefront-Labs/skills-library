---
id: computing-software.data-engineering.apache-hadoop.yarn-capacity-scheduler-preemption
name: yarn-capacity-scheduler-preemption
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, capacity-scheduler, preemption, auto-create-queues]
level: advanced
status: docs-checked
description: "Capacity Scheduler preemption monitor settings and defaults, per-queue disable_preemption, and auto-created leaf queue properties."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preemption and auto-created queues

The Capacity Scheduler can preempt containers from queues using more than their guaranteed capacity. In yarn-site.xml:
- `yarn.resourcemanager.scheduler.monitor.enable` = true (default false).
- `yarn.resourcemanager.scheduler.monitor.policies`: list of SchedulingEditPolicy classes; default `org.apache.hadoop.yarn.server.resourcemanager.monitor.capacity.ProportionalCapacityPreemptionPolicy`. Removing it from the list disables preemption (the page notes the default list means preemption is in the policy list by default once monitoring is on).

ProportionalCapacityPreemptionPolicy tuning (yarn-site.xml, prefix `yarn.resourcemanager.monitor.capacity.preemption.`):
- `observe_only`: false; if true, runs the policy without preempting or killing.
- `monitoring_interval`: 3000 ms between invocations.
- `max_wait_before_kill`: 15000 ms between requesting preemption from an app and killing the container.
- `total_preemption_per_round`: 0.1, the maximum share of resources preempted in one round.
- `max_ignored_over_capacity`: 0.1, a deadzone around target capacity to avoid thrashing.
- `natural_termination_factor`: 0.2, the fraction of the computed delta preempted, accounting for containers ending naturally.

Per queue, in capacity-scheduler.xml: `yarn.scheduler.capacity.<queue-path>.disable_preemption` = true opts a queue out (applies only when system-wide preemption is enabled; inherited from the parent if unset; default false). `<queue-path>.intra-queue-preemption.disable_preemption` does the same for intra-queue preemption, which also needs `yarn.resourcemanager.monitor.capacity.preemption.intra-queue-preemption.enabled` = true.

Legacy auto-created leaf queues (parent queue cannot also hold pre-configured queues):
- `<queue-path>.auto-create-child-queue.enabled`: mandatory on the parent; default false.
- `<queue-path>.auto-create-child-queue.management-policy`: optional; default `...capacity.queuemanagement.GuaranteedOrZeroCapacityOverTimePolicy`, which gives configured or zero capacity best-effort, so more leaf queues can exist than the parent can guarantee.
- `<queue-path>.leaf-queue-template.capacity`: mandatory; `.maximum-capacity` and other `leaf-queue-template.<property>` entries are optional. Absolute resource configuration is not supported for auto-created queues.
- Add `org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.QueueManagementDynamicEditPolicy` to `yarn.resourcemanager.scheduler.monitor.policies`; its interval is `yarn.resourcemanager.monitor.capacity.queue-management.monitoring-interval` (default 1500 ms).

The page also describes a flexible auto-creation mode (v2) that this skill does not cover.

## Checked

Method: 2026-11-08, read the CapacityScheduler markdown source in full for the preemption and auto-creation sections (and the queue-configuration sections for the sibling skill). Removed an unsupported "Verify" step and the "scheduler not scheduling" remark; added observe_only, intra-queue disable and the legacy-mode qualifier. Property names and defaults were unchanged.
