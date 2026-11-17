---
id: computing-software.systems-network-administration.patch-management.change-schedule-and-freeze-periods
name: change-schedule-and-freeze-periods
category: computing-software
field: systems-network-administration
product: patch-management
tags: [change-schedule, change-freeze, forward-schedule-of-change, maintenance-window, blackout-period, change-enablement]
level: practitioner
status: draft
description: "Run a change schedule with maintenance windows, freeze and blackout periods, a security-patch exception route during freezes, collision detection and stakeholder publication."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change schedule and freeze periods

**Goal:** everyone can see what changes when, risky periods are protected, and urgent security fixes still get through.

## The change schedule
A calendar of authorised changes (often called the forward schedule of change) plus planned outages (projected service outage). Each entry: change ID, CIs/services, window, implementer, risk.
- Publish to service desk, service owners and major customers.
- Use it in risk assessment to detect collisions.

## Maintenance windows
Pre-agreed recurring windows per service or tier (e.g. Tier 3 servers Wednesday 22:00-02:00, Tier 0 one node per Saturday). Agreements with business owners mean patching inside a window needs no fresh negotiation.

## Freeze and blackout periods
- **Freeze**: only emergency and pre-approved changes (e.g. year-end close, retail peak, major launches).
- **Blackout**: no changes at all on specified services (e.g. trading systems during market hours).
Announce dates well ahead and plan patch cycles around them (patch earlier, not later).

## Security exception route during freezes
Define in policy that exploited/KEV vulnerabilities on exposed systems may proceed as emergency changes during freezes, with named approvers. Without this, freezes create predictable exposure windows that attackers can exploit.

## Practices
- Freeze calendars live in the ITSM tool so the RFC form warns automatically.
- After a freeze, expect a change backlog; schedule it over several windows to avoid a spike in failures.

## Gotchas
- Long freezes (6+ weeks) push patch latency beyond SLAs; record the risk and the decision.
- Changes approved but not executed should drop off the schedule, or the calendar loses trust.

## Verify
Every implemented change in the period appears in the schedule beforehand, and no non-emergency changes landed in freeze periods.
