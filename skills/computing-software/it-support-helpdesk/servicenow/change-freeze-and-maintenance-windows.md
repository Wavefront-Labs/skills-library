---
id: computing-software.it-support-helpdesk.servicenow.change-freeze-and-maintenance-windows
name: change-freeze-and-maintenance-windows
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, change-management, change-enablement, change-freeze, maintenance-window, blackout-schedule, itil-4]
level: practitioner
status: draft
description: "Run change freezes and maintenance windows: blackout schedules in ServiceNow, exception approvals, communicating windows to users, and what support may still do during a freeze."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# change-freeze-and-maintenance-windows
Goal: changes land when the business can absorb them, and the riskiest
business periods are protected from avoidable change.

## Maintenance windows
- Define recurring windows per service with the service owner (e.g.
  Tue/Thu 22:00-02:00 local for core infrastructure; Sunday 06:00-10:00
  for ERP). Document user-visible impact in the service catalog.
- In ServiceNow, create **Maintenance schedules** (`cmn_schedule` of type
  maintenance) and link to CIs or CI classes; the change conflict checker
  then flags changes scheduled outside the window.
- Announce windows once (service catalog, intranet) and then per change
  only when users will notice an outage.

## Change freezes (blackouts)
- Typical: financial year-end close, peak trading (Black Friday through
  New Year), exam periods, major go-lives, staff holiday shutdowns.
- Create a **Blackout schedule**; changes planned in it fail conflict
  detection and need an exception.
- Publish the freeze calendar at least a quarter ahead so teams pull work
  forward instead of requesting exceptions.

## Exceptions
- Allowed: emergency changes restoring service, security fixes for actively
  exploited vulnerabilities, standard changes explicitly whitelisted.
- Exception request names the business risk of waiting vs risk of doing;
  approved by the change manager plus service owner (sometimes CIO).
- Track exception count per freeze; many exceptions mean the freeze is
  too broad or planning was poor.

## What the service desk can still do
Password resets, standard requests, user-level fixes and pre-approved
standard changes continue. Tier 2 must not push "small" config tweaks
(GPO edits, Intune assignments to all users) without an exception; these
are changes even if no RFC culture exists around them.

## Gotchas
- Freezes push work to the days just before and after; staff the desk for
  the post-freeze change surge.
- Automated pipelines (Intune update rings, WSUS approvals, vendor SaaS
  releases) ignore your freeze unless you pause them; list and pause them.
- Time zones: express windows in UTC plus local in the schedule.

## Verify
Scheduling a test change inside a blackout raises a conflict in
ServiceNow, and the freeze calendar is visible to all change requesters.
