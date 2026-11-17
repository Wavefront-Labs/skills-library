---
id: computing-software.software-engineering.code-review.giving-and-receiving-feedback
name: giving-and-receiving-feedback
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, feedback, nit, severity-labels, soft-skills, communication, blocking-comment, conventional-comments, review-culture, psychological-safety]
level: practitioner
status: draft
description: "Give code review comments that get acted on without defensiveness: severity labels, question framing, and distinguishing blocking issues from preference."
sources: ["Conventional Comments (conventionalcomments.org)", "Google's Engineering Practices - How to do a code review / review culture", "personal review experience leading a small team"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Giving and receiving review feedback — comments that change the code, not the mood

**Goal:** leave comments the author acts on quickly and without resentment, and
receive comments on your own code without treating them as a verdict on your worth.

## 1. Label severity explicitly
Unlabeled comments force the author to guess whether something blocks merge. Adopt a
convention (Conventional Comments is a good off-the-shelf one) and use it
consistently:
```
nit: this could be a one-liner (non-blocking, author's call)
suggestion: extract this into a helper — used 3x below
issue: this drops the error from the retry path, needs a fix before merge
question: why manual JSON parsing instead of the existing decoder?
praise: nice catch handling the empty-list case
```
A reviewer who marks everything the same severity (or marks nothing) is the most
common cause of review friction — the author can't tell "must fix" from "I'd have
done it differently."

## 2. Comment on the code, not the coder
"This function is confusing" invites defensiveness; "I had to read this three times
before I found where `total` gets reset — a comment or rename would help" states the
same observation as evidence plus an action. Never comment on intent ("you clearly
didn't think about...") — you cannot see intent, only the diff; assume competence and
missing context, not carelessness.

## 3. Ask, don't assert, when you're not sure
"Why not use the existing `RetryPolicy` here?" surfaces a real question (maybe there's
a reason) without presupposing the author is wrong. If you're confident it's a bug,
state it as `issue:` plainly — hedging a clear bug as a soft question ("have you
considered...?") wastes a review round-trip when the answer is just "yes, fix it."

## 4. Batch comments; don't drip-feed
Reviewing and submitting comments one at a time as you find them (if the tool allows
live posting) turns a 10-minute review into an hour of back-and-forth notifications.
Read the whole diff first, form an overall judgment, then submit comments together —
the author gets one coherent pass to respond to, not a slow trickle.

## 5. Pick your battles — not every preference is worth a comment
A nit worth raising changes behavior cheaply (a rename, a one-line extraction). A
style preference that's genuinely equivalent (tabs vs spaces the linter doesn't
enforce, which equally-valid pattern to use) costs review-cycle time for no quality
gain — if it's not in the style guide, it's not a blocking comment; either let it go
or raise it separately as a team style-guide proposal, not as resistance on this PR.

## 6. Receiving feedback without defensiveness
- Read the whole review before responding to any single comment — an early reaction
  to one comment, before seeing the rest, is usually the wrong reaction.
- Default response to a correct criticism: "good catch, fixing" — not a justification
  for why the bug happened. Explaining why is fine when asked; leading with it reads
  as excuse-making.
- If a comment feels personal, it is very often not intended that way — text strips
  tone; ask a clarifying question ("just to check, is this blocking or a nit?")
  instead of assuming hostility.
- Disagreeing with a comment is fine and expected sometimes — state your reasoning
  once, concretely, and if it's not resolved after one round, escalate to a quick
  call or a third opinion rather than a comment-thread war.

## Gotchas
- A reviewer who only ever leaves nits and never engages with correctness/design is
  providing low-value review — review for the thing that actually risks production
  (logic, error handling, data loss) before style.
- Praise comments are cheap and underused — a review that's 100% criticism, even
  justified criticism, trains authors to dread review instead of improving from it.
- "LGTM" with no comments on a large, risky diff is not actually a review — it's an
  unexamined approval; say so if you didn't have time to review it properly rather
  than rubber-stamping.

## Verify
- [ ] Every comment on a PR has a clear severity (blocking vs non-blocking), explicit
      or by convention the team has agreed on.
- [ ] No comment references the author's competence/intent rather than the code.
- [ ] A review that found zero issues on a non-trivial diff says what was actually
      checked, not just "LGTM."
- [ ] Disagreements that don't resolve in one comment round move to a synchronous
      conversation instead of a longer thread.

Related: computing-software.software-engineering.code-review.reviewing-a-diff
