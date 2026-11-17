---
id: computing-software.devops-ci-cd.github-actions.job-dependencies-outputs-and-conditionals
name: job-dependencies-outputs-and-conditionals
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, needs, needs-outputs, job-outputs, step-outputs, if-conditionals, always-condition, skipped-jobs, job-result, continue-on-error, fan-out-fan-in, gate-job, aggregate-job, dynamic-plan, plan-job, outputs-size-limit, outputs-empty, masked-outputs, matrix-outputs, timeout-minutes, job-ordering]
level: practitioner
status: verified
description: "Wire GitHub Actions jobs together: needs graphs, step-to-job outputs, the skipped-dependency trap, aggregate gate jobs for required checks, matrix output limits, masked outputs."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/passing-information-between-jobs", "https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idneeds", "https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idoutputs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job dependencies, outputs and conditionals

**Goal:** fan-out/fan-in pipelines whose jobs run in the right order, pass data cleanly,
and still produce a single green/red status for branch protection.

## 1. needs — the graph
```yaml
jobs:
  plan:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.v.outputs.version }}
      deploy:  ${{ steps.v.outputs.deploy }}
    steps:
      - id: v
        run: |
          echo "version=$(git describe --tags --always)" >> "$GITHUB_OUTPUT"
          echo "deploy=${{ github.ref == 'refs/heads/main' }}" >> "$GITHUB_OUTPUT"
  build:
    needs: plan
    runs-on: ubuntu-latest
    steps:
      - run: echo "building ${{ needs.plan.outputs.version }}"
  deploy:
    needs: [plan, build]
    if: needs.plan.outputs.deploy == 'true'
```
Jobs without `needs` start in parallel. A job needing a **failed or skipped** job is skipped
unless its `if` contains `always()`, `!cancelled()`, or `failure()`. Skipped propagates: one
`if: false` early job silently skips the whole downstream chain — the most common "why didn't
deploy run" cause.

## 2. Outputs — the rules that bite
- Step → job: `echo "name=value" >> "$GITHUB_OUTPUT"` in a step **with an `id`**, then map in
  `jobs.<id>.outputs`. Multiline: heredoc syntax
  `{ echo "body<<EOF"; cat notes.md; echo "EOF"; } >> "$GITHUB_OUTPUT"`.
- Outputs are strings; everything downstream is `'true'`, not `true`.
- Size limits: outputs can be at most 1 MB per job and 50 MB per workflow run (approximated in UTF-16);
  bigger → artifacts.
- **Secret-bearing outputs are dropped**: outputs containing secrets are redacted on the runner and not
  sent (the log warns "Skip output ... since it may contain secret"). Pass a reference, not the value, or
  re-fetch in the consumer.
- Outputs from a **matrix** job: if the legs use unique output names they are combined; if they write the
  same name, the last matrix job to run overrides it and the order is not guaranteed. Use unique names
  (for example `output_${{ matrix.version }}`), per-leg artifacts, or one combined output from an
  aggregator job.

## 3. Conditionals
- `if:` on a job is evaluated before the runner is assigned (no `env`, no `secrets`, no `steps`).
- To gate on a secret existing: `if: ${{ secrets.DEPLOY_KEY != '' }}` is **not allowed at job
  level** — do it in a prior job: output `has_key=${{ secrets.DEPLOY_KEY != '' }}` from a step env.
- `continue-on-error: true` on a step keeps the job green: `steps.x.outcome` keeps the real
  result, `steps.x.conclusion` becomes `success`. On a *matrix job* it means a failing leg does not
  fail the run or cancel the other legs.
- `jobs.<id>.timeout-minutes` defaults to **360**; set 10–30 on every job so a hung test does not burn six
  hours.

## 4. The aggregate gate job (required checks with matrices/conditionals)
Branch protection wants one named check that always reports. Pattern:
```yaml
  ci-ok:
    if: always()
    needs: [lint, test, build]
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo '${{ toJSON(needs) }}'
          [[ "${{ contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled') }}" == "false" ]]
```
Make `ci-ok` the only required check. `skipped` counts as OK here (path-filtered jobs); make
it fail on skipped too if a job must always run. Renamed matrix legs no longer break protection.

## 5. Dynamic fan-out
```yaml
  plan:
    outputs:
      matrix: ${{ steps.m.outputs.matrix }}
    steps:
      - id: m
        run: |
          echo "matrix=$(ls services | jq -R -s -c 'split("\n")[:-1] | {service: .}')" >> "$GITHUB_OUTPUT"
  build:
    needs: plan
    strategy: { matrix: "${{ fromJSON(needs.plan.outputs.matrix) }}" }
```
With no services the command prints `{"service":[]}` (jq 1.8.2); avoid an empty matrix by skipping the job
when the list is empty: `if: needs.plan.outputs.matrix != '{"service":[]}'`.

## 6. Sharing files, not strings
Anything beyond a few KB: `actions/upload-artifact` in the producer and `actions/download-artifact` in the
consumer (same workflow run; v4 of both exists, newer majors are out). Workspaces are **not** shared
between jobs: GitHub provisions a new virtual machine for each job.

## Verify
- [ ] A dependency marked `if: false` does not silently skip production deploy (gate uses `always()` + explicit result checks).
- [ ] No job output carries a secret-derived value (they arrive empty).
- [ ] Every job has `timeout-minutes`.
- [ ] Branch protection requires the aggregate job, not individual matrix legs.
