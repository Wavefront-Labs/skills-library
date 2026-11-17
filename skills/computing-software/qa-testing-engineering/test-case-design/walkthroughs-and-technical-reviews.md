---
id: computing-software.qa-testing-engineering.test-case-design.walkthroughs-and-technical-reviews
name: walkthroughs-and-technical-reviews
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [walkthrough, technical-review, static-testing, reviews, peer-review, informal-review, review-types]
level: practitioner
status: docs-checked
description: "Choose between informal review, walkthrough and technical review, and run each well: who leads, preparation needed, typical objectives and output."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Walkthroughs and technical reviews

**Goal:** pick the review type that fits the objective and formality needed. ISTQB CTFL v4.0 3.2.4.

| Type | Led by | Preparation | Main objective | Output |
|---|---|---|---|---|
| Informal (buddy check, pairing) | Anyone | No defined process | Detect anomalies | No formal documented output |
| Walkthrough | Author | Individual review optional | Quality, education, consensus, new ideas, anomaly detection | Per team practice |
| Technical review | Moderator, technically qualified reviewers | Per team practice | Consensus and decisions on a technical problem; also anomaly detection | Decisions, anomalies |
| Inspection | Moderator (author cannot lead or scribe) | Full generic review process | Find the maximum number of anomalies | Review results, metrics (see `formal-inspection`) |

## Walkthrough
- Author presents step by step (scenario dry run on a design, test plan walkthrough with stakeholders).
- Great for testers to walk developers through test approach and for devs to walk testers through architecture.

## Technical review
- Reviewers are technical peers; focus on solving technical problems and deciding (e.g. choose caching approach, test framework, data model).
- Record decisions and rationale (ADR).

## Success factors
Clear objective per review, right participants, small chunks, time to prepare, management support, training, facilitated meetings.

## Gotchas
- Mixing objectives (teach juniors and find all defects) gives poor results on both.
- Reviews without recorded outcomes get re-litigated.

## Verify
Each review has a stated objective and a recorded outcome that answers it.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): sections 3.2.4 and 3.2.5 (review types, objectives, who leads each, inspection follows the complete generic process and collects metrics, success factors).
Removed: per-type preparation and output claims the syllabus does not make, and the 'psychological safety, checklists' success factors.
Method: documentation only; no commands were run.
