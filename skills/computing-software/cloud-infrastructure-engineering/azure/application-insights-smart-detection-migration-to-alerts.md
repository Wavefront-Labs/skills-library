---
id: computing-software.cloud-infrastructure-engineering.azure.application-insights-smart-detection-migration-to-alerts
name: application-insights-smart-detection-migration-to-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-insights, smart-detection, smart-detection-migration, failure-anomalies-alert-rule, anomaly-detection]
level: practitioner
status: docs-checked
description: "Migrate Application Insights smart detection rules to alert rules, configure the Failure Anomalies alert, route notifications through action groups and tune noise."
sources: ["https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-smart-detections-migration", "https://learn.microsoft.com/azure/azure-monitor/alerts/proactive-failure-diagnostics", "https://learn.microsoft.com/azure/azure-monitor/alerts/resource-manager-alerts-smart-detection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smart detection to alert rules

**Goal:** get smart detection findings through normal action groups and alert management.

## Background
- Migrating creates one **alert rule** per migrated smart detection capability. The rules use action groups, can be
  managed like other Azure Monitor alert rules, and support alert processing rules. The migration is documented as preview;
  it does not change detection algorithms or behaviour, and it is applied per Application Insights resource (resources not
  migrated keep working as before).
- **Failure Anomalies** (abnormal rise in failed requests) is already an alert rule, created automatically with the
  Application Insights resource, and needs no migration. Its action group is named "Application Insights Smart Detection".

## Migrate
Portal: Application Insights, Investigate, Smart detection, then the banner *Migrate smart detection to alerts (Preview)*. Or CLI:
```bash
az rest --method POST --uri /subscriptions/<sub>/providers/Microsoft.AlertsManagement/migrateFromSmartDetection?api-version=2021-01-01-preview --body @body.txt
```
The body has a `scope` array, `actionGroupCreationPolicy` (`Auto` or `Custom`; blank means Auto) and, for Custom,
`customActionGroupName`. Auto maps the old email settings to an action group named "Application Insights Smart Detection"
(reused if it exists; default notification goes to Monitoring Contributor and Monitoring Reader users). ARM templates can also
trigger it per resource.

| Smart detection rule | Alert rule after migration |
|---|---|
| Degradation in server response time | Response latency degradation |
| Degradation in dependency duration | Dependency latency degradation |
| Degradation in trace severity ratio | Trace severity degradation |
| Abnormal rise in exception volume | Exception anomalies |
| Potential memory leak detected | Potential memory leak |
Not converted and no longer supported afterwards: slow page load time, slow server response time, long dependency duration,
potential security issue, abnormal rise in daily data volume.

## After migration
- Alerts entry of the resource: set Signal type to **Smart Detector** to list only smart detection alerts; the Smart Detection feed
  still shows detections.
- Failure Anomalies needs a minimum amount of data and takes 24 hours to learn normal behaviour. It uses an adaptive minimum
  failure percentage tied to request volume, may auto-resolve if the issue is gone for 8-24 hours (no notification on resolve),
  and the rule can be deleted (`az resource delete --ids <rule resource id>`).

## Verify
- [ ] The resource's alert rules list (Signal type Smart Detector) contains one rule per migrated capability.

## Checked
2026-10-28. Confirmed in Learn alerts-smart-detections-migration and proactive-failure-diagnostics: migration steps and az rest command,
body fields and policy values, action group naming, rule mapping table and unsupported detectors, Failure Anomalies behaviour. The
Resource Manager smart detection page returned 404. Removed: the Bicep Failure Anomalies rule (api version, detector id, severity and
frequency not confirmed), the incorrect detector list (abnormal rise in daily data volume is not converted), the static log alert and
SLO tuning advice, and the az resource list verification.
Method: documentation only; no commands were run.
