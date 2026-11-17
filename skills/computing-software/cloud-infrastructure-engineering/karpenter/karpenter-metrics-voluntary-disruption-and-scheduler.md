---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-metrics-voluntary-disruption-and-scheduler
name: karpenter-metrics-voluntary-disruption-and-scheduler
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [metrics, disruption, scheduler, consolidation, queue-depth, decisions]
level: advanced
status: docs-checked
description: "Karpenter voluntary disruption and scheduler metrics: decisions, eligible nodes, failed validations, consolidation timeouts, queue depth, unschedulable and ignored pods."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Voluntary disruption and scheduler metrics

Voluntary disruption:
- `karpenter_voluntary_disruption_decisions_total` (STABLE): labelled by decision, reason and consolidation type.
- `karpenter_voluntary_disruption_decisions_by_nodepool_total`: same per NodePool.
- `karpenter_voluntary_disruption_eligible_nodes` (BETA): nodes eligible, labelled by disruption reason.
- `karpenter_voluntary_disruption_decision_evaluation_duration_seconds` (BETA): duration of the decision evaluation, labelled by method and consolidation type.
- `karpenter_voluntary_disruption_failed_validations_total` (ALPHA): candidates selected for disruption that failed validation, labelled by consolidation type.
- `karpenter_voluntary_disruption_queue_failures_total` (BETA): times an enqueued disruption decision failed, labelled by method.
- `karpenter_voluntary_disruption_consolidation_timeouts_total` (BETA): times the consolidation algorithm reached a timeout, labelled by consolidation type.

Scheduler:
- `karpenter_scheduler_scheduling_duration_seconds` (STABLE): simulation time for provisioning and deprovisioning.
- `karpenter_scheduler_queue_depth` (BETA): pods waiting to be scheduled.
- `karpenter_scheduler_unschedulable_pods_count` (number of unschedulable pods), `karpenter_scheduler_ignored_pods_count` (pods ignored during scheduling), `karpenter_scheduler_unfinished_work_seconds` (work in progress not yet observed by scheduling_duration_seconds); all ALPHA.
- `karpenter_scheduler_pending_pods_by_effective_zone_count` (ALPHA): pending pods by effective zone constraint, with values a zone name, `flexible` or `none`.

## Checked

2026-11-08. Confirmed against the Metrics reference (v1.13) (names, stability levels, descriptions). Removed the "Diagnosis patterns" section (allowed_disruptions interpretation, churn and batching advice) and reworded failed-validation, queue-failure and timeout meanings to match the page; added missing stability levels.

Method: documentation only; no commands were run.

