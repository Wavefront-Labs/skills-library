---
id: computing-software.devops-ci-cd.ci-pipeline-design.test-analytics-and-ci-visibility
name: test-analytics-and-ci-visibility
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, test-analytics, ci-visibility, flaky-tests]
level: practitioner
status: docs-checked
description: "Collect test results across runs: GitLab JUnit unit test reports in merge requests, and Datadog Test Optimization features (flaky tests, durations, owners, impact analysis)."
sources: ["https://docs.datadoghq.com/tests/", "https://docs.gitlab.com/ci/testing/unit_test_reports/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test analytics and CI visibility tools

Single-run reports answer "what failed now"; results gathered across runs answer "what is
flaky, slow, or getting worse".

## GitLab unit test reports
- Show results in merge requests and the pipeline Tests tab. They need JUnit XML (`.xml`
  extension, under 100 MB in total per job) and do not affect job status.
- Configure with `artifacts:reports:junit`: a single file, a pattern such as
  `test-results/**/*.xml`, an array, or a combination; directories are not supported. Add
  `artifacts:when: always` to upload reports even when the job fails, and `artifacts:paths` to
  make the files browsable.
```yaml
ruby:
  stage: test
  script:
    - bundle exec rspec --format progress --format RspecJunitFormatter --out rspec.xml
  artifacts:
    when: always
    paths:
      - rspec.xml
    reports:
      junit: rspec.xml
```
- A merge request compares its results with a baseline pipeline on the target branch:
  newly failed (passed on target, failed on source), existing failures, and resolved
  failures. Tests that failed on the default branch in the last 14 days show
  `Failed {n} time(s) in {default_branch} in the last 14 days`.

## Datadog Test Optimization
Part of Datadog CI/CD Optimization, which combines CI Visibility and Test Optimization. It
gives a test-first view of CI health, with language libraries (.NET, Java/JVM, JavaScript,
Python, Ruby, Swift, Go) and a JUnit XML route. Features listed on the page:
- durations at microsecond resolution; suite, module and session level visibility;
- codeowner by test (from the CODEOWNERS file) and CI and git metadata;
- automatic detection of benchmark and parameterised tests;
- opt-in features (enabled in CI/CD Optimization settings): Test Impact Analysis (skips
  tests using code coverage and git metadata), Early Flake Detection (retries new tests to
  detect flakiness), Auto Test Retries (retry failed tests up to N times) and Failed Test
  Replay.
- Each test configuration (OS, runtime and so on) is tracked as a separate test. A test that
  fails then passes on retry against the same commit is marked passed and flaky.

## Verify
- [ ] Every test job uploads JUnit XML even when it fails.
- [ ] Flaky tests are visible to the team and attributed to an owner.

## Checked
Confirmed 2026-11-09 against the GitLab unit test reports page (format limits, `artifacts:reports:junit` syntax, comparison categories, 14-day message) and the Datadog Test Optimization overview (feature list, configurations, opt-in marker), from local text copies. The JUnit upload sub-page of Datadog was not fetched.
Removed as unconfirmed: the `datadog-ci junit upload` command and `DD_API_KEY` snippet, per-language JUnit flags (pytest, jest-junit, gotestsum, surefire), the rows for BuildPulse, Trunk, Buildkite and Allure, self-hosted Postgres/BigQuery/Grafana advice, and the list of metrics to watch.
Method: docs-checked 2026-11-09 against docs.datadoghq.com/tests and docs.gitlab.com unit_test_reports
