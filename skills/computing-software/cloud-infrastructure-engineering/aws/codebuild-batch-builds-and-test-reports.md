---
id: computing-software.cloud-infrastructure-engineering.aws.codebuild-batch-builds-and-test-reports
name: codebuild-batch-builds-and-test-reports
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, codebuild, batch-builds, build-matrix, build-graph, build-list, build-fanout, test-reports, report-groups, junit, code-coverage, buildspec, ci]
level: practitioner
status: docs-checked
description: "Fan out CodeBuild with batch builds (build-list, build-matrix, build-graph, fanout) and publish JUnit/coverage results to report groups with trends and pipeline gating."
sources: ["https://docs.aws.amazon.com/codebuild/latest/userguide/batch-build.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/batch-build-buildspec.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/test-reporting.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/report-group-create.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/code-coverage-report.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/test-permissions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CodeBuild batch builds and test reports

**Goal:** a long test suite runs as parallel builds, multi-platform builds run from one buildspec,
and every run's test and coverage results are visible as reports with history instead of buried in logs.

## 1. Enable batch on the project
Batch builds use a separate batch service role (CodeBuild calls StartBuild, StopBuild and RetryBuild with it) and
restrictions. Do not reuse the build role: that would let a build start more builds and bypass the
batch limits on build count and compute types.
```bash
aws codebuild update-project --name app-ci \
  --build-batch-config 'serviceRole=arn:aws:iam::<ACCOUNT_ID>:role/codebuild-batch,combineArtifacts=false,restrictions={maximumBuildsAllowed=20,computeTypesAllowed=[BUILD_GENERAL1_MEDIUM]},timeoutInMins=60'
aws codebuild start-build-batch --project-name app-ci
```
`batchReportMode` is `REPORT_INDIVIDUAL_BUILDS` or `REPORT_AGGREGATED_BATCH`.

## 2. Batch types in buildspec
Types: build graph, build list, build matrix, build fanout. Settings `fast-fail` (batch level) and `ignore-failure` (per build or fanout) exist.
```yaml
version: 0.2
batch:
  fast-fail: false
  build-graph:                        # tasks with dependencies
    - identifier: build
    - identifier: unit
      depend-on: [build]
    - identifier: integration
      depend-on: [build]
      buildspec: buildspec-integration.yml
```
```yaml
batch:
  build-fanout:                       # split tests across parallel builds
    parallelism: 5
    ignore-failure: false
phases:
  build:
    commands:
      - codebuild-tests-run --test-command 'npx jest' --files-search "codebuild-glob-search '**/*.test.ts'" --sharding-strategy 'equal-distribution'
```
Fanout creates one build per shard, counted by `parallelism`. `build-list` is an explicit list of builds with per-build env/buildspec; `build-matrix` builds the combinations of the `dynamic` env values (image, variables). Take the exact field names from the batch buildspec reference.

## 3. Test reports
```yaml
reports:
  unit-tests:
    files: ["**/junit*.xml"]
    base-directory: reports
    file-format: JUNITXML
  coverage:
    files: [coverage/jacoco.xml]
    file-format: JACOCOXML
```
- The service role needs `codebuild:CreateReportGroup`, `CreateReport`, `UpdateReport`, `BatchPutTestCases`, and for coverage `BatchPutCodeCoverages`. Those last four are not public permissions (no CLI or SDK call).
- Pre-create report groups with `aws codebuild create-report-group` (JSON input with export config) when you need raw-file export to S3.
- Trends: `aws codebuild get-report-group-trend --report-group-arn <ARN> --trend-field PASS_RATE`. Trend fields: PASS_RATE, DURATION, TOTAL, LINE_COVERAGE, LINES_COVERED, LINES_MISSED, BRANCH_COVERAGE, BRANCHES_COVERED, BRANCHES_MISSED.
- Other supported `file-format` values are listed on the test-reporting and code-coverage pages; check them there.

## Gotchas
- Each batch child is a full build with its own start-up; fan out only when the suite is long enough to amortise it.
- `fast-fail: true` stops the batch on the first failure: good for PRs, bad when you want every failure.
- In CodePipeline, enable batch on the CodeBuild action; check the action reference for how artifacts from batch children are combined (`combineArtifacts` on the project).

## Verify
- [ ] `aws codebuild batch-get-build-batches --ids <ID>` shows all children `SUCCEEDED` and total wall time below the serial run.
- [ ] Report group lists the latest run with pass/fail counts.
- [ ] Coverage report shows line coverage per run.

## Checked
2026-10-28. Confirmed on the batch-build, batch-build-buildspec, test-permissions and code-coverage-report pages and the codebuild botocore model: batch role rationale, batch types, fast-fail / ignore-failure / parallelism / depend-on / codebuild-tests-run, JACOCOXML, permissions and their non-public status, trend field enum, `buildBatchConfig` members and `batchReportMode` enum. Removed as unconfirmed: BatchEnabled/CombineArtifacts pipeline details, the full list of test and coverage file formats, "report files collected after post_build even when build fails", zero-test-case-success claim, cache and billing remarks, matrix example values.
Method: documentation only; no commands were run.
