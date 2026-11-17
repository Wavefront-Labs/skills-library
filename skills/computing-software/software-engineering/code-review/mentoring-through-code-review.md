---
id: computing-software.software-engineering.code-review.mentoring-through-code-review
name: mentoring-through-code-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, mentoring-review, knowledge-sharing, onboarding, junior-developers, teaching]
level: practitioner
status: draft
description: "Use code review to mentor: teaching comments with links and reasons, choosing what to teach per review, pairing on hard feedback, and growing new reviewers."
sources: ["https://google.github.io/eng-practices/review/reviewer/comments.html#mentoring", "https://abseil.io/resources/swe-book/html/ch09.html", "https://mtlynch.io/human-code-reviews-2/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mentoring through review

Code review is one of the main ways knowledge spreads in a team (Software Engineering at Google,
ch. 9). Google's guide: reviewers can leave comments that teach, labelled as optional when not
required for the change.

## Teaching comments
- Explain the principle, not just the fix: "Using `executemany` sends one round trip instead of
  one per row; with 10k rows that's seconds vs minutes. Docs: <link>."
- Mark educational, non-blocking points: "FYI:", "Nit (learning):", "Optional:".
- Link to the team's style guide, ADRs, past incidents or internal docs so knowledge compounds.
- Show an example rather than describing it (a suggestion block or a short snippet).

## Pace the feedback
- A newcomer's first PRs: pick the **two or three most important** lessons per review; let minor
  nits go or fix them yourself in a follow-up. Forty comments teach nothing but discouragement.
- Recognise what they did well and specifically (see praise in review).
- Repeated patterns: one comment plus "applies elsewhere", or a short call to walk through it.

## Harder conversations
- Major design problems: talk first (call or in person), then summarise in the PR. Better still,
  review a design sketch before they write the code.
- Ask questions that lead to the insight ("what happens if two requests do this at once?") when
  there's time; give the answer directly when there isn't.

## Growing reviewers
- Pair-review: senior and junior review the same PR, compare notes.
- Let newer engineers be first reviewer with a senior as second; read their comments and give
  feedback on the review itself.
- Ownership/readability programmes (Google's readability) formalise this for language style.

## Mentor the other direction
Senior engineers' code benefits from junior reviewers asking "why?"; it exposes unclear code and
undocumented assumptions.
