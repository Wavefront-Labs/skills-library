---
id: computing-software.software-engineering.code-review.self-review-before-requesting-review
name: self-review-before-requesting-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, pr-author, change-author, self-review, pre-review-checklist, draft-pr, diff-review]
level: practitioner
status: docs-checked
description: "Review your own change before asking others: read the diff as a reviewer, remove debris, check tests and edge cases, and annotate tricky parts, using a short checklist."
sources: ["https://google.github.io/eng-practices/review/reviewer/looking-for.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-review before requesting review

**Goal:** reviewers spend their time on design and correctness, not on problems you could
have caught yourself. Read your change the way Google's reviewer guide says a reviewer will.

## Checklist (from "What to look for in a code review")
**Design**
- [ ] Do the pieces interact sensibly? Does the change belong in this codebase, or in a library?
- [ ] Does it fit the rest of the system, and is now a good time to add it?

**Functionality**
- [ ] Does it do what you intended, and is that good for its users (end users and future developers)?
- [ ] Edge cases, concurrency problems (deadlocks, race conditions), and bugs visible just by reading.
- [ ] For user-facing changes, be ready to demo them; the reviewer may ask.

**Complexity**
- [ ] Lines, functions and classes are understandable quickly.
- [ ] Nothing is more generic than needed and nothing is built for a need you only speculate about.

**Tests**
- [ ] Appropriate unit, integration or end-to-end tests are in the same change as the production code (unless it is an emergency).
- [ ] Tests would fail when the code is broken, make simple useful assertions and are separated sensibly. Tests are code too; do not accept complexity in them.

**Naming and comments**
- [ ] Names are long enough to say what the thing is or does, without being hard to read.
- [ ] Comments are clear, necessary and explain why rather than what (except for things like regexes and complex algorithms). Stale TODOs and comments from before your change are removed or updated.

**Style and consistency**
- [ ] Follows the language style guide; major style changes (reformatting a whole file) go in a separate change.

**Documentation**
- [ ] If the change alters how users build, test, interact with or release the code, the READMEs and reference docs are updated; deleted or deprecated code has its docs removed.

## Read the whole diff
Reviewers are told to look at every human-written line and at the surrounding context of the
change, so read your own diff the same way, including the file around each hunk.

## Checked

2026-11-08. Read in full: Google eng-practices "What to look for in a code review". The checklist restates its Design, Functionality, Complexity, Tests, Naming, Comments, Style, Consistency, Documentation, Every Line and Context sections. Removed: the git diff command, the 400-line size figure, the draft-PR advice, secrets and migration checks and the CI advice, none of which the page states, and the developer guide landing page source.

Method: documentation only; no commands were run.
