---
id: computing-software.qa-testing-engineering.test-automation.pull-request-test-failure-annotations
name: pull-request-test-failure-annotations
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [pr-test-annotations, ci, github-actions, junit-xml, check-runs, code-review]
level: practitioner
status: docs-checked
description: "Annotate pull requests with test failures: GitHub check annotations from JUnit XML, problem matchers, job summaries, GitLab MR test widgets and sticky comments."
sources:
  - https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
  - https://docs.gitlab.com/ee/ci/testing/unit_test_reports.html
  - https://github.com/dorny/test-reporter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Annotating pull requests with test failures

**Goal:** developers see which tests failed, where and why directly in the PR, without digging through raw logs.

## GitHub
- **Workflow commands:** any step can print `::error file=src/cart.test.ts,line=42,title=Cart total::expected 10 got 9`, which appears as an annotation on the diff and in the checks summary.
- **Built-in reporters:** Playwright's `github` reporter (`reporter: process.env.CI ? [['github'], ['html']] : 'list'`) emits annotations automatically; Jest has a `github-actions` reporter.
- **From JUnit XML:** actions such as `dorny/test-reporter` or `mikepenz/action-junit-report` create a check run with per-test results and failure annotations. They need `checks: write` permission; PRs from forks run with read-only tokens, so use the `workflow_run` pattern for those.
- **Job summary:** write Markdown to `$GITHUB_STEP_SUMMARY` (failed tests table, links to artifacts).
- Reporter actions cap how many annotations they create (for example `max-annotations` in `dorny/test-reporter`), so summarise and link to the full report.

## GitLab
- `artifacts:reports:junit: report.xml` shows a test summary widget in the merge request with new failures, fixed tests and links.
- Code quality and coverage reports also appear in the MR (`reports:codequality`, `coverage_report`).

## Sticky comment
For richer summaries (flaky tests, coverage delta, visual diffs), post or update a single PR comment via the API (e.g. `marocchino/sticky-pull-request-comment`) instead of a new comment per run.

## Verify
A failing test in a PR shows an annotation at the relevant file/line or in the check run with its error message, and the summary links to artifacts.

## Checked
2026-10-28. Confirmed: `::error file=...,line=...,title=...::message` workflow command and `$GITHUB_STEP_SUMMARY` (GitHub workflow commands page); Playwright and Jest GitHub reporters (their reporter docs); `checks: write` and `max-annotations` (dorny/test-reporter README); `mikepenz/action-junit-report` and its workflow_run/fork note; `artifacts:reports:junit`, `reports:codequality` and `coverage_report` (GitLab docs); `marocchino/sticky-pull-request-comment`. Removed: the Jest 28 version gate and the per-step and per-job annotation counts.
Method: documentation only; no commands were run.
