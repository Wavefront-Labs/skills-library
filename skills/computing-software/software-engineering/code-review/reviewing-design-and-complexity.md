---
id: computing-software.software-engineering.code-review.reviewing-design-and-complexity
name: reviewing-design-and-complexity
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, reviewing-a-diff, design-review, complexity-review, over-engineering, yagni, abstraction, eng-practices]
level: advanced
status: docs-checked
description: "Review the design of a change before its details: does it belong here, fit the architecture, stay as simple as the problem allows, and avoid speculative generality?"
sources: ["https://google.github.io/eng-practices/review/reviewer/looking-for.html", "https://google.github.io/eng-practices/review/reviewer/navigate.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing design and complexity

**Goal:** catch the expensive problems (wrong place, wrong abstraction, needless
complexity) first, before spending effort on line-level comments.

## Order of review (Google "Navigating a CL in review")
1. Take a broad view: read the description; does this change make sense at all? If it
   should not have happened, respond immediately with an explanation and, courteously,
   suggest what to do instead.
2. Examine the main part of the change first (the file with the most logical changes). If
   you see major design problems, send those comments immediately, even before reviewing
   the rest: the other code may disappear, and the author may already be building on it.
3. Then the rest in a sensible sequence; sometimes reading the tests first shows what the
   change is meant to do.
4. If you reject many changes, communicate earlier in your process; better to say no before
   a lot of work is done.

## Design questions
- Do the interactions of the pieces make sense?
- Does the change belong in this codebase, or in a library?
- Does it integrate well with the rest of the system?
- Is now a good time to add this functionality?

## Complexity questions
"Too complex" usually means it cannot be understood quickly by readers, or developers are
likely to introduce bugs when calling or modifying it. Check at every level: lines,
functions, classes.
- Over-engineering: code more generic than needed, or with functionality not needed now.
  Encourage the author to solve the problem they know about today; the future problem can
  be solved when it arrives and its real shape is visible.

## Giving design feedback
- Offer an alternative when rejecting the approach, and stay courteous.
- Pointing out the problem and letting the author decide often yields a better solution,
  since the author is closer to the code.

## Verify
- [ ] First comment on a large PR addresses direction/design, not formatting.
- [ ] Every abstraction introduced has a current, concrete reason in the PR.

## Checked

2026-11-08. Read in full: Google eng-practices "What to look for in a code review" (Design, Complexity) and "Navigating a CL in review". Confirmed: the design questions, the definition of too complex, the over-engineering guidance, and the three-step navigation order including immediate design comments and courteous rejection with an alternative. Removed: data-model and schema-cost claims, indirection and hidden-coupling lists, the call-site example and the design-doc advice, none of which these pages state.

Method: documentation only; no commands were run.
