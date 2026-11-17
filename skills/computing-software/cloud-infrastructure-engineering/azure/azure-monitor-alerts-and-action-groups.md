---
id: computing-software.cloud-infrastructure-engineering.azure.azure-monitor-alerts-and-action-groups
name: azure-monitor-alerts-and-action-groups
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor, alerts, metric-alerts, log-alerts, alert-rules, action-groups, alert-processing-rules, dynamic-thresholds, activity-log-alerts, service-health-alerts, resource-health-alerts, smart-detection, alert-severity, alert-suppression, maintenance-suppression, itsm-connector, webhook, common-alert-schema, pagerduty, opsgenie, multi-resource-alerts, alert-fatigue]
level: practitioner
status: docs-checked
description: "Design Azure Monitor alerting: metric alerts with dynamic thresholds, log alerts, service and resource health alerts, action groups, processing rules, severity hygiene."
sources: ["https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-types", "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-dynamic-thresholds", "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/action-groups", "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-processing-rules", "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-common-schema", "https://learn.microsoft.com/en-us/cli/azure/monitor/alert-processing-rule"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Monitor alerts — rules, action groups and the discipline that prevents fatigue

**Goal:** every alert maps to a runbook and an owner; nothing pages at night that can
wait; platform incidents reach you before users; maintenance doesn't flood the channel.

## 1. Action groups first (one per audience, not per alert)
```bash
az monitor action-group create -g rg-ops -n ag-platform-oncall --short-name plat-oncall \
  --action email oncall oncall@example.com --action webhook pagerduty https://events.pagerduty.com/integration/<key>/enqueue usecommonalertschema \
  --action armrole Owner "Owner"            # notifies subscription Owners
az monitor action-group create -g rg-ops -n ag-platform-info --short-name plat-info --action webhook teams https://<teams-workflow-url> usecommonalertschema
```
- Prefer the **common alert schema** so one parser handles alerts from every signal type (see the common alert schema page for the field list).
- Email, SMS, voice and push notifications are rate limited across all subscriptions (webhooks and other actions are not); the limits are on the Azure Monitor service limits page.
- Two groups minimum: **oncall** (Sev0–1, pages) and **info** (Sev2–4, chat/ticket). Test with `az monitor action-group test-notifications create`.

## 2. Metric alerts
```bash
az monitor metrics alert create -g rg-ops -n "vm-cpu-high" --scopes /subscriptions/<sub> --target-resource-type Microsoft.Compute/virtualMachines --target-resource-region uksouth \
  --condition "avg Percentage CPU > 90" --window-size 15m --evaluation-frequency 5m --severity 2 --action ag-platform-info --auto-mitigate true
az monitor metrics alert create ... --condition "avg Percentage CPU > dynamic medium 2 of 4" --window-size 5m --evaluation-frequency 5m   # dynamic threshold
```
- **Multi-resource** rules (subscription or resource-group scope plus resource type and region) cover every matching resource, including future ones.
- **Dynamic thresholds** learn from historical data: 10 days are used to find hourly or daily seasonality, weekly seasonality after three weeks, and a rule does not fire until it has three days and at least 30 samples. Threshold sensitivity Medium or Low reduces noise. They cannot be used on rules with multiple conditions, or on log search rules with 1-minute frequency.
- Metric alerts are **stateful** by default: one fired alert until the condition clears (`--auto-mitigate`).

## 3. Log alerts (KQL)
```bash
az monitor scheduled-query create -g rg-ops -n "app-5xx-rate" --scopes <law-id> --severity 1 --evaluation-frequency 5m --window-size 10m \
  --condition "count 'Placeholder_1' > 50 resource id AppRoleName" \
  --condition-query Placeholder_1="AppRequests | where ResultCode startswith '5'" \
  --action-groups ag-platform-oncall --auto-mitigate true --mute-actions-duration 30m
```
The CLI condition grammar is awkward; the same rule can be defined in Bicep/ARM (`Microsoft.Insights/scheduledQueryRules`): query, measure, aggregation granularity, dimension split, threshold, number of violations to trigger, auto-mitigate and mute-actions duration. Log alerts can also be stateful or stateless.
Use log alerts for errors/rates from app logs, a missing heartbeat (`Heartbeat | summarize max(TimeGenerated) by Computer | where max_TimeGenerated < ago(10m)`), security events, anything joining tables.

## 4. Platform-level alerts you must have
- **Service Health**: `az monitor activity-log alert create -n svc-health --condition "category=ServiceHealth" --scope /subscriptions/<sub> --action-group ag-platform-oncall`.
- **Resource Health** alerts (`category=ResourceHealth`) for VMs/SQL/App Service.
- **Activity log** alerts on administrative operations you care about (role assignment writes, NSG rule writes, resource deletes), with `level=Error` variants for failures.

## 5. Processing rules and suppression
```bash
az monitor alert-processing-rule create -g rg-ops -n "suppress-patch-window" --rule-type RemoveAllActionGroups --scopes /subscriptions/<sub> \
  --filter-resource-type Equals Microsoft.Compute/virtualMachines --schedule-recurrence-type Weekly --schedule-recurrence Saturday \
  --schedule-recurrence-start-time 02:00:00 --schedule-recurrence-end-time 06:00:00 --schedule-time-zone "<time zone>"
az monitor alert-processing-rule create -g rg-ops -n "add-sec-team" --rule-type AddActionGroups --scopes /subscriptions/<sub> --action-groups ag-sec --filter-severity Equals Sev0 Sev1
```
Rule types are `RemoveAllActionGroups` (suppress notifications, for example during patching) and `AddActionGroups` (add groups by severity, resource type, resource group and other filters). Keep the rule names and schedules in code.

## 6. Hygiene
- Write down a severity contract (Sev0 outage → page; Sev1 degraded → page in business hours; Sev2 act today; Sev3 informational; Sev4 verbose) and apply it consistently.
- Every rule: `description` with the runbook link and owner; tags `team`, `runbook`.
- Review the fired-alert history regularly; tune or delete rules that fire without action.
- Deploy rules via Bicep/Terraform so they are reviewed.

## Gotchas
- Metric alerts on a stopped resource show no data; add a heartbeat log alert for the "it vanished" case.
- Log alert evaluation depends on ingestion latency; use a window comfortably longer than your ingestion delay.
- Dynamic thresholds on a brand-new resource stay silent until enough data exists (three days and 30 samples).

## Verify
- [ ] Test notification to each action group arrives with the common schema fields populated.
- [ ] Simulate a breach: the alert fires within evaluation frequency + window and resolves after the fix.
- [ ] A Service Health alert rule exists at every subscription.
- [ ] Processing rule window: alerts during the patch window appear in the Alerts view but no notification is sent.

## Checked
2026-10-28. Confirmed on the Azure Monitor alert types, dynamic thresholds, action groups and Alert processing rules pages and the `az monitor alert-processing-rule` reference: stateful metric and log alerts, dynamic threshold data requirements (10 days, three weeks, three days and 30 samples), Medium/Low sensitivity advice, multi-condition and 1-minute-log limits, rate limiting scope (SMS, voice, push, email), processing rule types, `--filter-resource-type`, `--filter-severity`, schedule flags. CLI commands checked with check_commands (corrected `--filter-target-resource-type`). Removed: email 100/hour figure, 93-day metric retention, evaluation-frequency bounds, per-alert-type schema field names, Sev tag policy, AMBA recommendation, action-group scope remark, the specific Activity log operation names and smart-detection routing.
Method: documentation only; no commands were run.
