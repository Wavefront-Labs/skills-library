---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.correlating-faults-with-recent-changes
name: correlating-faults-with-recent-changes
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, change-correlation, change-management, reliability-monitor, timeline, windows-update, audit-logs, incident-timeline]
level: practitioner
status: draft
description: "Answer 'what changed?' quickly: build a timeline from change records, Reliability Monitor, update and install logs, MDM and identity audit logs, then prove cause by rollback."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/monitor-audit-logs"
  - "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# correlating-faults-with-recent-changes

Most faults that start suddenly follow a change. Find the first-seen time, then look for
changes just before it.

## Pin the start
First ticket time, the user's "it was fine yesterday", monitoring graph step changes.
Narrow to the hour if you can.

## Sources of change, by layer
| Layer | Where to look |
|---|---|
| Planned IT changes | ITSM change records filtered by affected CI/service and date |
| Windows device | Reliability Monitor (`perfmon /rel`): installs, updates, app failures per day; `Get-HotFix`; `Get-WinEvent -ProviderName Microsoft-Windows-WindowsUpdateClient`; MsiInstaller events 11707/11724 |
| Drivers | `Get-WinEvent -LogName Microsoft-Windows-Kernel-PnP/Configuration` or Setup log; Device Manager driver date |
| Intune/MDM | Tenant admin > Audit logs (policy and assignment edits), app deployment history |
| Identity | Entra audit logs (Conditional Access, app, group changes), sign-in logs for policy results |
| Network/security | Firewall/proxy change logs, certificate expiries, DNS changes |
| Vendor/SaaS | Service health dashboards and release notes |

## Build a timeline
Put fault symptoms and candidate changes on one timeline with timestamps (same time zone).
Changes affecting exactly the affected population (and not the unaffected) rank first;
combine with an IS/IS NOT spec (see kepner-tregoe-is-is-not-analysis).

## Prove it
Correlation is not cause. Roll back or exclude a small pilot group from the suspect
change; the symptom should stop for them only. Then raise a change to roll back or fix
properly and link it to the incident/problem.

## Gotchas
- Unrecorded changes (emergency fixes, vendor auto-updates, user installs) exist; Reliability
  Monitor and audit logs catch what the CAB did not.
- Certificate and password expiries are "changes" with no change record.

## Verify
The incident/problem record holds the timeline, the change identified, and the pilot
rollback result that confirms it.
