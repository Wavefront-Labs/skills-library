---
id: computing-software.qa-testing-engineering.exploratory-testing.bug-bash-and-bug-hunt
name: bug-bash-and-bug-hunt
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [bug-bash, bug-hunt, experience-based-testing, exploratory-testing, whole-team-testing]
level: practitioner
status: draft
description: "Run a bug bash: scope and charters, participants and roles, environment and data prep, logging and dedup, triage and follow-up within days."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bug bashes and bug hunts

**Goal:** a time-boxed session where many people (developers, PMs, designers, support, testers) explore the product to find issues fast, typically before a release or launch.

## Prepare (a week before)
- **Scope:** features, platforms and builds in scope; known issues list so people do not refile them.
- **Charters:** 6-12 areas with a focus ("checkout on mobile Safari with vouchers", "admin bulk import of 10k rows"); assign pairs to charters, mix roles.
- **Environment:** stable build deployed, test accounts per participant with varied roles and data, feature flags set, devices booked.
- **Logging:** one channel or a form with required fields (title, steps, expected/actual, device, screenshot); a triage team of 2-3 watching in real time.
- **Incentives:** small prizes for most severe, most unusual, best-written report.

## Run (60-120 minutes)
1. Kickoff 10 min: goals, scope, how to log, what is known.
2. Explore in pairs; switch charters halfway.
3. Triage team deduplicates and asks for missing info live.
4. Wrap-up 15 min: top findings, thanks.

## Follow up (same week)
- Triage every report: duplicate, not a bug, bug with severity/priority, improvement.
- Publish a summary: counts by area and severity, top issues, decisions.
- Fix-or-defer decisions recorded; release decision updated.

## Gotchas
- Unstable builds waste everyone's time; smoke-test the build beforehand.
- Without charters people all test the login page.
- Floods of duplicates if the known-issues list is missing.
- Do not let it replace systematic testing; it complements it.

## Verify
All reports triaged within 3 working days, summary shared, and high-severity issues tracked to resolution.
