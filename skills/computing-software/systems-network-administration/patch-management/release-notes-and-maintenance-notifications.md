---
id: computing-software.systems-network-administration.patch-management.release-notes-and-maintenance-notifications
name: release-notes-and-maintenance-notifications
category: computing-software
field: systems-network-administration
product: patch-management
tags: [release-notes, maintenance-notification, user-communication, status-page, release-management, change-communication]
level: practitioner
status: draft
description: "Communicate releases and maintenance: notification lead times, a clear notice template (what, when, impact, action), release notes contents, channels and completion messages."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-release-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release notes and maintenance notifications

**Goal:** users and stakeholders know what is changing, when, and what (if anything) they must do; the service desk is never surprised.

## Lead times (example policy)
| Impact | Notice |
|---|---|
| Full outage of a customer-facing service | 10 business days, reminder 1 day before |
| Degraded service / short outage in window | 5 business days |
| No user impact (redundant patching) | Change schedule only; service desk informed |
| Emergency | As soon as decided; explain why short notice |

## Maintenance notice template
- **Subject**: "[Planned maintenance] Payroll portal unavailable Sat 24 Oct 22:00-23:30 UTC"
- **What**: plain-language description ("security updates to the servers running the payroll portal").
- **When**: start and end with timezone; local time conversions for global audiences.
- **Impact**: what users will notice (unavailable, slow, need to sign in again).
- **Action required**: save work, avoid submitting forms, none.
- **Contact**: service desk channel; status page link.

## Release notes (for software releases)
Version and date; new features; changes in behaviour; fixed issues (with ticket IDs); known issues and workarounds; upgrade or rollback notes; links to documentation. Keep separate audiences in mind: user-facing notes vs technical notes for support.

## Channels
Status page with subscription (email/SMS/RSS), email lists by service, service desk briefing note, ITSM change record link. Post "started", "completed" and "extended" updates.

## Gotchas
- Jargon ("applying LCU KB5040442") belongs in technical notes, not user notices.
- Forgetting the completion message leaves users unsure whether problems are expected.

## Verify
Service desk tickets during maintenance windows mostly reference the notice rather than asking whether there is an outage.
