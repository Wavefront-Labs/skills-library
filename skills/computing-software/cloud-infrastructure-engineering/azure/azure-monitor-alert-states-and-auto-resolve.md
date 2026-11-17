---
id: computing-software.cloud-infrastructure-engineering.azure.azure-monitor-alert-states-and-auto-resolve
name: azure-monitor-alert-states-and-auto-resolve
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor, alert-state, auto-resolve, stateful-alerts, alert-processing-rules]
level: practitioner
status: docs-checked
description: "Understand Azure Monitor alert condition vs user response state, stateful vs stateless log alerts, auto-resolve timing, and how to close or suppress alerts."
sources: ["https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-overview", "https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-manage-alert-instances", "https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-create-log-alert-rule", "https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-processing-rules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Monitor alert states and auto-resolve

**Goal:** know why an alert is still "Fired", why you got (or did not get) a resolved notification, and how to manage the queue.

## Two independent states
| State | Values | Set by |
|---|---|---|
| **Monitor condition** | Fired, Resolved | The platform, when the condition stops being true (stateful rules only) |
| **Alert state** (user response) | New, Acknowledged, Closed | People or automation (portal, Alert Management REST API) |
The user response does not change until a user or automation changes it.

## Stateful vs stateless
| Rule type | Behaviour |
|---|---|
| Stateless | Fires each time the condition is met; condition is always Fired |
| Stateful metric alert | Resolved when the condition isn't met for three consecutive checks |
| Stateful log search alert | Resolved when the condition isn't met for a time range that depends on frequency (1 min: 10 min; 5-15 min: three periods; 15 min-11 h: two periods; 11-12 h: one period) |
| Activity log alerts | Always stateless |

In the portal, **Automatically resolve alerts** makes a log search alert stateful, and **Mute actions** sets a wait before actions trigger again.

## Managing the queue
Use Azure Resource Graph with the `AlertsManagementResources` schema to query alerts across subscriptions, and the Alert Management REST API to update fired alerts.

Suppress during maintenance with **alert processing rules** (action: remove all action groups, with schedule), not by disabling rules.

## Gotchas
- Stateful alerts are deleted after 30 days, but the alert condition is kept until the alert resolves.
- Log alert resolution waits for the frequency-dependent time range above, so low-frequency rules resolve slowly.
- Fired alert instances are read-only; configuration changes apply only to future alerts.
- The alert payload field `data.essentials.monitorCondition` tells fired from resolved.

## Verify
- [ ] Test rule fires, then resolves, and the webhook payload shows `"monitorCondition": "Resolved"`.

## Checked

Date: 2026-10-28.

Confirmed against Learn (alerts-overview, create-or-edit alert rule, alerts-processing-rules): monitor condition Fired/Resolved versus user response New/Acknowledged/Closed, stateless versus stateful behaviour, metric three-checks and log time-range resolution table, 30-day deletion with stored condition, activity log alerts stateless, Automatically resolve and Mute actions options, monitorCondition payload field, AlertsManagementResources via Resource Graph.
Removed: `az monitor alert update` (no such command), autoMitigate/muteActionsDuration Bicep property names and per-type defaults, Service Health row, example REST changestate URL and Resource Graph query, dimension-resolution claim.

Method: documentation only; no commands were run.
