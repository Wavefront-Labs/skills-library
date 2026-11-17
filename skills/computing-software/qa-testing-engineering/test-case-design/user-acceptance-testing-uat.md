---
id: computing-software.qa-testing-engineering.test-case-design.user-acceptance-testing-uat
name: user-acceptance-testing-uat
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [user-acceptance-testing, uat, test-levels, acceptance-testing, business-sign-off, acceptance-criteria]
level: practitioner
status: draft
description: "Run UAT with business users: scenario selection, training, environment and data, defect handling during UAT, and a clear sign-off decision."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# User acceptance testing (UAT)

**Goal:** the intended users confirm the system supports their real work, and formally accept it. ISTQB CTFL v4.0 2.2.1.

## Plan
- **Who**: real business users (not proxies), with time released from day jobs.
- **What**: business processes end to end ("month-end close", "onboard new client"), not feature-by-feature checks; the QA team has already done that.
- **Acceptance criteria**: agreed before UAT starts, e.g. "all P1 scenarios pass, no open critical defects, max 3 open major with workarounds".
- **Environment and data**: stable, production-like, with realistic (masked) data the users recognise.

## Run
1. Kick-off: train users on the tool for logging issues and on what "defect vs change request" means.
2. Provide scenario scripts with room for users to deviate (users find usability and workflow gaps).
3. Daily triage with business and dev (`defect-triage-meetings`); classify as defect, change request, training issue.
4. Track progress by scenario, not by test steps.

## Sign-off
Written acceptance by the business owner against the agreed criteria, listing known issues and workarounds.

## Gotchas
- UAT used as the first real test phase becomes a defect flood and loses user trust. Enter UAT only when system test exit criteria are met.
- Change requests disguised as defects; classify explicitly.

## Verify
Signed acceptance exists with criteria, results and open issues; no P1 scenario untested.
