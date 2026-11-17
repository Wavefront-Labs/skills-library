---
id: business-finance.product-management.requirements-writing.prd-user-stories-and-acceptance-criteria
name: prd-user-stories-and-acceptance-criteria
category: business-finance
field: product-management
product: requirements-writing
tags: [product-management, requirements-writing, prd, product-requirements-document, one-pager, user-stories, acceptance-criteria, gherkin, given-when-then, invest, definition-of-done, edge-cases, non-goals, scope-definition, story-splitting, jira, confluence, handoff, requirements-gathering, backlog-refinement]
level: practitioner
status: draft
description: "Write a lean PRD (problem, goals, non-goals, success metrics, requirements), INVEST user stories with Given/When/Then acceptance criteria, an edge-case sweep and a clean handoff to delivery."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PRD, user stories and acceptance criteria

**Goal:** engineers and designers can build the right thing without guessing, and
everyone can tell when it's done, while the *how* stays with the people who build it.

## 1. The lean PRD (2-5 pages, living doc in Confluence/Notion/Google Docs)
1. **Problem**: who, what pain, evidence (interview quotes, data). Link discovery.
2. **Goals and success metrics**: the outcome and target number, plus guardrail
   metrics that must not get worse (e.g. latency, support tickets).
3. **Non-goals**: what this explicitly won't do. The most useful section for
   preventing scope creep and misreadings.
4. **Users and scenarios**: the main flows in plain language.
5. **Requirements**: numbered, prioritised (must / should / could), each testable.
6. **Edge cases and error states** (section 4 below).
7. **Dependencies, risks, open questions** with owners and due dates.
8. **Rollout**: flags, phasing, migration, who is told.
Leave out technical design; link the engineering design doc instead. Keep a changelog
at the top; requirements drift silently otherwise.

## 2. User stories that pass INVEST
"As a <specific user>, I want <capability> so that <benefit>."
INVEST: Independent, Negotiable, Valuable, Estimable, Small (fits in a sprint, ideally
a few days), Testable. The "so that" is mandatory: it lets engineers propose a cheaper
way to the same benefit.
**Split** big stories by workflow step, by business rule, by data variation, by happy
path vs errors, or by platform, never by technical layer (a "backend story" delivers
no user value and can't be demoed).

## 3. Acceptance criteria
Write them as **Given / When / Then** (Gherkin-style) for behaviour:
```
Given an invoice with status "Draft"
When the user clicks "Send"
Then the status changes to "Sent"
And the customer receives an email within 5 minutes
And the "Send" button is no longer shown
```
Or as a checklist for simpler rules. Each criterion must be **verifiable by someone
other than you**: numbers instead of "fast", named states instead of "appropriately".
Keep team-wide quality items (tests, accessibility, analytics events) in a shared
**Definition of Done** rather than repeating them per story.

## 4. Edge-case sweep (run this list on every feature)
- Empty state, first use, one item, many items (pagination, 10k rows).
- Invalid input, too long, special characters/emoji, other languages and RTL.
- Permissions: who can't see/do this? What do they see instead?
- Concurrency: two users editing; double-click submit; retries.
- Failure: network loss, third-party down, partial success.
- Time: time zones, daylight-saving shifts, month-end, leap day.
- Money: currency, rounding, refunds, negative values.
- Data lifecycle: deletion, export, existing data migration.
- Analytics: which events prove the success metric moved?

## 5. Handoff to delivery
Walk the team through the PRD live (not by link drop); invite challenges to scope.
Refine stories with engineers in backlog refinement; estimates and splits come from
them. Stay available during the build for questions; answer within hours, not days,
and record decisions back in the doc/ticket.

## Gotchas
- Specifying UI pixel-by-pixel in the PRD duplicates and conflicts with design files.
- "Should" requirements without priority all become "must" in practice.
- Acceptance criteria written after the build are test descriptions, not requirements.
- Unclear authority: state who signs off scope changes.

## Verify
- [ ] PRD has non-goals, a success metric with a target, and named open-question owners.
- [ ] Every story has a "so that" and is small enough for a sprint.
- [ ] Every acceptance criterion is testable by a QA engineer who wasn't in the meeting.
- [ ] Edge-case sweep done and answers recorded.
- [ ] Analytics events for the success metric are specified.
