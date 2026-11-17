---
id: computing-software.qa-testing-engineering.exploratory-testing.writing-a-defect-report
name: writing-a-defect-report
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [defect-report, bug-report-writing, defect-management, reproduction-steps, istqb]
level: practitioner
status: draft
description: "Write a defect report developers can act on: one-line summary, environment, minimal steps, expected vs actual with oracle, evidence, severity and isolation notes."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.iso.org/standard/81291.html
  - https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a defect report

**Goal:** a report that is reproduced at first attempt and fixed without a conversation (ISTQB CTFL 5.5; ISO/IEC/IEEE 29119-3 incident report).

## Structure
```
Title: Checkout total ignores 2nd discount code when codes are applied in reverse order

Environment: staging build 4.2.0-rc3 (a1b2c3d), Chrome 129 / macOS 15, user role: member, locale en-GB
Preconditions: basket with 1x SKU-123 (£40); codes SAVE10 and FREESHIP active

Steps:
1. Open /checkout
2. Apply FREESHIP
3. Apply SAVE10
Expected: total £36.00, shipping £0 (pricing rules doc §4.2: codes stack)
Actual: total £40.00 + £4.99 shipping; SAVE10 shown as applied
Reproducibility: 5/5; applying SAVE10 first works correctly

Evidence: screenshot, HAR (POST /api/basket/discounts response), console log
Severity: Major (wrong price charged, workaround exists)
Isolation: also on Firefox; not on build 4.1.3 -> regression
```

## Rules
- Title = symptom + condition, searchable; no "doesn't work".
- Minimal steps: remove everything not needed to reproduce; state starting data.
- Expected result cites the oracle (spec, previous version, comparable product, consistency).
- Facts, not blame or guesses; put hypotheses in a separate "Notes" section.
- One defect per report; link related ones.
- Attach evidence: screenshot/video, logs, HAR, request ids, timestamps (with timezone).
- Severity = impact; priority is set in triage.

## Gotchas
- Missing build/version makes the report unverifiable later.
- Personal data in screenshots and HAR files: redact before attaching.
- Intermittent bugs: give the frequency and the conditions tried.

## Verify
Someone else reproduced it from the report alone, and the title alone tells a triager what is wrong.
