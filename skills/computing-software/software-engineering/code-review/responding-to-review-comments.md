---
id: computing-software.software-engineering.code-review.responding-to-review-comments
name: responding-to-review-comments
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, pr-author, change-author, responding-to-review, review-iterations, fixup-commits, resolving-threads, eng-practices]
level: practitioner
status: docs-checked
description: "Respond to code review as an author: don't take it personally, fix the code rather than explain in comments, reply to every thread, and make re-review easy."
sources: ["https://google.github.io/eng-practices/review/developer/handling-comments.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to review comments

**Goal:** turn review feedback into a better change in as few round trips as possible.

## Mindset
- The review is about maintaining the quality of the codebase, not a personal attack. If
  a comment reads harsh, ask what constructive point the reviewer is making and act as if
  that is what they said.
- Never respond in anger. If too annoyed to be kind, step away until calm.
- If a reviewer is not constructive or polite, tell them in person or on a video call, or
  by private email, kindly saying what you would like changed; escalate to your manager
  as appropriate if that does not work.

## Fix the code, not just the reviewer's understanding
If a reviewer didn't understand something, future readers won't either. First clarify the
CODE itself; if it cannot be clarified, add a code comment explaining why it is there; only
if a comment seems pointless answer in the review tool. A reply in the review tool does not
help future readers.

## Disagreeing
- First ask yourself whether you understand what the reviewer is asking; if not, ask for
  clarification.
- If you understand but disagree, be collaborative, not combative: explain the trade-offs
  behind your choice and ask whether the reviewer is suggesting the trade-offs be weighed
  differently ("No, I'm not going to do that" is the bad example).
- You may know things about users, the codebase or the change that the reviewer does not:
  fix the code where appropriate and give them the context.
- Try to reach consensus first; if you cannot, fall back on the Standard of Code Review.

## Verify
- [ ] Every reviewer question was answered, ideally by making the code or its comments clearer.
- [ ] Disagreements are answered with reasons, not ignored.

## Checked

2026-11-08. Read in full: Google eng-practices "How to handle reviewer comments". Confirmed: do not take it personally, never respond in anger, raise unconstructive tone in person or privately then escalate to a manager, fix the code before explaining in the tool, collaborative disagreement example, and consensus before the Standard of Code Review. Removed: git commit --fixup, rebase and force-push remarks, the one business day ping, the GitHub comment-page source and the template reply wording, none of which the Google page states.

Method: documentation only; no commands were run.
