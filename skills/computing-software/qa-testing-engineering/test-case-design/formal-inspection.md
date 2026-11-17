---
id: computing-software.qa-testing-engineering.test-case-design.formal-inspection
name: formal-inspection
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [inspection, formal-review, static-testing, reviews, fagan-inspection, review-roles, review-metrics, review-moderator]
level: practitioner
status: docs-checked
description: "Run a formal inspection: roles (moderator, author, scribe, reviewers), entry criteria, individual checking with checklists, logging meeting, rework, follow-up and metrics."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Formal inspection

**Goal:** the most rigorous review type, for high-risk work products (safety requirements, security-critical code, contracts, architecture). ISTQB CTFL v4.0 3.2; ISO/IEC 20246.

## Roles
Moderator (facilitator, owns process), author, scribe/recorder, reviewers with assigned perspectives (tester, user, maintainer, security), manager (decides what is reviewed and provides resources). The author cannot be review leader or scribe.

## Process
1. **Planning**: scope, purpose, quality characteristics, focus areas, exit criteria, effort and timeframe; review in small chunks.
2. **Kick-off**: objectives, materials, roles.
3. **Individual review**: each reviewer applies a technique (checklist-based, scenario-based) and logs anomalies, recommendations and questions.
4. **Communication and analysis**: anomalies are discussed in a review meeting; decide status, owner and actions for each, and the quality level of the work product.
5. **Rework** by author.
6. **Follow-up**: raise a defect report per defect, verify fixes against the exit criteria, report results.
7. **Metrics**: collect and use them to improve the SDLC and the inspection process.

## Gotchas
- Meetings that turn into design debates kill inspections; moderator parks solutions.
- Evaluating participants must never be a review objective.
- Using defect counts to evaluate authors destroys the process.

## Verify
Anomaly log shows reviewers' individual findings, all majors resolved and verified at follow-up, and metrics recorded.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): sections 3.2.2 to 3.2.5 (generic review process, roles, inspection as the most formal type with metrics and author not leading or scribing, success factors).
Removed: size limits, checking rates, meeting length, entry-criteria specifics and defect-density metrics that the syllabus does not give, and the unread ISO source.
Method: documentation only; no commands were run.
