---
id: computing-software.devops-ci-cd.ci-pipeline-design.coverage-thresholds-and-gates
name: coverage-thresholds-and-gates
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, coverage-thresholds, coverage-gate, code-coverage, diff-coverage, patch-coverage, ratchet, jacoco, coverage-py, istanbul, nyc, codecov, sonarqube-quality-gate, branch-coverage]
level: practitioner
status: docs-checked
description: "Gate CI on coverage without gaming: tool-native thresholds (coverage.py, Jest, JaCoCo), patch/diff coverage on PRs, ratchets, Codecov/Sonar gates, and merging shard reports first."
sources: ["https://coverage.readthedocs.io/en/latest/config.html", "https://jestjs.io/docs/configuration#coveragethreshold-object", "https://www.eclemma.org/jacoco/trunk/doc/check-mojo.html", "https://docs.codecov.com/docs/commit-status", "https://github.com/Bachmann1234/diff_cover"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coverage thresholds and gates

## Principle
Gate on **new/changed code** (patch coverage), and keep the **overall** number from
regressing. An absolute global target on a legacy codebase either
blocks everyone or gets lowered; on a new one it invites assertion-free tests.

## Tool-native thresholds (fail the test command)
```toml
# pyproject.toml - coverage.py
[tool.coverage.run]
branch = true
source = ["src"]
[tool.coverage.report]
fail_under = 78
skip_covered = true
exclude_also = ["raise NotImplementedError"]
```
```js
// jest.config.js
coverageThreshold: {
  global: { branches: 70, functions: 75, lines: 80, statements: 80 },
  './src/payments/': { lines: 90 }       // stricter for critical paths
}
```
```xml
<!-- Maven JaCoCo: jacoco:check bound to verify -->
<rule><element>BUNDLE</element><limits>
  <limit><counter>LINE</counter><value>COVEREDRATIO</value><minimum>0.75</minimum></limit>
  <limit><counter>BRANCH</counter><value>COVEREDRATIO</value><minimum>0.60</minimum></limit>
</limits></rule>
```

## Patch / diff coverage on PRs
- `diff-cover coverage.xml --compare-branch=origin/main --fail-under=80` (the base branch must be available locally).
- Codecov `codecov.yml`:
  ```yaml
  coverage:
    status:
      project: { default: { target: auto, threshold: 0% } }   # target auto = compare with the base commit
      patch:   { default: { target: 80% } }
  ```
- SonarQube quality gate: add a condition on coverage of new code (see the SonarQube quality gates page).

## Ratchet
Store the current number (or use `target: auto` against the base commit) and fail only
on decrease; bump `fail_under` upward in the same PR that raises coverage.

## Mechanics that cause false failures
- **Sharded tests**: merge reports before the gate (`coverage combine` for coverage.py; other tools have a merge
  step of their own). Gating each shard separately fails them all.
- Path mismatches between CI workspace and repo root (`[paths]` in the coverage.py config).
- Generated code, migrations, vendored files: omit them explicitly.
- Branch coverage off by default in coverage.py and many tools: turn it on; line coverage
  hides untested `else` paths.

## Keep it honest
Coverage proves execution, not verification. Pair high-value modules with mutation
testing (`computing-software.devops-ci-cd.ci-pipeline-design.mutation-testing-in-ci`) and
review tests for missing asserts.

## Checked
2026-11-01. Confirmed: coverage.py `branch` (default False), `fail_under`, `exclude_also`, `[paths]` and `coverage combine`; Jest
`coverageThreshold` object; JaCoCo check rule; diff-cover `--compare-branch` and `--fail-under`; Codecov project/patch
statuses and `target: auto`; sources listed. Removed: pytest-cov flag, `fetch-depth`, `nyc merge`, JaCoCo merge goal,
`after_n_builds`, Codecov `fixes:`, the 0.5 point threshold and the Sonar percentage (not confirmed).
Method: documentation only; no commands were run.

## Verify
Add an untested function in a PR: patch coverage status fails with the uncovered lines
listed; the global threshold still passes.
