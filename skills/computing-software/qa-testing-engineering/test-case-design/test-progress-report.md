---
id: computing-software.qa-testing-engineering.test-case-design.test-progress-report
name: test-progress-report
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-progress-report, test-reporting, test-monitoring, test-status-report, istqb]
level: practitioner
status: docs-checked
description: "Write a test progress (status) report: progress against plan, quality signals, blockers, risks and decisions needed, for a daily, sprint or weekly audience."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test progress reports

**Goal:** regular, short reports that let stakeholders steer during testing. Different from the end-of-phase test completion report.

## Template
```
Test progress report - Release 4.2 - week 3 of 4 - 2026-10-16
Status: AMBER (on scope, 2 days behind on payments)

Progress
- Executed 312/410 planned (76%); passed 289, failed 17, blocked 6
- Risk coverage: 9/12 high risks fully tested; R3, R7, R11 in progress
- Exploratory: 7/10 charters done

Quality
- Open defects: 2 critical, 5 major, 11 minor (new this week: 9, closed: 14)
- Hotspot: payments service (8 of 18 open)

Blockers and risks
- Payment sandbox down since Tue (6 tests blocked) - owner: Ops, ETA Fri
- Soak test environment not booked - risk to R7

Decisions needed
- Accept descoping of IE-mode tests? (low risk, saves 1 day)

Next period
- Finish payments regression, start soak test Monday
```

## Rules
- Lead with status (RAG) and the decisions needed; numbers support, not lead.
- Compare to plan and to last report (trend arrows).
- Name owners and dates for blockers.
- Audience-specific: daily stand-up = blockers; steering = risk and dates.
- Automate the numbers from the test management tool and CI; spend writing time on interpretation.

## Gotchas
- Green on numbers but amber in reality: say so; RAG is a judgement.
- Blocked tests are not "not run"; separate them so the cause is visible.

## Verify
Report states status, progress vs plan, quality hotspots, blockers with owners, and explicit decisions, and stakeholders can act without asking follow-up questions.

## Checked

2026-10-28. Confirmed: Template and rules are judgement and carry no source-specific claims. Removed: Syllabus section number and the ISO/IEC/IEEE 29119-3 attribution (the cited page is 29119-1, not 29119-3).

Method: documentation only; no commands were run.
