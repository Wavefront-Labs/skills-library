---
id: computing-software.software-engineering.code-review.reviewing-large-or-generated-changes
name: reviewing-large-or-generated-changes
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, large-pr-review, generated-code, mechanical-changes, review-strategy, lockfiles]
level: practitioner
status: draft
description: "Review large or generated changes efficiently: ask to split, separate mechanical from logical edits, review generators not output, and verify bulk diffs with tooling."
sources: ["https://google.github.io/eng-practices/review/developer/small-cls.html", "https://google.github.io/eng-practices/review/reviewer/navigate.html", "https://docs.github.com/en/repositories/working-with-files/managing-files/customizing-how-changed-files-appear-on-github"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing large or generated changes

## First: should it be this big?
Large reviews get rubber-stamped; defect detection drops sharply beyond a few hundred lines
(SmartBear/Cisco study: 200-400 LOC per hour, under 400 LOC per review). If a change mixes concerns,
ask to split it (refactoring vs behaviour, by layer, by feature). Google: reviewers may reject a
change for being too large.

## When it legitimately has to be big
- **Mechanical changes** (rename, codemod, dependency bump, formatting): ask for the **command or
  script** that produced it in the description. Review the script, spot-check output, and re-run it
  yourself if feasible (`git diff` after running should be empty).
- **Commit structure**: ask the author to split into commits ("1. move files (no edits) 2. rename
  3. logic change") and review commit by commit. Moves without edits let git detect renames.
- **Generated code** (protobuf stubs, OpenAPI clients, ORM migrations, snapshots, lockfiles):
  review the **source** (`.proto`, schema, config) and the generator version; skim output for
  surprises (huge unexpected diff = wrong generator version). Mark generated files so the UI
  collapses them: `.gitattributes` `gen/** linguist-generated=true` (GitHub), `gitlab-generated`
  for GitLab.
- **Lockfiles**: check new/removed packages and major version jumps, not every hash.
- **New subsystem**: review design doc first; then review in multiple sessions with a written plan
  (entry points, data model, error paths, tests).

## Techniques
- Check out locally and use an IDE (code navigation, run tests, "find usages").
- `git diff --stat`, `git diff -w` (ignore whitespace), `--color-moved=zebra` to see moved code,
  `difftastic` for structural diffs.
- Ask for a walkthrough call for very large changes; record conclusions in the PR.
- State your coverage: "Reviewed packages api/ and db/; did not review ui/."

## AI-generated code
Treat it like code from a new contributor: the author must understand and vouch for every line;
look harder at plausible-but-wrong API usage, invented functions/flags, missing error handling and
tests that assert the implementation.
