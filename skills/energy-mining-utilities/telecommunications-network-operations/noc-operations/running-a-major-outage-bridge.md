---
id: energy-mining-utilities.telecommunications-network-operations.noc-operations.running-a-major-outage-bridge
name: running-a-major-outage-bridge
category: energy-mining-utilities
field: telecommunications-network-operations
product: noc-operations
tags: [noc-operations, telecommunications-network-operations, noc, network-operations-centre, network-operations-center, outage-bridge, major-incident, incident-commander, p1, sev1, alarm-correlation, root-alarm, service-impact, fibre-cut, power-outage, escalation, field-dispatch, vendor-tac, status-updates, change-freeze, rollback, service-restoration, mttr, post-incident-review, itil]
level: practitioner
status: draft
description: "Run a telecom NOC major outage bridge: declare it, find the root alarm, split restoration from diagnosis, dispatch field and vendor, keep timed updates and close with a clean timeline."
sources: ["ITIL major incident management concepts (paraphrased)", "Common carrier NOC practice"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a major outage bridge

**Goal:** when a large part of the network goes down — a fibre cut taking out a ring, a
core router failure, a power loss at an exchange — get service back fast by putting
one person in charge, keeping the right people on a single call, and separating
"restore now" from "understand later". The NOC owns the bridge even when the fix is
in someone else's hands.

## 1. Declare early
Criteria are set by your severity matrix (customers affected, critical services such
as emergency calls, enterprise SLAs). If in doubt, declare — a P1 stood down after ten
minutes costs little; a P1 declared an hour late costs a lot.
On declaration:
- Name the **incident commander (IC)** — usually the NOC shift lead. The IC runs the
  call and makes decisions; they do not troubleshoot.
- Open the bridge (conference line + chat channel + incident ticket). Post the
  bridge details to the call-out list.
- Assign a **scribe** who keeps the timeline in the ticket.

## 2. Find the root alarm
- In an outage, the alarm list fills with consequences: hundreds of downstream
  loss-of-signal or BGP-down alarms. Sort by **first occurrence time** and by
  network layer — power and transport (optical, microwave) alarms before IP/service
  alarms.
- Look for the common point: same fibre route, same site, same card. A topology view
  or alarm correlation in the OSS helps; trust it but check.
- Ask "what changed?": the change calendar for the last 24 hours. Many outages are
  changes — check before dispatching anyone.

## 3. Restore first, diagnose second
- **Restoration options**, roughly fastest first: roll back a recent change, switch
  to protection/redundant path, reroute traffic, power to a generator, swap a card.
- Dispatch the **field technician** (or splicing crew for a cut) as soon as a
  physical cause is likely — travel time is usually the longest part of MTTR.
- Engage **vendor TAC** with logs already collected; give them the case priority that
  matches.
- Freeze other changes in the affected area until the incident is closed.

## 4. Run the call
- Roll call: who is on and in which role.
- Every 15–30 minutes (match your SLA), the IC states: current impact, what's being
  tried, next update time. Customer care and management get the same summary in
  writing — they should not need to join the bridge.
- Keep side conversations off the main call: technical deep dives go to a breakout
  and report back.
- Each action gets an owner and a time: "Field ETA 40 minutes, Alex owns".

## 5. Close and learn
- Confirm service restoration from **customer-side** measures (probe results,
  traffic levels back, test calls), not just alarms clearing.
- Stand down the bridge with a final update; keep the ticket open for root cause.
- **Post-incident review** within days: timeline, root cause, what slowed restoration,
  actions with owners. Blameless, factual.

## Gotchas
- Two people giving instructions on the bridge = no one in charge.
- Field crews entering a manhole or climbing a pole are not reachable on the bridge —
  agree check-in times.
- Power outages: batteries give a few hours; generator fuel and site access are the
  real constraint.
- Uncertain: severity criteria, update intervals and regulatory outage-reporting
  thresholds (e.g. FCC NORS in the US, Ofcom in the UK) vary — check your licence obligations.

## Verify
- [ ] IC and scribe named at declaration; bridge details sent.
- [ ] Root alarm identified, recent changes checked.
- [ ] Restoration path chosen and field/vendor engaged with owners and ETAs.
- [ ] Timed updates sent on schedule to stakeholders.
- [ ] Restoration confirmed from service measures; review scheduled; regulatory report filed if required.
