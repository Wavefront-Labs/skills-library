---
id: computing-software.software-engineering.code-review.reviewing-a-diff
name: reviewing-a-diff
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, pull-request, merge-request, pr-review, diff, reading-order, risk-based-review, pr-size, small-prs, stacked-prs, conventional-comments, nitpick, blocking, review-turnaround, codeowners, github, gitlab, gerrit, security-review, test-review, git-range-diff, approval, software-engineering]
level: practitioner
status: draft
description: "Review a pull request efficiently: read in a deliberate order, spend attention on risk, keep PRs small, label comments by severity, and turn reviews around within a working day."
sources: ["Google Engineering Practices - Code Review Developer Guide", "SmartBear / Cisco Systems code review study (Best Kept Secrets of Peer Code Review)", "Conventional Comments specification (conventionalcomments.org)", "Bacchelli and Bird, Expectations, Outcomes, and Challenges of Modern Code Review (ICSE 2013)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing a diff — find what matters, say it clearly, don't block for nothing

**Goal:** catch defects, design problems and risk before merge, while keeping the
author unblocked and the codebase healthier after every PR than before it.

## 1. Before reading code: context and size
- Read the description and linked issue: what problem, why this approach, how was it
  tested? If you can't tell, ask before reviewing line by line.
- Check CI is green; don't spend human attention on what linters and tests catch.
- Check size. Defect-finding effectiveness drops sharply past roughly 200–400 changed
  lines and after about 60–90 minutes of continuous review (the widely cited
  SmartBear/Cisco study; treat as rule of thumb). Ask for a split when a PR mixes
  refactor + feature, or exceeds ~400 lines of non-generated code. Stacked PRs
  (Graphite, `git-branchless`, Gerrit chains, `gh` stacks) make splitting cheap.

## 2. Reading order
1. **Tests first.** They state intended behaviour; missing tests for the new path is
   your first finding.
2. **Public interfaces:** API signatures, schemas, migrations, config, protobuf/OpenAPI
   files, feature flags. These are hardest to change later.
3. **Core logic** — the file where the real change is (often not the first in the
   alphabetical list). In GitHub, use the file tree; for large PRs review commit by
   commit if the author kept them clean.
4. **Call sites and wiring**, then generated files/lockfiles (skim for surprises:
   unexpected new dependencies, version jumps).
For re-reviews after a force-push, `git range-diff main old-head new-head` shows what
actually changed between revisions.

## 3. Where to spend attention (risk-first)
Ask, in roughly this order:
- **Correctness:** off-by-one, null/empty, error paths, retries, timezones, integer
  overflow, unit mismatches, concurrent access to shared state.
- **Security:** input validation, authZ on every new endpoint, injection (SQL, shell,
  template), secrets in code or logs, unsafe deserialisation, SSRF in URL fetches.
- **Data and migrations:** reversible? lock-heavy on large tables? backfills batched?
  backward compatible with the currently deployed version during rollout?
- **Operability:** logs/metrics for the new path, timeouts, feature flag, rollback plan.
- **Design:** right module? duplicates something existing? will the next change be easy?
- **Readability:** names, comments explaining *why*, dead code.
Style belongs to the formatter; if a style point isn't automated, it isn't worth a
blocking comment.

Pull the branch and run it when behaviour is non-trivial (`gh pr checkout <n>`);
reading alone misses UI and integration issues.

## 4. Writing comments
Use **Conventional Comments**-style labels so severity is unambiguous:
```
issue (blocking): this query runs inside the loop — N+1 against orders. Batch by id?
suggestion (non-blocking): extract the retry policy so payments can reuse it.
nitpick: `cnt` → `retry_count`.
question: is the 30 s timeout from the upstream SLA or a guess?
praise: nice property test for the rounding edge cases.
```
- Comment on the code, not the person ("this function" not "you").
- Explain the why and, where you can, propose a concrete alternative or patch
  (GitHub "suggested changes").
- Separate must-fix from preferences; approve with non-blocking comments rather than
  holding a PR hostage for nits.
- Large design disagreements: move to a call or a short design doc, then summarise
  the outcome in the PR.

## 5. Turnaround and process
- Respond within one working day (Google's guidance); the first response matters
  most, even if it's "will review this afternoon".
- Review in focused blocks of up to an hour; batch reviews between deep-work sessions.
- Approve when the change **improves overall code health**, even if not perfect.
- Use `CODEOWNERS` to route to the right reviewers; avoid adding five reviewers who
  each assume another will look properly.
- Authors: self-review the diff before requesting review; annotate tricky spots.

## Gotchas
- The riskiest change is often what's *missing*: a call site not updated, a test not
  added, a migration without a rollback, a config change not applied in every environment.
- Renames and moves hide edits; enable rename detection (`git diff -M`) and review moved
  blocks for modifications.
- "LGTM" on a 2,000-line PR is rubber-stamping; say you skimmed, or ask for a split.
- Approving with "fix the nits then merge" is fine only if you trust nobody will sneak
  in unrelated changes after approval — configure "dismiss stale approvals" if not.

## Verify
- [ ] You know what the PR is meant to do and how it was tested before commenting.
- [ ] You read tests and interface changes before implementation details.
- [ ] Each comment carries a label; blocking ones state the risk and a fix.
- [ ] Correctness, security, migrations and operability were explicitly considered.
- [ ] Oversized or mixed PRs were sent back for splitting instead of skimmed.
- [ ] First response went out within one working day.

Related: computing-software.software-engineering.refactoring.characterisation-tests-and-safe-refactoring
