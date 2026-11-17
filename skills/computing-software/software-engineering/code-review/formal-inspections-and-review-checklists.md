---
id: computing-software.software-engineering.code-review.formal-inspections-and-review-checklists
name: formal-inspections-and-review-checklists
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, review-process, code-inspection, review-checklist, fagan-inspection, ieee-1028, defect-checklists]
level: practitioner
status: draft
description: "Run formal code inspections (Fagan, IEEE 1028) for high-risk code and build checklists that catch real defects: roles, preparation rates, logging defects and checklist upkeep."
sources:
  - https://ieeexplore.ieee.org/document/4601584
  - https://en.wikipedia.org/wiki/Fagan_inspection
  - https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
  - https://www.atulgawande.com/book/the-checklist-manifesto/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formal inspections and review checklists

Lightweight pull-request review suits most changes. Safety-critical, security-critical, financial, or regulated code (DO-178C, IEC 62304, ISO 26262, PCI) often needs a formal inspection with records.

## Fagan inspection / IEEE 1028 roles
- **Moderator:** plans, runs the meeting, ensures follow-up. Not the author.
- **Author:** answers questions, fixes defects; does not defend.
- **Reader:** paraphrases the code aloud, section by section.
- **Inspectors:** find defects (often each with a focus: security, concurrency, error handling, spec conformance).
- **Recorder/scribe:** logs each defect with location, type, severity.

## Process
1. **Planning:** entry criteria met (compiles, tests pass, static analysis clean); material and checklist distributed; meeting scheduled.
2. **Overview** (optional): author explains context.
3. **Preparation:** each inspector reviews alone with the checklist. Rate matters: ~150-200 lines of code per hour (SmartBear/Cisco study found defect detection drops sharply above ~400 LOC per session and after 60-90 minutes).
4. **Inspection meeting** (max 2 hours): reader walks through; defects are logged, not solved.
5. **Rework:** author fixes every logged defect.
6. **Follow-up:** moderator verifies fixes; exit criteria met. Re-inspect if rework was substantial.
7. **Metrics:** defects found per KLOC, per hour, by type - used to improve checklists and the development process, never to grade authors.

## Building a checklist that works
- **Short** (10-20 items) and **specific** to defects your team actually ships. Derive items from postmortems, escaped bugs, and static analysis gaps.
- Phrase as checks with yes/no answers, grouped by concern:
  - Error handling: every external call has a timeout and handles failure; errors are not swallowed.
  - Security: inputs validated at trust boundaries; queries parameterised; authorisation checked per object.
  - Concurrency: shared mutable state guarded; locks acquired in a consistent order.
  - Resources: files/connections closed on all paths.
  - Data: migrations reversible or expand-contract; time stored in UTC.
  - Spec: each requirement traced to code and a test.
- Drop items that never find anything or that tools now enforce; add items after each escaped defect class.
- Separate checklists for authors (self-review) and inspectors.

## Lightweight variants
Checklist-driven PR review (checklist in the PR template), pair review on screen for risky diffs, or a two-reviewer rule with one specialist for critical paths.

## Verify
- [ ] Inspection records (defect log, sign-off) stored with the change for audited code.
- [ ] Checklist revised at least quarterly from defect data.
