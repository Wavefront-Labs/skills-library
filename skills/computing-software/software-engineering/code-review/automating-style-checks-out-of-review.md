---
id: computing-software.software-engineering.code-review.automating-style-checks-out-of-review
name: automating-style-checks-out-of-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, review-process, review-automation, linters, formatters, danger-js, pre-commit-hooks]
level: practitioner
status: draft
description: "Remove style and mechanical checks from human review: formatters, linters, required CI checks, review bots (Danger, reviewdog), CODEOWNERS and PR templates."
sources:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://danger.systems/js/
  - https://github.com/reviewdog/reviewdog
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automating style checks out of review

Humans should review design, correctness, and readability. Anything a machine can check should be checked by a machine before a reviewer looks.

## Layers
1. **Formatters** (no debate, auto-fix): Prettier, Black/Ruff format, gofmt/goimports, rustfmt, clang-format, dotnet format, ktlint/spotless. Run on save and in pre-commit; CI fails on diff (`prettier --check`, `ruff format --check`, `gofmt -l`).
2. **Linters** for bug patterns and conventions: ESLint, Ruff, golangci-lint, Clippy, Checkstyle/SpotBugs/Error Prone, Roslyn analyzers, ShellCheck, hadolint, markdownlint.
3. **Type checks and tests** as required status checks.
4. **Security and dependency scans:** CodeQL/Semgrep, secret scanning with push protection, Dependabot/Renovate, licence checks.
5. **Review bots** for repo-specific rules.

## Make them blocking, fast, and local
- Branch protection / rulesets: required status checks, up-to-date branch, required reviews.
- Same config locally and in CI: `pre-commit` framework (`.pre-commit-config.yaml`), lefthook, husky + lint-staged. Pre-commit hooks are a convenience; CI is the enforcement.
- Keep the required checks under ~10 minutes; slow checks get bypassed.
- Introduce a new rule on an existing codebase with a baseline (ESLint `--max-warnings` ratchet, detekt/PHPStan baselines, Ruff `--add-noqa` once) so only new code must comply.

## Bots that comment on PRs
- **reviewdog:** posts linter output as inline PR comments only on changed lines (`reviewdog -reporter=github-pr-review -filter-mode=added`).
- **Danger (JS/Ruby/Kotlin/Swift):** codified review rules in `dangerfile`:
```javascript
import { danger, warn, fail } from "danger";
const big = danger.github.pr.additions + danger.github.pr.deletions > 600;
if (big) warn("Large PR: consider splitting for faster review.");
const appChanged = danger.git.modified_files.some(f => f.startsWith("src/"));
const testsChanged = danger.git.modified_files.some(f => f.includes("test"));
if (appChanged && !testsChanged) warn("Source changed without tests.");
if (danger.git.modified_files.includes("package.json") && !danger.git.modified_files.includes("package-lock.json"))
  fail("package.json changed but lockfile did not.");
```
- Labelers (size labels), changelog/semantic PR title checks (`amannn/action-semantic-pull-request`), migration reviewers via CODEOWNERS.

## Routing and context
- `CODEOWNERS` assigns the right reviewers automatically; combine with "require review from code owners".
- PR templates prompt for description, testing done, screenshots, rollout plan.

## What reviewers then stop commenting on
Formatting, import order, naming conventions the linter enforces, missing semicolons. If a style comment recurs in reviews, turn it into a lint rule instead.

## Verify
- [ ] A PR with misformatted code fails CI before any human review.
- [ ] Review comment sample shows few or no style nits after rollout.
