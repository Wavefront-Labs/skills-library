---
id: computing-software.qa-testing-engineering.test-case-design.release-readiness-go-no-go
name: release-readiness-go-no-go
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [release-readiness, go-no-go, exit-criteria, release-decision, risk-acceptance, quality-gates]
level: practitioner
status: draft
description: "Run a release readiness / go-no-go assessment: evidence against exit criteria, open defect review, residual risk, rollback readiness and who decides."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Release readiness and go/no-go

**Goal:** a release decision based on evidence, made by the people who own the risk.

## Inputs (prepared by QA)
1. **Exit criteria** status with numbers: planned tests run %, pass %, requirement/risk coverage, automated regression results.
2. **Open defects** by severity with workaround and customer impact; any waivers requested.
3. **Non-functional results**: performance vs targets, security scan/pen test findings, accessibility.
4. **Residual risks**: what is untested or weakly tested and what could happen.
5. **Operational readiness**: monitoring, alerts, runbooks, on-call, rollback plan tested, feature flags for risky parts, staged rollout plan.
6. **Changes since last test run** (late fixes) and their retest status.

## Meeting (15-30 min)
Product owner, engineering lead, QA, ops/SRE, support. QA presents facts and recommendation; the product/business owner decides; decision and accepted risks recorded.

## Possible outcomes
Go; go with conditions (staged rollout 5% -> 25% -> 100% with metric gates, known issues published); no-go with specific blockers and re-assessment date.

## Gotchas
- QA as sole gatekeeper makes QA the scapegoat; QA informs, owners decide.
- Late "small" fixes skipping regression are a classic cause of incidents.

## Verify
Decision record exists with criteria evidence, accepted risks and named decision maker.
