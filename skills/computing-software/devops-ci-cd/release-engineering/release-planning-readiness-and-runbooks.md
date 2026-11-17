---
id: computing-software.devops-ci-cd.release-engineering.release-planning-readiness-and-runbooks
name: release-planning-readiness-and-runbooks
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, release-plan, release-strategy, release-checklist, release-readiness, go-no-go, release-runbook, deployment-runbook, rollback-plan, release-captain, release-notes, stakeholder-communication, change-window, maintenance-window, status-page, dependency-coordination, big-bang-release, first-release, cutover-plan, dress-rehearsal, post-release-verification, smoke-checks, war-room, release-retrospective]
level: practitioner
status: draft
description: "Plan a non-routine release: release strategy and readiness checklist, go/no-go criteria, a step-by-step runbook with owners and rollback triggers, comms and status page, verification, retro."
sources: ["Humble & Farley, Continuous Delivery (2010), ch. 10 Deploying and Releasing Applications - Creating a Release Strategy, Deploying for the First Time", "https://sre.google/sre-book/release-engineering/", "https://sre.google/workbook/on-call/", "https://www.atlassian.com/incident-management/handbook/postmortems"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Release planning, readiness and runbooks

**Goal:** for the releases that aren't push-button yet (first launch, big migration,
coordinated multi-team cutover, regulated change), everybody knows the plan, the
abort criteria and their job — and the plan gets simpler every time.

## 1. Release strategy (write once per product, CD ch. 10)
A one-page document agreed with ops, security and product: who approves releases; how
artifacts are promoted; which environments exist and who owns them; deployment method
(rolling/blue-green/canary) and rollback approach; how config and secrets are managed;
monitoring and alerting expectations; data migration rules; freeze windows; how the
first deployment differs from steady state. Revisit when any of these changes. For
routine continuous deployment this document *is* the pipeline; this skill covers the
exceptions.

## 2. Readiness checklist (go/no-go inputs)
- [ ] Artifact passed every pipeline stage; version and digest recorded.
- [ ] Changes since last release listed (release notes draft); risky ones flagged.
- [ ] Database migrations rehearsed on a prod-sized copy; timings known; backward-compatible (expand/contract) or downtime approved.
- [ ] Rollback tested: previous version redeployable; data rollback plan if migrations are not reversible.
- [ ] Feature flags default to **off** for new features; kill switches wired.
- [ ] Monitoring: dashboards + alerts for the new/changed paths exist; SLOs defined; synthetic checks ready.
- [ ] Capacity: load test on the release candidate or justified skip; scaling limits reviewed.
- [ ] Security: scans clean or exceptions signed; secrets rotated if required; pen-test findings closed.
- [ ] Dependencies: upstream/downstream teams, vendors, partners informed and aligned on sequence.
- [ ] Support: customer support briefed; FAQ/known issues; status page components ready.
- [ ] People: release captain, deployer, verifier, comms owner named and available; on-call aware; no key person on leave.
- [ ] Timing: change window agreed; not Friday 17:00; not during a freeze or a peak.
Go/no-go: a 15-minute meeting (or async thread) where each owner says go/no-go against
the checklist; a single no-go with a reason stops the release. Record the decision.

## 3. The runbook
Numbered steps, each with **owner, command/click, expected result, verification, time
estimate**, and the rollback action for that step:
```
T-24h  Comms: announce window on status page + customer email (comms owner)
T-1h   Freeze merges to release branch; confirm artifact v2.3.0 digest sha256:… (captain)
T-15m  War room open (video + chat channel #rel-2-3-0); dashboards up (captain)
T-0    1. Enable maintenance banner (deployer) — verify banner visible
       2. Run migration 0042 (expand) — expected < 4 min; verify row count; ROLLBACK: migration 0042 down (tested)
       3. Deploy v2.3.0 to canary 5 % (deployer) — verify error rate < 0.5 %, p95 < 400 ms for 10 min; ROLLBACK: redeploy v2.2.4
       4. Ramp 25 % → 50 % → 100 % at 10-min intervals with the same checks (deployer+verifier)
       5. Run post-release smoke suite (verifier) — all green
       6. Enable flag `new-checkout` for internal users; then 10 % customers (product)
       7. Remove banner; comms "complete" (comms owner)
T+2h   Hypercare: watch dashboards; on-call briefed; abort criteria still apply
T+1d   Contract migration 0043 (drop old columns) after confirming no reads (DBA)
```
Abort criteria are written *before* the release (error rate, latency, failed smoke,
support ticket spike) and whoever is verifier can call abort without debate. Keep the
runbook in the repo (`docs/releases/2.3.0.md`), fill it in live, and it becomes the record.

## 4. Rehearse
For first-time or high-risk releases: a dress rehearsal in staging following the runbook
literally, timed. Every manual step found in the rehearsal is a candidate for automation
before the real thing. Migrations get a rehearsal on a fresh prod snapshot (also tests
the restore procedure).

## 5. Communication
Status page component + scheduled maintenance entry (even for zero-downtime releases,
state "deploying, no impact expected"); internal channel with a pinned timeline; a
template for customer-facing notes (what changed, what to do, where to ask). During the
release: one person posts updates at fixed intervals (every 15 min or at each step);
silence reads as failure. After: "complete" message with version and link to release notes.

## 6. Verification after deploy
Smoke suite (read-only journeys with synthetic accounts), synthetic monitors, key
business metrics compared with the same hour last week (orders/min, sign-ups,
conversion), error budget burn rate, and a manual look at the top 3 user flows. Define
"done" as "verifier signs off", not "deploy job green".

## 7. Retrospective
Within a week: what took longer than planned, which steps were manual, what surprised
us, what the abort criteria missed. Output = tickets that automate or delete steps.
The measure of release engineering maturity is that this runbook gets *shorter* each
release until it is a pipeline with a button.

## Verify
- [ ] Runbook exists for the release with owners, timings, verification and rollback per step.
- [ ] Go/no-go recorded with named approvers and checklist state.
- [ ] Dress rehearsal (or migration rehearsal) done and timed for anything irreversible.
- [ ] Post-release retro produced at least one automation ticket; the next runbook is shorter.
