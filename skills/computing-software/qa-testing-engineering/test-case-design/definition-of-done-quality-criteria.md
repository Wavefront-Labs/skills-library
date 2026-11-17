---
id: computing-software.qa-testing-engineering.test-case-design.definition-of-done-quality-criteria
name: definition-of-done-quality-criteria
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [definition-of-done, exit-criteria, quality-criteria, agile-testing, istqb]
level: practitioner
status: docs-checked
description: "Write a definition of done with real quality criteria: tests at the right levels, coverage, non-functional checks, no open critical defects, docs and deployability."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://scrumguides.org/scrum-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Definition of done: quality criteria

**Goal:** "done" means potentially releasable, with testing built in. Scrum Guide (Definition of Done).

## Example DoD (story level)
- Acceptance criteria verified; acceptance tests automated and passing in CI.
- Unit tests for new logic; coverage of new code >= agreed level with meaningful assertions.
- Code reviewed; static analysis and security scan gates passed.
- Exploratory session done for user-facing changes, notes attached.
- Accessibility checks (automated scan + keyboard pass) for UI changes.
- No open critical/major defects for the story; minor ones logged.
- Performance budget respected (if story touches hot paths).
- Feature flag state and rollout plan documented; monitoring/alerts added for new endpoints.
- Docs/release notes updated.
- Deployed to staging by the pipeline.

## Release-level DoD
Regression suite green, non-functional test results within targets, release notes, rollback tested.

## Making it work
- Keep it short enough to fit on one screen; teams ignore long lists.
- Review it at retros: add a criterion when an escaped defect shows a gap, drop ones that add no value.

## Gotchas
- "Done except testing" is not done; do not count points.
- Criteria that depend on another team (security review) need an SLA or they become permanent blockers.

## Verify
Pick finished stories randomly; check each DoD item has evidence (CI link, session notes, scan result).

## Checked

2026-10-28. Confirmed: Scrum Guide: Definition of Done as a quality commitment of the Scrum Team. Removed: Syllabus section number, the "exit criteria = DoD" mapping, the 80% coverage example and a named scanner.

Method: documentation only; no commands were run.
