---
id: computing-software.software-engineering.code-review.handling-review-pushback
name: handling-review-pushback
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, review-comments, feedback, handling-pushback, review-disagreement, escalation, code-health, eng-practices]
level: practitioner
status: docs-checked
description: "Handle disagreement in code review: evaluate the author's argument on merit, hold the line on code health, avoid 'clean it up later', and escalate constructively."
sources: ["https://google.github.io/eng-practices/review/reviewer/pushback.html", "https://google.github.io/eng-practices/review/reviewer/standard.html", "https://google.github.io/eng-practices/review/reviewer/comments.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling pushback in code review

**Goal:** resolve disagreements quickly and on technical merit, without either rubber-
stamping or blocking indefinitely.

## When the author disagrees with your comment
1. **Consider that they may be right.** Authors are often closer to the code. If their
   argument shows the change improves code health and your concern doesn't apply, say so
   and drop the comment.
2. If you still believe you're right, **explain further**: show you understood their
   reply and add information about why the change is requested. Keep advocating when you
   believe the code-health gain justifies the extra work; sometimes it takes a few rounds,
   so stay polite and say you hear them but disagree.
3. Keep it about the code, not the developer.

## "I'll clean it up later"
Google's guidance: experience shows that "later" usually doesn't happen, not out of bad
intent but because other work arrives. Unless the change is an emergency, insist on the
cleanup now if it's about complexity introduced by this change. If deferral is truly
justified, require a filed bug assigned to the author and a TODO referencing it in code.

## Upset authors
Upsets are usually more about the way comments are written than about the reviewer
insisting on quality, and are often brief. Be polite, explain reasoning, and label
non-mandatory points ("Nit:", "Optional:", "Consider:", "FYI:"). If you move from lax to
strict reviews, complaints fade over time, and improving review speed helps.

## Breaking a deadlock
1. First try to reach consensus on the basis of the Standard of Code Review. If that is
   hard, a face-to-face meeting or video call can help; record the result as a comment on
   the change for future readers.
2. Technical facts and data overrule opinion; the style guide is the authority on style;
   design is weighed on principles, not personal preference.
3. Otherwise escalate: a broader team discussion, a Technical Lead, a maintainer of the
   code, or an Eng Manager. Do not let the change sit because the two of you disagree.

## Self-check as reviewer
- Is this a principle (correctness, design, maintainability) or my preference? A purely
  educational or polish point gets "Nit:" so the author may ignore it.
- Would the change definitely improve code health even if not perfect? Then favour approving.

## Verify
- [ ] Each disagreement ends with a written resolution in the thread.
- [ ] Deferred cleanups have a bug id referenced in the code.

## Checked

2026-11-08. Read in full: Google eng-practices "Handling pushback in code reviews", "The Standard of Code Review" and "How to write code review comments". Confirmed: author may be right; keep explaining politely; "clean it up later" rarely happens and new complexity is cleaned up before submission unless an emergency; otherwise file and self-assign a bug with an optional TODO referencing it; upsets mostly about comment wording; escalation path and recording the outcome. Removed: the 10-minute call figure, benchmark/test arbiter examples and the invented "approve with comments" self-check.

Method: documentation only; no commands were run.
