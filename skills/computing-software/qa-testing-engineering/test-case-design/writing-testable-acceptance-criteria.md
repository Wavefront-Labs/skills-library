---
id: computing-software.qa-testing-engineering.test-case-design.writing-testable-acceptance-criteria
name: writing-testable-acceptance-criteria
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [acceptance-criteria, scenario-based-testing, testable-requirements, rule-oriented-criteria, scenario-oriented-criteria, istqb]
level: practitioner
status: draft
description: "Write acceptance criteria that are testable: rule-oriented lists or scenario-oriented Given-When-Then, with explicit boundaries, negatives and non-functional limits."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing testable acceptance criteria

**Goal:** criteria that define done unambiguously and translate directly into tests. ISTQB CTFL v4.0 4.5.2.

## Two formats
**Rule-oriented** (bullet list):
- Password must be 12-64 characters.
- Account locks for 15 minutes after 5 failed attempts within 10 minutes.
- Locked users see "Try again in N minutes" and no hint whether the user exists.

**Scenario-oriented** (Given/When/Then):
```
Given an account with 4 failed attempts in the last 10 minutes
When the user enters a wrong password
Then the account is locked for 15 minutes
And the response time is under 1 second
```

## Checklist for each criterion
- Observable outcome (what the user/system visibly does).
- Concrete numbers and inclusive/exclusive boundaries.
- At least one negative/error criterion.
- Non-functional limits where relevant (performance, accessibility "keyboard operable", security).
- No implementation detail ("uses Redis") unless it is a real constraint.
- Independent of UI layout unless layout is the requirement.

## Gotchas
- "Works as designed in Figma" is not a criterion; list the behaviours.
- Too many criteria (more than ~8) signals the story should be split.

## Verify
Hand criteria to someone else: they write the same expected results you would.
