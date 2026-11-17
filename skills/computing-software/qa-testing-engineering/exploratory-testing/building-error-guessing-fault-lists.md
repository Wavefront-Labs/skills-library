---
id: computing-software.qa-testing-engineering.exploratory-testing.building-error-guessing-fault-lists
name: building-error-guessing-fault-lists
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [fault-lists, error-guessing, experience-based-testing, fault-taxonomy, defect-history]
level: practitioner
status: draft
description: "Build and maintain error guessing fault lists from defect history, taxonomies and checklists, and turn them into fault attacks per feature type."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building error guessing fault lists

**Goal:** make error guessing (CTFL v4.0 4.4.1) systematic: a curated list of likely mistakes, attacked deliberately.

## Sources for the list
- Your own defect tracker: group the last 6-12 months of escaped and found defects by cause.
- Incident postmortems.
- Published taxonomies: Kaner/Falk/Nguyen appendix of common software errors, Beizer's bug taxonomy, OWASP Top 10 for security, ODC defect types.
- Developers: "what part of this code scares you?"

## Structure
Organise by feature type, each entry phrased as a testable attack:
| Area | Fault | Attack |
|---|---|---|
| Input | no trimming | enter " value " with spaces |
| Input | length not checked server-side | 10,000-char string via API |
| Numbers | rounding | 0.005 amounts, currency with 0 or 3 decimals |
| Dates | timezone | create at 23:30 local in UTC+10 |
| Lists | empty / one / pagination edge | 0, 1, page-size, page-size+1 items |
| State | double submit | double-click Pay, browser back after submit |
| Errors | unhandled dependency failure | stub returns 500 / timeout |
| Files | odd names | unicode, spaces, 255 chars, same name twice |
| Auth | IDOR | change ID in URL to another user's |

## Using it
1. Before testing a feature, pick the relevant sections; turn entries into a short charter or checklist.
2. Log which entries found defects; promote them, retire entries that never find anything.
3. Feed recurring faults into prevention: lint rules, shared validators, review checklist.

## Gotchas
- A generic list gets stale and ignored; keep it product-specific and short per section.
- Error guessing finds only what someone imagined; combine with systematic techniques.

## Verify
The fault list is versioned, each entry has a source (defect ID or taxonomy), and session notes reference which entries were applied.
