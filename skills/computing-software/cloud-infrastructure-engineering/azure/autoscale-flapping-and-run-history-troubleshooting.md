---
id: computing-software.cloud-infrastructure-engineering.azure.autoscale-flapping-and-run-history-troubleshooting
name: autoscale-flapping-and-run-history-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, autoscale, autoscale-flapping, autoscale-run-history, autoscaleevaluations, vmss, app-service-autoscale]
level: practitioner
status: docs-checked
description: "Debug Azure Monitor autoscale: why it didn't scale or flapped, run history, AutoscaleEvaluations logs, threshold gaps, cooldowns, profiles and metric sources."
sources: ["https://learn.microsoft.com/azure/azure-monitor/autoscale/autoscale-troubleshoot", "https://learn.microsoft.com/azure/azure-monitor/autoscale/autoscale-flapping", "https://learn.microsoft.com/azure/azure-monitor/autoscale/autoscale-best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoscale troubleshooting

**Goal:** explain every autoscale decision (or non-decision) and stop out/in oscillation.

## Where to look
- Autoscale setting > **Run history** chart: instance count over time and scale actions.
- Activity log: "Autoscale scale up/down completed/failed" events.
- Diagnostic settings on the autoscale setting send evaluation records to the `AutoscaleEvaluationsLog` table (metric values and rule results).
```kusto
AutoscaleEvaluationsLog
| where TimeGenerated > ago(6h)
| project TimeGenerated, OperationName, MetricData, ObservedValue, Threshold, EstimateScaleResult
```

## Flapping
Before a scale-in, autoscale evaluates whether it would trigger the opposite scale event. If so it may skip the action and
reevaluate at the next run, or scale in by fewer instances than the rule says. Flapping checks apply to scale-in only, not scale-out.
Symptom: the instance count never drops and no scale event appears; check the **Run history** tab. Flapping is recorded in the activity log
(`Flapping` or `FlappingOccurred`).
Rules of thumb:
- Keep adequate margins between scale-out and scale-in thresholds.
- Use the same metric to control both scale-in and scale-out rules.
- Cool-down time can also keep a scale action from occurring.

## Didn't scale at all
- Wrong **profile**: a recurrence or fixed-date profile is active with different limits.
- Already at **max** (or min) instance count.
- Metric missing: guest OS metrics need the agent/DCR and correct namespace; Application Insights/custom metrics need
  the right resource ID; dimension filters exclude everything.
- Time aggregation/window too long to react.
- Scale action failed: quota (vCPU), allocation failure, or policy denial - check activity log.

## Notifications
Add email/webhook notifications on scale actions and failures (autoscale setting > Notify) or alerts on the activity log events.

## Verify
- [ ] Load test produces a clean scale-out then scale-in with no oscillation; evaluation logs show expected metric values.

## Checked

Date: 2026-10-28.

Confirmed against Learn (autoscale-flapping, autoscale-best-practices, autoscale-troubleshoot): flapping evaluation for scale-in only, skip or smaller scale step, Run history tab, activity log Flapping/FlappingOccurred, AutoscaleEvaluationsLog columns used in the query, cool-down note, same metric for scale-in and scale-out.
Removed: the 70/30 CPU thresholds, 5-minute cooldown and +2/-1 advice, the AutoscaleEvaluations/AutoscaleScaleActions category names, one-profile-at-a-time claim, the 10-minute average example, and the MetricName/Profile query columns.

Method: documentation only; no commands were run.
