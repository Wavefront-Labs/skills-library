---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.dirt-disaster-exercise-planning
name: dirt-disaster-exercise-planning
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [dirt-exercise, disaster-exercise-planning, disaster-recovery-testing, game-day, business-continuity]
level: advanced
status: draft
description: "Plan and run a DiRT-style disaster recovery exercise: scenario selection, test proposals with risk and rollback, approvals, comms, execution, abort criteria and findings."
sources: ["https://sre.google/sre-book/testing-reliability/", "https://queue.acm.org/detail.cfm?id=2371516"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DiRT disaster exercise planning

Google's Disaster Recovery Testing (DiRT) runs company-wide exercises that cause real failures (data
centre loss, key people unavailable, authentication down) to find gaps in technology and process before a
real disaster does (ACM Queue, "Weathering the Unexpected").

## Scenario sources
- Loss of a region/zone or a whole cloud provider service.
- Loss of a critical internal service (auth, DNS, config, secrets manager).
- People scenarios: the only expert is unreachable; the incident channel tool is down.
- Data scenarios: restore from backup into a clean environment.
- Supplier failure: a SaaS dependency unavailable for 24 h.

## Test proposal template (each test reviewed before approval)
```
Title:            Fail over primary Postgres in eu-west to replica
Owner:            <team>          Date/time window: <UTC>
Hypothesis:       failover < 2 min, < 0.1% failed writes, no data loss
Scope/blast radius: checkout writes in eu-west only
Risk:             medium. Worst case: replica lag causes data loss up to 5 s
Prerequisites:    replica lag < 1 s; backup verified within 24 h
Abort criteria:   error rate > 5% for 3 min, or any data integrity check fails
Rollback plan:    promote original primary (runbook link), tested in staging on <date>
Comms:            notify support and status-page owner 24 h before; incident channel #dirt-2026q4
Observers:        <names>; scribe <name>
```

## Running it
1. Go/no-go check 1 h before: system healthy, error budget available, no ongoing incidents.
2. Announce start; responders act as if real (unless the test is to measure detection, then on-call is
   not told).
3. Coordinator watches abort criteria; anyone can call abort.
4. Record timeline and surprises.

## Findings
- Rank by severity; each finding gets an owner and due date like postmortem action items.
- Repeat failed tests next cycle to confirm fixes.

## Gotchas
- Start with tests in staging and low-risk production scopes; expand as confidence grows.
- Exercises that "pass" every time are too easy; raise difficulty.
- Real incidents during a test: abort the test and restore immediately.

## Verify
- [ ] Every test has an approved proposal with abort criteria and a rehearsed rollback.
- [ ] Findings tracked and re-tested.
