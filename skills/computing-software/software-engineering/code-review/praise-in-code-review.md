---
id: computing-software.software-engineering.code-review.praise-in-code-review
name: praise-in-code-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, review-praise, positive-feedback, team-culture, recognition]
level: intro
status: docs-checked
description: "Give useful praise in code review: specific positive comments on good decisions, tests and clean-ups, why it matters for learning and morale, and how to keep it genuine."
sources: ["https://google.github.io/eng-practices/review/reviewer/looking-for.html", "https://google.github.io/eng-practices/review/reviewer/comments.html", "https://conventionalcomments.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Praise and positive feedback in review

Google's guide: "If you see something nice in the CL, tell the developer, especially when they
addressed one of your comments in a great way. Code reviews often just focus on mistakes, but
they should offer encouragement and appreciation for good practices as well."

## Why bother
- People learn from reinforcement of what they do well, not only from what they could do
  better. Google's guide adds that telling a developer what they did right can be even
  more valuable for mentoring than telling them what they did wrong.
- Include why you liked something, which encourages the developer to keep the practice.
- Typical praise targets: cleaning up a messy algorithm, exemplary test coverage, or
  something you learned from the change.

## Make it specific
| Weak | Useful |
|---|---|
| "LGTM, nice!" | "praise: the table-driven test makes the edge cases easy to scan; I'll copy this pattern." |
| "Good job" | "Splitting the migration into expand/contract steps means we can roll back the deploy safely. Thanks." |
| "+1" | "Nice catch on the time-zone bug in `due_date`; that would have bitten EU customers." |

Praise decisions, not just output: deleting code, adding a missing test, a clear PR description,
measuring before optimising, asking for help early, gracefully handling feedback.

## Keep it genuine
Conventional Comments advises leaving at least one praise comment per review, never false
praise (which it says can be damaging), and sincerely looking for something to praise.

## Labels
Conventional Comments defines `praise:` as highlighting something positive, for example
`praise: Beautiful test!`.

## Checked

2026-11-08. Read in full: Google eng-practices "What to look for in a code review" (Good Things section and the quoted sentence) and "How to write code review comments"; the Conventional Comments home page (praise label, one per review, no false praise). Removed: the compliment sandwich, reactions and team-channel advice, and the mtlynch.io source (page only read for relevance, praise claims not found there).

Method: documentation only; no commands were run.
