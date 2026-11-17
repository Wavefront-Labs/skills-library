---
id: computing-software.cybersecurity-defensive.cloud-security.azure-diagnostic-settings
name: azure-diagnostic-settings
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [diagnostic-settings, azure-monitor, activity-log, resource-logs, log-analytics, azure-policy-deployifnotexists, cloud-logging]
level: practitioner
status: docs-checked
description: "Configure Azure diagnostic settings at scale: activity log and Entra logs export, resource logs per service, Log Analytics vs storage vs Event Hub, and Azure Policy enforcement."
sources: ["https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/diagnostic-settings", "https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/diagnostics-settings-policies-deployifnotexists", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-integrate-activity-logs-with-azure-monitor-logs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure diagnostic settings

Azure resources do not keep their logs anywhere useful by default: the activity log is collected automatically (use a diagnostic setting to export it), but
resource logs (data plane: Key Vault access, storage reads, SQL audit, NSG flow logs) are not collected
until a diagnostic setting sends them somewhere.

## Three levels
| Level | What | How |
|---|---|---|
| Tenant (Entra ID) | Entra sign-in and audit logs (categories are listed on the Entra "integrate activity logs with Azure Monitor logs" page) | Entra admin center -> Diagnostic settings |
| Subscription | Activity log (control plane: who created/deleted what) | Subscription diagnostic setting, all categories |
| Resource | Resource logs and metrics per service (categories differ per service) | Per resource, or by policy |

## Destinations
- **Log Analytics workspace** (Sentinel) for detection.
- **Storage account** for long retention/forensics.
- **Event Hub** for third-party SIEM.

## At scale with Azure Policy
Built-in DeployIfNotExists initiatives exist for the `allLogs` and `audit` category groups, one per destination type; assign at management group and run a remediation task for existing resources.

## Gotchas
- Up to five diagnostic settings per resource; competing teams' settings can hit the limit.

## Checked

2026-10-28: confirmed on the diagnostic settings and DeployIfNotExists policy pages: each resource can have up to five diagnostic settings, the activity log is collected without configuration, `allLogs` and `audit` category groups, one initiative per destination type. Removed: 90-day retention, P1/P2 licence note, per-service category names, resource-specific table advice, kube-audit-admin, storage sub-resource note, exact initiative title and KQL table names (not on the pages read).

Method: documentation only; no commands were run.

## Verify
- [ ] Policy compliance: all supported resources have diagnostic settings.
- [ ] Activity log entries from every subscription arrive in the workspace.
- [ ] Key Vault access events are present in the workspace.
