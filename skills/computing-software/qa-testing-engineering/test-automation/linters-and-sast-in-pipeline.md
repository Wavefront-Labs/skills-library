---
id: computing-software.qa-testing-engineering.test-automation.linters-and-sast-in-pipeline
name: linters-and-sast-in-pipeline
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [static-analysis, linters, sast, semgrep, codeql, eslint, ruff, spotbugs, ci-pipeline]
level: practitioner
status: docs-checked
description: "Run linters and SAST (ESLint, Ruff, SpotBugs, Semgrep, CodeQL) in CI with baselines, severity gates and suppression rules so findings get fixed, not ignored."
sources:
  - https://semgrep.dev/docs/
  - https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql
  - https://docs.astral.sh/ruff/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linters and SAST in the pipeline

**Goal:** catch defect patterns before tests run, with a signal the team trusts.

## Typical stack
| Language | Lint | Bug patterns / SAST |
|---|---|---|
| JS/TS | ESLint | Semgrep, CodeQL |
| Python | Ruff | Semgrep, CodeQL |

## CI wiring
```yaml
# GitHub Actions
- run: npx eslint . --max-warnings=0
- run: ruff check --output-format=github .
- run: semgrep scan   # add a rule config; see the Semgrep CLI reference
```
CodeQL runs through GitHub code scanning (see the CodeQL code scanning page).
Upload SARIF so findings show inline on PRs.

## Making it stick
- **Baseline legacy findings** and gate only *new* findings (Semgrep `--baseline-commit`).
- Fail on high severity; warn on the rest; review warnings weekly.
- Suppressions require a reason, for example a `nosemgrep` comment naming the rule.
- Run lint in pre-commit for speed, full SAST in CI.

## Gotchas
- Turning on every rule produces noise and mass suppression. Start with recommended sets.
- SAST misses logic flaws and finds false positives; it complements testing, does not replace it.

## Verify
Introduce a known bad pattern in a test branch: the pipeline fails with the finding inline.

## Checked
2026-10-28. Confirmed: ESLint `--max-warnings` (CLI page); Ruff `output-format` setting (settings page); Semgrep `--baseline-commit`, SARIF output and `nosemgrep` comments (CLI reference and ignoring-code pages); CodeQL supported languages (GitHub code scanning page). Removed: the Java and SonarQube rows, `ruff --select S`, `--error` and `p/ci`, the CodeQL action steps, the ESLint and SpotBugs suppression syntax, and the exam-syllabus reference, none of which were in the fetched pages.
Method: documentation only; no commands were run.
