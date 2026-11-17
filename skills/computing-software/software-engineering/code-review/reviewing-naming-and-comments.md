---
id: computing-software.software-engineering.code-review.reviewing-naming-and-comments
name: reviewing-naming-and-comments
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, naming-review, code-comments, readability, documentation-comments]
level: practitioner
status: draft
description: "Review naming and comments: names that reveal intent at the right length, comments that explain why rather than what, stale or misleading comments, TODOs and doc comments."
sources: ["https://google.github.io/eng-practices/review/reviewer/looking-for.html#naming", "https://google.github.io/eng-practices/review/reviewer/looking-for.html#comments", "https://abseil.io/tips/", "https://testing.googleblog.com/2017/07/code-health-to-comment-or-not-to-comment.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing naming and comments

## Naming checks
- Does the name tell a reader what it is or does **without reading the implementation**?
  (`retry_delay_ms` vs `d`; `fetch_active_customers()` vs `get_data()`).
- Length proportional to scope: tiny loop variables short, public APIs descriptive.
- Consistent with existing vocabulary (domain terms; don't introduce `client` where the codebase
  says `customer`).
- Booleans as predicates (`is_enabled`, `has_children`); functions as verbs; classes as nouns.
  Avoid vague suffixes (`Manager`, `Helper`, `Data`, `Info`, `Util`).
- Units and kinds in names where types don't carry them (`timeout_seconds`, `price_cents`).
- Misleading names are worse than vague ones: `get_user()` that creates one, `is_valid` that also
  saves.
- Comment pattern: "Nit: `items` holds order ids, not items; `order_ids`?" Suggest a concrete
  alternative.

## Comment checks
- **Why, not what** (Google): code says what it does; comments explain why it does it this way,
  constraints, links to bugs/specs, non-obvious consequences.
  - Remove: `i += 1  # increment i`.
  - Keep/ask for: `# Stripe retries webhooks for 3 days; dedupe on event id, not payload hash.`
- If a comment is needed to explain **what** the code does, ask whether the code can be simpler or
  better named instead (extract a function whose name is the comment).
- **Stale comments**: did the change alter behaviour described by a nearby comment or docstring?
  Reviewers catch these far more often than tools do.
- Doc comments on public APIs: parameters, return, errors, thread-safety, units, examples.
- `TODO`s: have an owner or ticket (`TODO(#1234): ...`); no TODOs for things the change should do.
- Commented-out code: delete it (version control remembers).
- Regular expressions, bit twiddling, workarounds for library bugs: should have explanatory comments.

## Tone
Naming is subjective; label preferences as "Nit:" or "Optional:", and don't block on them unless the
name is actively misleading.
