---
id: computing-software.cloud-infrastructure-engineering.azure.service-health-security-advisories-and-access-control
name: service-health-security-advisories-and-access-control
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, service-health, security-advisory-alerts, service-health-rbac, privacy-breach-notification]
level: practitioner
status: docs-checked
description: "Route Azure security advisories and sensitive Service Health events to the right team and control who can read them with Service Health RBAC permissions."
sources: ["https://learn.microsoft.com/azure/service-health/security-advisories-elevated-access", "https://learn.microsoft.com/azure/service-health/alerts-activity-log-service-notifications-portal", "https://learn.microsoft.com/azure/service-health/service-health-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security advisories and Service Health access

**Goal:** make sure security-relevant Azure notices reach the security team and only authorised people can see sensitive details.

## Event types
Service Health shows Service issues, Planned maintenance, Health advisories, and **Security advisories** (vulnerabilities, required actions, privacy/security incidents affecting your subscriptions).

## Elevated access for sensitive events
- Sensitive security advisory details need elevated access roles; users without them see a summary only (the security advisories elevated access page lists the roles that grant it).

## Alerts
Create an activity log alert for Service Health events in each subscription (or deploy one per subscription with Azure Policy DINE) and send it to an action group that reaches the SOC mailbox or ITSM.

## Gotchas
- Service Health alerts are per subscription; a new subscription has none until policy deploys them.
- Emails from Azure to subscription admins do not replace alerts; contacts drift.

## Verify
- [ ] Each subscription has a ServiceHealth security alert.
- [ ] A SOC analyst with the documented elevated-access role can open a security advisory's impacted resources.

## Checked
2026-10-28. Confirmed on the security advisories elevated access page: security advisories are distinct from general service issues, contain sensitive information and need elevated access roles to see all details.
Removed (not confirmed): the specific role list, the custom role JSON and `fetchEventDetails` action, the `incidentType` filter and alert CLI command, the billing-updates remark, and the `servicehealthresources` note.

Method: documentation only; no commands were run.
