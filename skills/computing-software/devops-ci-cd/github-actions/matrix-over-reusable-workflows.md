---
id: computing-software.devops-ci-cd.github-actions.matrix-over-reusable-workflows
name: matrix-over-reusable-workflows
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, matrix-reusable-workflow, reusable-workflows, workflow-call, matrix-uses, per-service-pipeline, fan-out-reusable, matrix-with-inputs, nested-jobs-naming, reusable-workflow-outputs-matrix, secrets-inherit, monorepo-services, dynamic-matrix, matrix]
level: practitioner
status: verified
description: "Call a reusable workflow once per matrix leg (service, region, env) with uses + with from matrix values; naming, output collection, limits and the dynamic-matrix feed from a plan job."
sources: ["https://docs.github.com/en/actions/sharing-automations/reusing-workflows#using-a-matrix-strategy-with-a-reusable-workflow", "https://docs.github.com/en/actions/sharing-automations/reusing-workflows#limitations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matrix over reusable workflows

**Goal:** one `deploy.yml` reusable workflow, invoked N times in parallel — once per
service or region — from a matrix.

## 1. Caller
```yaml
jobs:
  plan:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.s.outputs.list }}
    steps:
      - uses: actions/checkout@v7
      - id: s
        run: echo "list=$(ls services | jq -R . | jq -sc .)" >> "$GITHUB_OUTPUT"
  deploy:
    needs: plan
    strategy:
      fail-fast: false
      max-parallel: 3
      matrix:
        service: ${{ fromJSON(needs.plan.outputs.services) }}
    uses: ./.github/workflows/deploy-service.yml
    with:
      service: ${{ matrix.service }}
      environment: staging
    secrets: inherit
```
A job that `uses:` a workflow cannot have `steps`, `runs-on` or `environment` — those live
inside the callee. Per the docs it can only use `name`, `uses`, `with`, `secrets`, `strategy`, `needs`, `if`,
`concurrency` and `permissions` (plus `cache-mode` where available). `matrix` is available in `with`, `name`,
`concurrency` and `secrets` there, but not in the job-level `if`.

## 2. Callee
```yaml
on:
  workflow_call:
    inputs:
      service:
        type: string
        required: true
      environment:
        type: string
        default: staging
    outputs:
      url:
        value: ${{ jobs.deploy.outputs.url }}
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    concurrency:
      group: deploy-${{ inputs.environment }}-${{ inputs.service }}
    outputs:
      url: ${{ steps.d.outputs.url }}
    steps:
      - id: d
        run: echo "url=https://${{ inputs.service }}.example.com" >> "$GITHUB_OUTPUT"
```

## 3. Names and outputs
Check names combine the caller job and the callee job with ` / ` (read the exact text, including how matrix
values are shown, from a real run). Set `name:` on the callee jobs for readability.
Outputs of a matrixed reusable workflow collapse (docs): `needs.deploy.outputs.url` is the output of the **last
successfully completing** leg that actually sets a value, so an empty value from a later leg does not overwrite
an earlier one. Collect per-leg results via artifacts or step summaries instead.

## 4. Limits
- GitHub.com: at most **50 unique** reusable workflows per workflow file (nested ones included) and ten levels of
  workflows (caller + nine); GHES: 20 and four. A matrix over one `uses:` is still one unique workflow.
- Max 256 matrix jobs per workflow run (docs); `max-parallel` throttles.
- `secrets: inherit` passes all caller secrets to the directly called workflow; explicit `secrets:` must list each.
- Callee cannot read caller `env`; everything goes through `inputs`.
- Input `type` must be `boolean`, `number` or `string`; pass JSON as a string and `fromJSON` inside.

## 5. Gotchas
- Guard the empty case: `if: needs.plan.outputs.services != '[]'` on `deploy`, and handle a `skipped`
  `needs.deploy.result` in aggregate jobs (what an empty matrix does without the guard was not tested here).
- `matrix` is not available in the caller's job-level `if:`; per-leg skipping needs `if:` inside the callee using `inputs`.
- A same-repo `./.github/workflows/x.yml` reference runs the callee from the same commit as the caller (docs),
  so same-repo PRs test caller and callee together; `owner/repo/...@ref` pins a ref.

## Verify
- [ ] Adding a directory under `services/` adds a leg with no YAML change.
- [ ] Each leg shows as its own check with the service name.
- [ ] A failing leg does not cancel siblings (`fail-fast: false`).
