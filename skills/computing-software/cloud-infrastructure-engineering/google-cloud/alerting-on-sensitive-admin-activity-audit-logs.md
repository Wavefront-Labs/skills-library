---
id: computing-software.cloud-infrastructure-engineering.google-cloud.alerting-on-sensitive-admin-activity-audit-logs
name: alerting-on-sensitive-admin-activity-audit-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-audit-logs, audit-log-alerting, iam-change-alerts, log-based-alerts, cloud-monitoring, security-monitoring]
level: practitioner
status: docs-checked
description: "Alert on privileged IAM grants and other sensitive changes using log-based alerting policies (LogMatch) over Admin Activity audit logs, with rate limiting and auto-close."
sources: ["https://docs.cloud.google.com/logging/docs/alerting/log-based-alerts", "https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Alerting on sensitive admin activity

## 1. Filters worth alerting on
| Event | Filter (Logging query language) |
|---|---|
| Owner / IAM admin granted | `protoPayload.methodName="SetIamPolicy" AND protoPayload.serviceData.policyDelta.bindingDeltas.action="ADD" AND protoPayload.serviceData.policyDelta.bindingDeltas.role=("roles/owner" OR "roles/resourcemanager.organizationAdmin" OR "roles/iam.securityAdmin")` |

Build further filters (service-account keys, firewall rules, sinks, KMS) from the `protoPayload.methodName` values you see in real audit entries, and test each in Logs Explorer against a past event before wiring an alert.

## 2. Create the log-based alert
```json
{
  "displayName": "IAM: privileged role granted",
  "combiner": "OR",
  "conditions": [{"displayName": "privileged grant",
    "conditionMatchedLog": {"filter": "<FILTER FROM TABLE>",
      "labelExtractors": {"actor": "EXTRACT(protoPayload.authenticationInfo.principalEmail)"}}}],
  "alertStrategy": {"notificationRateLimit": {"period": "300s"}, "autoClose": "604800s"},
  "notificationChannels": ["projects/<SEC_PROJECT>/notificationChannels/<ID>"],
  "documentation": {"content": "Runbook: https://wiki.example.com/iam-grant", "mimeType": "text/markdown"}
}
```
```bash
gcloud monitoring policies create --policy-from-file=iam-grant.json --project=<SEC_PROJECT>
```

## 3. Make it org-wide
Log-based alerting policies ignore the Logs Explorer scope. A policy defined in a project scans the entries that a project-level sink routes to a log bucket for entries originating in that project. The docs do not describe alerting on entries that arrive through an organization aggregated sink, so create the policy in each project (for example by automation) rather than assuming one security-project policy covers the org.

## Gotchas
- `alertStrategy.notificationRateLimit.period` sets the minimum time between notifications (300s above); `autoClose` defaults to 7 days (604800s) and the minimum is 1800s. A log-based policy has exactly one condition and `combiner` must be `OR`. Read the incident list, not just the email.
- Terraform applies by the pipeline SA will fire alerts too; either route those to a lower-priority channel (`principalEmail!="tf@..."`) or accept and annotate. Never exclude humans.

## Verify
- [ ] Granting `roles/owner` in a sandbox project fires the alert with the actor label filled.
- [ ] Deleting a test sink triggers the tampering alert.

## Checked
2026-10-31. Confirmed on Cloud Logging "Configure log-based alerting policies" and "Understanding audit logs": LogMatch condition via `conditionMatchedLog`, `labelExtractors`, `notificationRateLimit.period`, `autoClose` default 7 days and minimum 1800s, one condition with combiner OR, `documentation.mimeType` text/markdown, `gcloud monitoring policies create --policy-from-file` (not alpha), `SetIamPolicy` with `policyDelta.bindingDeltas`, alerts scan entries routed by a project-level sink. Removed: the SA-key, org-policy, firewall, sink, KMS and public-bucket filter rows (method names not confirmed on the fetched pages); org-wide aggregated-sink alerting claim (contradicted by the page's scoping rule); notificationRateLimit-required claim.
Method: documentation only; no commands were run.
