---
id: computing-software.qa-testing-engineering.test-case-design.requirements-and-story-testability-review
name: requirements-and-story-testability-review
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [requirements-review, testability-review, static-testing, reviews, ambiguity-review, user-story-review]
level: practitioner
status: draft
description: "Review requirements and user stories for testability: ambiguous words, missing error cases, contradictions and unmeasurable non-functional statements, before coding starts."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Requirements and user story testability review

**Goal:** find defects in the test basis, where they are cheapest to fix. ISTQB CTFL v4.0 3.1, CTAL-TA v4.0 5.

## Checklist
- **Ambiguous words**: fast, easy, user-friendly, appropriate, etc., some, usually, support, handle. Ask: measured how?
- **Missing negatives**: what happens on invalid input, timeout, empty list, duplicate, concurrent edit, no permission?
- **Boundaries undefined**: "orders over 100": is 100 included? currency? before or after tax?
- **Contradictions** between stories, between story and UI design, between text and examples.
- **Non-functional without numbers**: "should be fast" -> "p95 < 500 ms at 200 req/s".
- **Undefined terms**: glossary missing ("active customer"?).
- **Untestable**: depends on things the tester cannot observe or control; ask for logs, test hooks, or a seam.
- **Story INVEST**: small enough, has acceptance criteria, independent.

## Output
Comments on the story/ticket, each with a proposed rewording or a question. Example:
> "Users are locked out after several failed logins" -> how many attempts, in what time window, how long is the lock, does a password reset unlock it?

## Gotchas
- Reviewing only the happy path text misses the biggest gaps: absent behaviour. Ask "what else could happen here?".
- Raise ambiguity as a question, not an accusation; the business owner may know an answer nobody wrote down.

## Verify
After review, each acceptance criterion can be turned into at least one test with an unambiguous expected result.
