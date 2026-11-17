---
id: computing-software.qa-testing-engineering.test-automation.github-actions-test-matrix
name: github-actions-test-matrix
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [github-actions-matrix, ci-matrix, matrix-strategy, cross-version-testing]
level: practitioner
status: docs-checked
description: "Run tests across versions, OSes and shards with GitHub Actions matrix strategy: include/exclude, fail-fast, max-parallel, dynamic matrices and aggregating results."
sources:
  - https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations
  - https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
  - https://docs.github.com/en/actions/reference/workflows-and-actions/contexts
  - https://playwright.dev/docs/test-sharding
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test matrix jobs in GitHub Actions

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false              # let all combinations finish (default true cancels others)
      max-parallel: 8
      matrix:
        os: [ubuntu-24.04, windows-2022, macos-14]
        python: ["3.10", "3.12", "3.13"]
        exclude:
          - { os: macos-14, python: "3.10" }
        include:
          - { os: ubuntu-24.04, python: "3.13", coverage: true }   # extra key on one combo
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python }}", cache: pip }
      - run: pip install -e .[test]
      - run: pytest --junit-xml=results-${{ matrix.os }}-${{ matrix.python }}.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: results-${{ matrix.os }}-${{ matrix.python }}, path: results-*.xml }
```

## Sharding with a matrix
```yaml
matrix: { shard: [1, 2, 3, 4] }
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4
```

## Dynamic matrix
```yaml
setup:
  outputs: { matrix: ${{ steps.m.outputs.matrix }} }
  steps:
    - id: m
      run: echo "matrix=$(python ci/changed_packages.py)" >> "$GITHUB_OUTPUT"   # JSON like {"pkg":["a","b"]}
test:
  needs: setup
  strategy: { matrix: ${{ fromJSON(needs.setup.outputs.matrix) }} }
```

## Required checks
Branch protection needs stable job names, and each matrix combination is its own check. Add a final
aggregator job (`needs: test`, `if: always()`, fail if `needs.test.result != 'success'`) and
require only that one.

## Gotchas
- A matrix generates at most 256 jobs per workflow run, on hosted and self-hosted runners.
- An `include` entry is added to every original combination it does not overwrite; if it cannot be
  added to any combination, it creates a new one.
- `strategy.fail-fast` applies to the whole matrix (default true); `continue-on-error` applies to a
  single job, so an experimental combination can fail without cancelling the others.

## Verify
Workflow summary shows each combination; the aggregator job fails when any required combo fails.

## Checked
2026-10-31. Confirmed in the GitHub Actions workflow syntax and matrix pages: `fail-fast`
(default true), `max-parallel`, 256-job limit, `include`/`exclude` semantics, `continue-on-error`,
`fromJSON` dynamic matrices, `$GITHUB_OUTPUT`, runner labels `ubuntu-24.04`, `windows-2022` and
`macos-14`, `always()` and `needs.<job_id>.result`; the setup-python README (`python-version`,
`cache: pip`); the pytest docs (`--junit-xml`); and the Playwright sharding page (`--shard`).
Corrected: pytest flag is `--junit-xml`. Removed: the `3.14-dev` experimental job and
`allow-prereleases`, the exact matrix job-name string, and the runner-cost remark, because no
fetched page confirms them.
Method: documentation only; no commands were run.
