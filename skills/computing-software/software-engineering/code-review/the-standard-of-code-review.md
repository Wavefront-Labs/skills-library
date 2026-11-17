---
id: computing-software.software-engineering.code-review.the-standard-of-code-review
name: the-standard-of-code-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, reviewing-a-diff, code-health, approval-standard, lgtm, perfectionism, mentoring, eng-practices]
level: practitioner
status: docs-checked
description: "Apply the senior standard for approving changes: approve once the change definitely improves overall code health, even if not perfect; distinguish blockers from nits."
sources:
  - https://raw.githubusercontent.com/google/eng-practices/master/review/reviewer/standard.md
  - https://raw.githubusercontent.com/google/eng-practices/master/review/reviewer/looking-for.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The standard of code review

**Goal:** a consistent bar for "approve": high enough that the codebase gets better over
time, low enough that developers can make progress.

## The rule (Google eng-practices)
"Reviewers should favor approving a CL once it is in a state where it definitely improves
the overall code health of the system being worked on, even if the CL isn't perfect."
- Perfection is not required; reviewers can still deny approval for other reasons, such as an unwanted feature.
- Nothing justifies submitting a change that definitely worsens code health, except in an emergency.

## Blocking vs non-blocking
- Prefix minor, optional points with "Nit: " so the author knows they could ignore them.
- Purely educational comments should be marked as not required for this change.
- Do not block on personal preference; the style guide is the authority on style.

## Principles for judgement calls
- Technical facts and data overrule opinions and personal preferences.
- The style guide is the absolute authority on style; anything not in it is personal preference, and with no prior style the author's choice is accepted.
- Design decisions rest on engineering principles, not opinion; if the author shows several approaches are equally valid, the author's preference wins.
- If no rule applies, you may ask for consistency with the existing codebase, provided that does not worsen code health.

## Resolving conflicts
1. Try to reach consensus first.
2. If that stalls, meet face to face or by video and record the outcome as a comment on the change.
3. If still unresolved, escalate to a broader team discussion, a technical lead, the code's maintainer or an engineering manager.
4. Do not let a change sit because author and reviewer cannot agree.

## Verify
- [ ] Every blocking comment is tied to code health or the style guide.
- [ ] Preference-only comments are labelled "Nit:".

## Checked
2026-11-01. Confirmed against the google/eng-practices review/reviewer standard.md: approval standard, emergency exception, Nit prefix, educational comments, principles, conflict resolution steps. Removed (not on that page): the blocking-severity table, Optional:/FYI: labels, approve-with-comments advice.
Method: documentation only; no commands were run.
