---
id: computing-software.qa-testing-engineering.test-automation.gitlab-ci-test-jobs-and-junit-reports
name: gitlab-ci-test-jobs-and-junit-reports
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [gitlab-ci-tests, gitlab-ci, junit-xml, parallel-jobs, test-reporting, ci]
level: practitioner
status: docs-checked
description: "Configure GitLab CI test jobs: stages, services, caching, parallel:matrix and parallel splitting, JUnit report artifacts, coverage regex and rules for MR pipelines."
sources:
  - https://docs.gitlab.com/ee/ci/yaml/
  - https://docs.gitlab.com/ee/ci/testing/unit_test_reports.html
  - https://docs.gitlab.com/ee/ci/services/
  - https://docs.gitlab.com/ci/testing/code_coverage/
  - https://playwright.dev/docs/test-sharding
  - https://playwright.dev/docs/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab CI test jobs and JUnit reports

**Goal:** fast, parallel test jobs whose results show up in merge requests.

## Example `.gitlab-ci.yml`

```yaml
stages: [lint, test, e2e]

default:
  image: python:3.12

unit:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest tests/unit
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    when: always
    reports:
      junit: report.xml

integration:
  stage: test
  services:
    - name: postgres:16
      alias: db
  variables: { POSTGRES_PASSWORD: test, DATABASE_URL: "postgresql://postgres:test@db/postgres" }
  script: [pip install -r requirements.txt, pytest tests/integration]
  artifacts: { when: always, reports: { junit: report.xml } }

e2e:
  stage: e2e
  image: mcr.microsoft.com/playwright:v<PLAYWRIGHT_VERSION>-noble
  parallel: 4
  script: [npm ci, npx playwright test --shard=$CI_NODE_INDEX/$CI_NODE_TOTAL]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

## Notes
- Make your test command write the JUnit XML file (`report.xml` above) with your runner's own report option; the GitLab keywords are the same regardless of runner.
- Cache dependencies with `cache:` (keyed on the lockfile via `cache:key:files`); see GitLab's caching docs for the pip pattern.
- `parallel: N` sets `CI_NODE_INDEX`/`CI_NODE_TOTAL` for sharding; `parallel:matrix` runs version combinations.
- `artifacts:when: always` uploads other artifacts on failure too; files under `artifacts:reports` are uploaded regardless of job result. JUnit reports must be XML, each file under 30 MB, under 100 MB in total per job, and do not change job status: the script must exit non-zero for the job to fail.
- The `coverage` regex shows the percentage in the MR widget (last matching line wins). Line-by-line diff annotations need `artifacts:reports:coverage_report` (a Cobertura or JaCoCo XML report) configured separately; see the code coverage docs for setup.
- Pin the Playwright image tag to the installed `@playwright/test` version (tags are `v<version>-noble` or `-jammy`).
- `rules` decide MR vs branch pipelines; avoid duplicate pipelines with `workflow:rules`.
- `needs:` builds a DAG so e2e can start as soon as its dependency finishes rather than waiting for the whole stage.
- `retry: { max: 1, when: runner_system_failure }` retries infrastructure failures only, not test failures (`retry:max` can be 0, 1 or 2; with no `when`, every failure type retries). The reference marks `stuck_or_timeout_failure` as deprecated in GitLab 19.1 in favour of more specific reasons; check the retry:when list for your version.

## Verify
An MR shows the test summary widget with failures and coverage, shards each run a subset, and a failing test produces artifacts.

## Checked
2026-10-31. Confirmed on the GitLab CI YAML reference, Unit test reports, Services and Code coverage pages: `coverage` regex behaviour (last matching line wins), `artifacts:when`, `CI_NODE_INDEX`/`CI_NODE_TOTAL` for `parallel`, `parallel:matrix`, `retry:max` values, `retry:when` reasons and the `stuck_or_timeout_failure` deprecation in GitLab 19.1, service `alias`, the JUnit constraints (XML, under 30 MB per file, under 100 MB per job, no effect on job status), and the separate `coverage_report` keyword (Cobertura or JaCoCo XML input). Playwright `--shard=x/y`, `npm ci` and the `mcr.microsoft.com/playwright` tag form confirmed on its docs. Removed: the pytest `--junitxml` / `--cov` / `--cov-report=term` example flags and the `PIP_CACHE_DIR` pip-cache pattern (not in any page fetched this batch; see the pytest and pip docs for them), the Cobertura `coverage_report` config block (its yaml keys are on a page not fetched this batch), the old `v1.48.0` image pin, and `stuck_or_timeout_failure` from the retry example.
Method: documentation only; no commands were run.
