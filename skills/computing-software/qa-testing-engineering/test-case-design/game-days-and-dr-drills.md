---
id: computing-software.qa-testing-engineering.test-case-design.game-days-and-dr-drills
name: game-days-and-dr-drills
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [game-day, dr-drill, disaster-recovery-testing, chaos-engineering, reliability-testing, rto-rpo]
level: advanced
status: docs-checked
description: "Run game days and disaster recovery drills: scenario design, blast radius limits, roles, measuring RTO and RPO against targets, and turning findings into fixes."
sources:
  - https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/
  - https://principlesofchaos.org/
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Game days and disaster recovery drills

**Goal:** rehearse real failures with real people and runbooks, measure recovery against RTO/RPO, and find the gaps before an incident does.

## Plan
1. **Scenario:** a hypothesis such as "if the primary DB region fails, we restore service in the secondary within the agreed RTO and RPO". Draw from past incidents and the risk register.
2. **Scope and blast radius:** staging first; production only with steady-state monitoring, a stop button and approval. Pick a time with on-call coverage and no releases.
3. **Roles:** facilitator, incident commander, operators, observer/scribe, comms. Operators should be the real on-call people, not the experts who wrote the runbook.
4. **Success metrics:** RTO (time to restore service), RPO (data loss window, measured by the last committed record found after restore), customer-visible error rate, runbook accuracy.
5. **Abort criteria** written in advance.

## Run
- Inject the failure (shut down instances, block network paths, revoke credentials, corrupt a replica, delete a test bucket) or simulate via tabletop if risk is too high.
- Scribe timestamps: detection, page, diagnosis, decision, recovery steps, service restored, data verified.
- Do not help responders beyond what an incident would provide; that is the test.

## Measure RPO concretely
Write a heartbeat row every few seconds before the drill; after restore, the newest heartbeat present gives the actual data loss window.

## After
Blameless review within days: timeline, measured RTO/RPO vs target, runbook steps that were wrong or missing, alerting gaps, action items with owners and dates. Re-run the scenario after fixes.

## Verify
The drill report shows measured RTO and RPO against target with evidence timestamps, and each finding has an owned action item.

## Checked

2026-10-28 Confirmed against: Principles of Chaos Engineering (minimise blast radius, run experiments in production when ready, automate). Removed or generalised: the AWS deep link (it redirected to the guide root and returned no text, so the root is cited instead), the example RTO/RPO figures, and the NACL detail.

Method: documentation only; no commands were run.
