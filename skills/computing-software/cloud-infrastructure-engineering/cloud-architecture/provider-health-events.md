---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.provider-health-events
name: provider-health-events
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, ecosystem-roles, provider-health-events, aws-health, azure-service-health, google-personalized-service-health, scheduled-maintenance, status-page]
level: practitioner
status: draft
description: "Route provider health events (AWS Health, Azure Service Health, Google Personalized Service Health) into on-call and change processes, including maintenance and retirements."
sources: ["https://docs.aws.amazon.com/health/latest/ug/what-is-aws-health.html", "https://learn.microsoft.com/azure/service-health/overview", "https://cloud.google.com/service-health/docs/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Consuming provider health and service events

Public status pages lag and are not account-specific. Use the account-scoped feeds.

## Sources
| Provider | Feed | Integration |
|---|---|---|
| AWS | AWS Health (Health Dashboard, `aws health describe-events`, organizational view) | EventBridge rule on `source: aws.health` -> SNS/Chat/ITSM |
| Azure | Service Health (service issues, planned maintenance, health advisories, security advisories), Resource Health | Activity Log alerts on `ServiceHealth` category -> action groups |
| Google Cloud | Personalized Service Health | Alerting policies / Pub/Sub, API |

## Event types to route
- **Active incidents** affecting your regions/services -> incident channel and on-call.
- **Scheduled maintenance** and **retirements** (instance retirement, runtime/TLS deprecations,
  certificate rotations) -> ticket to the owning team with due date.
- **Account notifications** (abuse reports, exposed keys) -> security queue immediately.

## Setup steps
1. Enable organisation-wide aggregation (AWS Health organizational view; Azure alerts at
   subscription scope via policy; Google at org/folder level).
2. Create rules per event category with different routing.
3. Enrich with resource tags -> owner (lookup table) so tickets land with the right team.
4. Add provider incidents to your incident timeline automatically.
5. Review retirements weekly in the ops meeting.

## Gotchas
- Without org view, events land only in the member account nobody watches.
- Health events cover provider faults, not your misconfiguration; still need your own SLO alerts.
- Do not page on informational advisories; route by category.

## Verify
- [ ] Test event (AWS: sample event via EventBridge; Azure: test action group) reaches on-call.
- [ ] Open retirement notices all have a ticket and owner.
