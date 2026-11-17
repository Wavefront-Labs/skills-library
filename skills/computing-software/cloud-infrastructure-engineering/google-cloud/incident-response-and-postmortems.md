---
id: computing-software.cloud-infrastructure-engineering.google-cloud.incident-response-and-postmortems
name: incident-response-and-postmortems
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, incident-response, postmortem, incident-management, on-call, incident-commander, blameless-postmortem, severity-levels, personalized-service-health, cloud-status, support-escalation, communications-lead, war-room, timeline, action-items, incident-metrics, mttr, pagerduty, game-days]
level: advanced
status: docs-checked
description: "Run incidents on GCP the SRE way: severities, roles (IC, ops, comms), a first-response checklist (Service Health, audit logs), Google support escalation, blameless postmortems."
sources: ["https://sre.google/sre-book/managing-incidents/", "https://sre.google/sre-book/postmortem-culture/", "https://sre.google/workbook/incident-response/", "https://docs.cloud.google.com/service-health/docs/overview", "https://docs.cloud.google.com/support/docs/customer-care-procedures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident response and postmortems

**Goal:** when the pager fires, everyone knows who decides, who fixes, who talks, and what
to check first on GCP — and afterwards the organisation learns something it can act on.

## 1. Severity (decide before the incident)
| Sev | Definition | Response |
|---|---|---|
| **SEV1** | customer-facing outage or data loss/exposure; fast SLO burn; revenue stopped | page IC + ops lead + comms immediately, exec notified, status page updated |
| **SEV2** | degraded for many users or one critical function; fast burn | page on-call, IC assigned, regular updates on an agreed cadence |
| **SEV3** | limited impact, workaround exists, slow burn | business hours, ticket |
| **SEV4** | no user impact (internal tooling, near-miss) | ticket |
Tie severities to **SLO burn rate** (see `slo-monitoring-and-error-budgets`) so the first responder does not have to argue about it. Anyone can declare; the IC can downgrade.

## 2. Roles
- **Incident Commander (IC)**: owns the incident, assigns work, decides on mitigations (rollback, failover, feature flag), keeps the timeline; does not debug.
- **Operations lead**: hands on the keyboard; may delegate to subject experts.
- **Communications lead**: status page, internal channel, customer support, exec updates on a cadence.
- **Scribe** (can be the IC for small incidents, or a bot): timeline in the incident channel.
Hand-offs at shift boundaries are explicit ("you are now IC"). One channel per incident (`#inc-<DATE>-payments`), one video bridge, one doc.

## 3. First 15 minutes on GCP
1. **Is it us or Google?** Personalized Service Health (console → Service Health; `gcloud beta service-health events list --location=global` lists incident events) and the Google Cloud status page; subscribe to alerts beforehand. If Google: mitigate (failover region, degrade gracefully), open a P1 support case, do not spend the hour debugging your code.
2. **What changed?** Cloud Deploy/Cloud Build last releases; Admin Activity audit log for the recent window (`protoPayload.methodName` on IAM, firewall, org policy, Cloud SQL, GKE); Terraform applies; feature flags. Most incidents follow a change — **roll it back first**, understand later.
3. **Blast radius**: SLO dashboards per service, LB 5xx by backend, Error Reporting new groups, GKE workload Observability tab, Cloud SQL/Spanner CPU and connections, Pub/Sub oldest unacked age, quota dashboard (429s).
4. **Mitigate**: traffic rollback (`gcloud run services update-traffic`, Cloud Deploy `targets rollback`, MIG `rolling-action start-update` to previous template), scale (raise max instances, add nodes), shed load (Cloud Armor rate limit, disable expensive features), failover (Cloud SQL `failover`, promote replica, DNS/LB to secondary region per `ha-dr-design`).
5. **Communicate** at the cadence; the first update says "we know, we are on it, next update at HH:MM".
Keep a runbook index linked from every alert (see `alerting-policies-and-notification-channels`).

## 4. Escalating to Google
- Response time depends on case priority and your support service (see the Technical Support Services Guidelines). Open the case with: project ID, affected resources, timestamps in UTC, error messages/trace IDs, what changed, **impact statement**. P1 means the application or infrastructure is unusable in production with no quick workaround; P1 cases follow the sun by default.
- Escalate through the case (escalate option; Premium Support customers can also contact the TAM) — not by filing duplicates. Provide `gcloud` output and audit log excerpts; ask for the Google-side incident ID if one exists.
- For security incidents: Security Command Center findings and Access Transparency logs, plus your own IR plan (rotate keys/SA credentials, revoke tokens, snapshot disks for forensics before rebuilding).

## 5. Postmortem (promptly)
Blameless; template: summary, impact (users, duration, SLO budget consumed, revenue), timeline (detection → mitigation → resolution with timestamps from the channel), root cause(s) and triggers, what went well / what went badly / where we got lucky, **action items** with owner, priority and due date in the tracker (prevent, detect faster, mitigate faster), lessons. Review in a weekly ops meeting; track action-item completion as a metric. Incidents caused by Google go in too — your action is usually "multi-region" or "degrade gracefully".
Metrics worth keeping: time to detect, time to mitigate, number of SEV1/2 per quarter, share of action items closed on time.

## 6. Practice
- **Game days**: kill a zone (drain GKE node pool, `simulate-maintenance-event`), fail over Cloud SQL, revoke a service account, exhaust a quota — on purpose, in staging then prod with a budget.
- **Wheel of misfortune**: replay past incidents with a new on-caller as IC.
- Update runbooks after every exercise; retire alerts that did not help.

## Gotchas
- Debugging in the IC seat is the most common failure mode; if the IC starts typing `kubectl`, hand off IC.
- Rolling back a deploy does not roll back a schema migration or a Pub/Sub schema; know which changes are reversible before the incident.
- Audit logs lag minutes; "nothing changed" is only true after they catch up.
- Opening a P1 for a dev project wastes your credibility with support; severity must match impact.
- Postmortems with "be more careful" as an action item produce nothing — actions must be tests, alerts, limits or automation.

## Checked
2026-10-31. Confirmed against the Google Cloud Customer Care procedures page (P1 definition, follow-the-sun default for P1, escalation via the case, TAM for Premium Support), the `gcloud beta service-health events list` reference (global location for incident events), and the SRE book and workbook incident and postmortem chapters (roles, blameless culture). Removed unconfirmed: support-plan response-time table, the 10x burn, 15/30-minute and 80 percent figures, 5-working-day deadline, Mandiant, and the dead architecture-framework source. Severity levels and cadences are team policy, not documented facts. Other gcloud commands were verified by check_commands.
Method: documentation only; no commands were run.

## Verify
- [ ] On-call rota, severity table, roles and the first-15-minutes checklist are in a runbook linked from every P1/P2 alert.
- [ ] Service Health alerts route to the on-call channel (test with the "test notification" or a past event).
- [ ] Last quarter's game day produced at least one fix that shipped; postmortem action items are closed on time.
- [ ] A support P1 dry run (or a real one) achieved first response within the plan's SLA.
