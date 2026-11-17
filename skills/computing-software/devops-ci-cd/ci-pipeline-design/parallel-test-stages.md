---
id: computing-software.devops-ci-cd.ci-pipeline-design.parallel-test-stages
name: parallel-test-stages
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, parallel-test-stages, test-parallelisation, deployment-pipeline]
level: practitioner
status: docs-checked
description: "Split test stages into parallel jobs by suite and shard, keep shared setup cached, aggregate results and coverage, and size parallelism against cost and queue time."
sources: ["https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations", "https://docs.gitlab.com/ci/yaml/#parallel"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel test stages

## Split dimensions
1. **By suite type**: unit, integration, contract, e2e as separate jobs, each with its own
   environment needs.
2. **By shard within a suite**: N workers each run 1/N of tests (timing-balanced where possible).
3. **By platform**: OS/runtime matrix only where behaviour differs.

## GitLab
```yaml
unit:
  parallel: 4
  script: ./run-tests.sh --shard $CI_NODE_INDEX/$CI_NODE_TOTAL   # your runner's sharding option
  artifacts: { reports: { junit: report.xml }, paths: [.coverage.*] }
```
## GitHub Actions
```yaml
strategy: { matrix: { shard: [1, 2, 3, 4] } }
steps:
  - run: ./run-tests.sh --shard ${{ matrix.shard }}/4   # your test runner's sharding option
```

## Aggregation
- JUnit reports from all shards (collect them with a fan-in job or your CI's report feature).
- Coverage: each shard writes partial data, a final job combines them with your coverage tool's merge command and enforces thresholds once.
- A single required "tests passed" gate job depending on all shards keeps branch protection simple.

## Sizing
- Setup cost per job (checkout, deps, DB) is paid N times; cache aggressively or parallelism stops paying.
- Diminishing returns past the point where the slowest single test file dominates; split that file.
- Watch queue time: many shards on a busy runner pool can be slower than fewer.

## Verify
- [ ] Wall-clock of the test stage drops roughly with N up to the chosen size; combined coverage equals the serial figure.

## Checked

2026-10-28. Confirmed: GitLab parallel keyword and the CI_NODE_INDEX / CI_NODE_TOTAL predefined variables (GitLab CI YAML reference); GitHub Actions matrix strategy (run job variations page). Removed: pytest-split and Playwright shard flags, merged-JUnit and coverage-merge command names, and the 20-versus-8 shard figures (not in the sources).

Method: documentation only; no commands were run.
