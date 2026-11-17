---
id: computing-software.software-engineering.code-review.what-to-look-for-in-code-review
name: what-to-look-for-in-code-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, what-to-look-for, review-checklist, design-review, functionality, complexity]
level: practitioner
status: docs-checked
description: "Know what to look for in a review per Google's guide: design, functionality, complexity, tests, naming, comments, style, consistency, documentation, every line, context."
sources:
  - https://raw.githubusercontent.com/google/eng-practices/master/review/reviewer/looking-for.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# What to look for in a code review

Google engineering practices, "What to look for":

| Area | Ask |
|---|---|
| **Design** | Do the pieces interact sensibly? Does this belong in this codebase? Is now the right time for it? |
| **Functionality** | Does it do what the author intended, and is that good for users (end users and developers who call it)? Edge cases, concurrency; for user-facing UI changes consider a demo. |
| **Complexity** | Could it be simpler? Can a reader understand it quickly? Over-engineering for speculative future needs? |
| **Tests** | Appropriate unit/integration/e2e tests in the same change; would they fail if the code broke; are they simple and maintainable? |
| **Naming** | Do names say what things are/do without being unwieldy? |
| **Comments** | Mainly explain *why*, not *what*; remove unneeded comments and stale TODOs. |
| **Style** | Follows the style guide; purely personal preferences marked "Nit:" and not blocking. Major style reformatting belongs in a separate change. |
| **Consistency** | The style guide is the authority where it has requirements; where it only recommends, use judgment, otherwise match surrounding code. |
| **Documentation** | If the change alters how users build, test, use or release code, READMEs and reference docs should be updated; request missing docs. |

## Every line
Read all human-written code closely enough to understand it; if it is too hard to follow, ask the developer to clarify. If you lack expertise in an area such as security or privacy, make sure another qualified reviewer is involved. When you review only part of a change, say which parts.

## Context
Look at the whole file and system, not just the diff: does the change improve or degrade code health, since small added complexities accumulate? Point out good practices too; encouragement is part of mentoring.

## Checked
2026-11-01. Confirmed against the google/eng-practices review/reviewer looking-for.md: each area above, every line, context, good things. Removed (not on that page): the importance ordering claim, the Navigating a CL section (page not read), demo-or-screenshot wording, changelog and tests-first advice.
Method: documentation only; no commands were run.
