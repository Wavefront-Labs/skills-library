---
id: computing-software.qa-testing-engineering.exploratory-testing.test-checklists
name: test-checklists
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [test-checklists, checklist-based-testing, experience-based-testing, regression-checklist, heuristics]
level: practitioner
status: draft
description: "Build and maintain checklist-based testing: derive items from defects and standards, keep them high-level, version them, retire stale items, and measure their yield."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/test-analyst
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building and maintaining test checklists

**Goal:** a short, living list of conditions to check, giving consistency without the cost of scripted cases (ISTQB CTFL 4.4.3 checklist-based testing).

## Where items come from
- Escaped defects and post-mortems ("date pickers ignore timezone").
- Standards: WCAG, OWASP ASVS, platform guidelines (iOS HIG, Material).
- Recurring review comments and support tickets.
- Heuristics: SFDIPOT, HICCUPPS, CRUD, boundaries.

## Writing items
- One condition per item, phrased as a question that a tester can answer yes/no: "Does every form show inline errors on submit with JS disabled?"
- Keep items high-level enough to allow variation (each run explores a little differently, reducing the pesticide paradox).
- Group by area (forms, auth, i18n, accessibility, error handling, performance smells).
- 15-40 items per list; longer lists stop being read.

## Example (web form checklist excerpt)
```
[ ] Required fields marked and announced to screen readers
[ ] Max-length enforced client and server side
[ ] Paste, autofill and IME input work
[ ] Double-submit does not create duplicates
[ ] Server error keeps entered data
[ ] Back button after submit does not resubmit
```

## Maintenance
- Store in the repo or test management tool, versioned with the product.
- Each item has an owner and a "last found a bug" date; review quarterly.
- Retire items that have not found a defect in many cycles and are now automated.
- Add an item for every escaped defect class, not every individual bug.

## Gotchas
- Checklists drift into scripts; if an item needs steps, it belongs in an automated test.
- Ticking without testing: ask for a note or evidence on failed or risky items.

## Verify
Checklist is versioned, each item is answerable, and the yield (defects found per item) is reviewed at least each release.
