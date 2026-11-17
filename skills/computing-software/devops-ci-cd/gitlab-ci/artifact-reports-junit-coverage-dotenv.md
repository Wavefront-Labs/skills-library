---
id: computing-software.devops-ci-cd.gitlab-ci.artifact-reports-junit-coverage-dotenv
name: artifact-reports-junit-coverage-dotenv
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, artifacts-reports, junit-report, coverage-report, cobertura, jacoco, coverage-keyword, dotenv-report, codequality-report, test-visualization, mr-widget, unit-test-reports, artifacts-expire-in, artifacts-when, artifacts-exclude, artifacts-untracked, artifacts-expose-as, dotenv-artifacts]
level: practitioner
status: docs-checked
description: "Surface GitLab CI results in merge requests: artifacts:reports for junit, coverage (cobertura/jacoco), dotenv and codequality; JUnit limits, screenshots, expiry."
sources: ["https://docs.gitlab.com/ci/yaml/artifacts_reports/", "https://docs.gitlab.com/ci/testing/unit_test_reports/", "https://docs.gitlab.com/ci/testing/code_quality/", "https://docs.gitlab.com/ci/yaml/#artifacts"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Artifact reports: junit, coverage, dotenv and friends

**Goal:** failing tests, coverage deltas and lint findings appear **in the merge request**,
not buried in a job log.

## 1. The report keys
```yaml
test:
  script:
    - run-tests --junit report.xml --coverage coverage.xml     # your tool's flags
  coverage: '/TOTAL.*\s+(\d+%)$/'     # regex over the job log; sets the job's coverage number
  artifacts:
    expire_in: 1 week
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura    # or jacoco
        path: coverage.xml
    paths: [htmlcov/]                 # list files here too if people must download them
```
| report | what it does |
|---|---|
| `junit` | unit test report: merge request comparison of source branch against a baseline on the target branch, pipeline Tests view |
| `coverage_report` (cobertura or jacoco) | line-by-line coverage annotations in the MR diff |
| `dotenv` | collects variables from a file and makes them CI/CD variables for later jobs |
| `codequality` | findings in the MR Reports tab, compared against a baseline pipeline on the target branch |

Artifacts created for `artifacts:reports` are **always uploaded, whether the job succeeds
or fails**; `artifacts:when` does not change that. Use `artifacts:when: always` only for the
files you list under `paths:`.

## 2. JUnit specifics
- `junit:` takes a filename, a glob (`rspec-*.xml`, `test-results/**/*.xml`), an array, or a
  mix. Directories are not supported.
- Each JUnit file must be under 30 MB and all JUnit files of a job under 100 MB total.
- Screenshots: a test case's `<system-out>` contains `[[ATTACHMENT|screenshots/failure.png]]`
  and the job uploads the directory in `artifacts:paths` (use `artifacts:when: always` so
  screenshots upload on failure).

## 3. Coverage
- `coverage:` is a regex run over the job log.
- `coverage_report` (cobertura or jacoco) gives the diff annotations; `path:` points at the
  XML file.

## 4. Code quality
Produce a Code Climate JSON report and set `reports: codequality: <file>`. Each finding has a
`fingerprint` (a unique string such as a hash of its contents); findings with identical
fingerprints display as one entry, and new or resolved findings are determined by comparing with
the baseline pipeline on the target branch. The built-in Code Quality template is marked
deprecated in the docs: check the Code Quality page for the current approach.

## 5. Artifact mechanics
- `expire_in` accepts forms such as `42 seconds`, `3 mins 4 sec`, `2h20min`, `6 mos 1 day`,
  `3 weeks and 2 days`, or `never`; with no unit the value is seconds. Unset, it defaults to
  the instance-wide setting. It does not affect the latest job's artifacts unless keeping them
  is disabled for the project or instance. Expired artifacts are deleted hourly by default.
  Selecting Keep on the job page also protects them.
- Too short an expiry makes later jobs fail with `could not retrieve the needed artifacts`.
- `artifacts:exclude` paths are not searched recursively. `artifacts:untracked: true` adds
  git-untracked files and ignores `.gitignore`. `artifacts:name` names the archive (default
  `artifacts.zip`).
- `artifacts:expose_as` shows artifacts in the MR UI: once per job, maximum 10 jobs per MR.
- `needs:artifacts` controls whether a `needs` job downloads artifacts.

## Verify
- [ ] A deliberately failing test shows in the MR as a new failure with the message.
- [ ] Changed lines show coverage annotations in the MR diff.
- [ ] Job page shows the coverage percentage.

## Checked
2026-10-31. Confirmed on the artifacts:reports page (junit, dotenv, coverage_report, formats),
the Unit test reports page (30 MB and 100 MB limits, ATTACHMENT screenshots), the Code Quality page
(fingerprint, baseline comparison, deprecated template) and the CI/CD YAML reference (expire_in
forms and defaults, exclude, untracked, name, expose_as limits, reports always uploaded).
Corrected: reports upload on failure without `when: always`. Removed as unconfirmed: terraform, metrics
and annotations rows, test-runner flags, coverage regex samples, badge URL, 10 MB coverage
limit, Coverage-Check rule, path-rewriting advice, linter flags, artifact download API path.
Method: documentation only; no commands were run.
