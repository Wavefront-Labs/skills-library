---
id: computing-software.qa-testing-engineering.test-automation.publishing-test-artifacts-in-ci
name: publishing-test-artifacts-in-ci
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-artifacts, ci, screenshots, playwright-trace, junit-xml, github-actions]
level: practitioner
status: docs-checked
description: "Publish test artifacts from CI: screenshots, videos, traces, logs and reports uploaded on failure with retention, naming per shard, and links in the job summary."
sources:
  - https://docs.github.com/en/actions/tutorials/store-and-share-data
  - https://docs.gitlab.com/ci/jobs/job_artifacts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing test artifacts in CI

**Goal:** every failed CI run carries the evidence needed to debug it without re-running locally.

## What to publish
- JUnit XML (always) for the CI test summary.
- An HTML report for browsing.
- On failure: screenshots, videos, traces, browser console logs, server and container logs, HAR files.

## GitHub Actions
```yaml
- run: <your test command>
- uses: actions/upload-artifact@v4
  if: <condition that also runs when the tests fail>
  with:
    name: test-report-${{ matrix.shardIndex }}
    path: |
      test-report/
      test-results/
    retention-days: 14
```
- Use an `if:` condition with a status check function so the upload step still runs after a failed test
  step; see the GitHub docs on status check functions.
- Artifacts are immutable in v4, so give each matrix shard a distinct `name`; without a name the default is
  `artifact`.
- `retention-days` sets a custom retention period and cannot exceed the limit set by the repository,
  organisation or enterprise.

## GitLab CI
```yaml
e2e:
  script: <your test command>
  artifacts:
    when: always
    expire_in: 2 weeks
    paths: [test-report/, test-results/]
    reports:
      junit: results/junit.xml
```
- By default artifacts upload only when the job succeeds; `artifacts:when: always` uploads regardless of
  status, `on_failure` only on failure.
- `expire_in` sets how long artifacts are kept (instance default applies if unset); artifacts from the most
  recent pipelines on a ref are kept regardless by default.
- `artifacts:exclude` skips files (not recursive), `artifacts:name` names the archive,
  `artifacts:expose_as` links artifacts in the merge request UI.
- Report artifacts (for example JUnit results) are not part of the archive downloaded by job name and branch;
  download them by job ID with `file_type`.

## Practice
- Configure the test runner to produce heavy artifacts (screenshots, video, traces) only when useful, for
  example on failure or on retry, to save storage; check your runner's docs for the option names.
- Mask secrets in logs before upload.
- Retention long enough to debug; longer for release builds if audit needs it.

## Verify
A deliberately failing test produces downloadable screenshot, trace and logs linked from the CI run, and
artifacts from parallel shards do not overwrite each other.

## Checked
2026-11-01. Confirmed: GitHub "store and share data" page (`upload-artifact`, v4 immutability, default name,
`retention-days` and its cap); GitLab job artifacts page (`when`, `expire_in`, `exclude`, `name`, `expose_as`,
`reports` and JUnit download behaviour, retention of recent pipelines). Removed: `!cancelled()` and
`failure()` expressions, `$GITHUB_STEP_SUMMARY`, Playwright option names and `show-trace`/trace.playwright.dev,
the `docker compose logs` command, specific report tools, and the 1-4 week retention figure, none of which
those pages state.
Method: documentation only; no commands were run.
