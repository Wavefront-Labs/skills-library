---
id: computing-software.devops-ci-cd.github-actions.reusable-workflows-and-composite-actions
name: reusable-workflows-and-composite-actions
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, reusable-workflows, workflow-call, composite-actions, action-yml, runs-using-composite, secrets-inherit, workflow-inputs, workflow-outputs, dry, shared-ci, central-workflows, platform-team, versioning, action-versioning, major-tag, nesting-limit, javascript-action, docker-action, uses, ci-templates]
level: advanced
status: verified
description: "Choose between reusable workflows and composite actions, wire inputs/secrets/outputs correctly, version them for many repos, and avoid nesting and context gotchas."
sources: ["https://docs.github.com/en/actions/sharing-automations/reusing-workflows", "https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-composite-action"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reusable workflows and composite actions

**Goal:** one place to maintain CI logic that dozens of repos call, without copy-paste
drift and without surprising callers when you change it.

## 1. Pick the right unit
| Need | Use |
|---|---|
| Share a few *steps* inside a caller's job (setup + lint, a build recipe) | **Composite action** |
| Share whole *jobs* — own `runs-on`, matrix, environments, `needs` graph | **Reusable workflow** |
| Logic that needs real code, error handling, API calls | JavaScript action (or a script in the composite) |

Rule of thumb: if it needs its own runner or an `environment:` with approvals, it's a
reusable workflow. If it should feel like one `uses:` step, it's a composite action.

## 2. Reusable workflow skeleton
```yaml
# org/ci-templates/.github/workflows/node-ci.yml
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: "22"
      working-directory:
        type: string
        default: "."
    secrets:
      NPM_TOKEN:
        required: false
    outputs:
      artifact-name:
        value: ${{ jobs.build.outputs.name }}
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      name: ${{ steps.meta.outputs.name }}
    defaults:
      run:
        working-directory: ${{ inputs.working-directory }}
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm
      - run: npm ci && npm test
      - id: meta
        run: echo "name=dist-${{ github.sha }}" >> "$GITHUB_OUTPUT"
```
Caller:
```yaml
jobs:
  ci:
    uses: org/ci-templates/.github/workflows/node-ci.yml@v2
    with:
      node-version: "20"
    secrets: inherit          # or map explicitly: NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```
Gotchas:
- A job that calls a reusable workflow can only use these keywords (docs): `name`, `uses`, `with`, `secrets`,
  `strategy`, `needs`, `if`, `concurrency`, `permissions` (plus `cache-mode` where available). No `steps`, no `runs-on`,
  and the calling job cannot set `environment` (set it on the job inside the called workflow).
- `env:` set in the caller does **not** propagate into the called workflow, and the callee's `env` is not visible to
  the caller. Pass values as inputs and read results via outputs.
- `permissions` in the called workflow can only *reduce* what the caller grants, never raise it.
- The `github` context in the called workflow is the **caller's** (event, ref, repo, and `github.workflow_ref`).
  To identify the template file itself use the `job` context (`job.workflow_ref`, `job.workflow_sha`,
  `job.workflow_repository`; not on GHES) or the `job_workflow_ref`/`job_workflow_sha` OIDC claims.
- Nesting on GitHub.com: up to ten levels (caller plus nine reusable levels) and at most 50 unique reusable workflows
  per workflow file, counting nested ones (4 levels and 20 on GHES). Loops are not allowed. Keep it to 1-2 levels.
- Private/internal template repos must allow access: *Settings > Actions > General > Access* on the template repo.

## 3. Composite action skeleton
```yaml
# org/actions/setup-toolchain/action.yml
name: setup-toolchain
inputs:
  python:
    description: Python version
    default: "3.12"
outputs:
  cache-hit:
    description: pip cache hit
    value: ${{ steps.py.outputs.cache-hit }}
runs:
  using: composite
  steps:
    - id: py
      uses: actions/setup-python@v7
      with:
        python-version: ${{ inputs.python }}
        cache: pip
    - shell: bash                      # mandatory on every run: step
      run: pip install -r "${{ github.action_path }}/requirements-tools.txt"
```
Gotchas:
- Every `run:` needs `shell:`; there is no default.
- Use `${{ github.action_path }}` (only set in composite actions, docs) to reach files shipped with the action.
- The `secrets` context is not available in composite actions (docs: for security reasons) — pass secrets as inputs.
- Debugging is harder than inline steps; echo key values.
- `if:` and `continue-on-error` are both documented step keys in a composite action's `runs.steps`.

## 4. Versioning for many callers
- Tag releases semver (`v2.3.1`) **and** move a major tag (`v2`) to the latest compatible release.
- Callers pin `@v2` internally (trusted org) or a full SHA (strict supply-chain posture).
  Dependabot's `github-actions` ecosystem updates actions and reusable workflows referenced with the
  `owner/repo@ref` syntax and ignores local `./.github/...` references (docs).
- Breaking change (renamed input, removed output) = new major. Keep `v1` alive until callers migrate.
- Add a CI job in the template repo that calls the workflow via `uses: ./.github/workflows/node-ci.yml`
  so a change is exercised before tagging.

## 5. Anti-patterns
- Giant "do-everything" workflow with 30 boolean inputs: split into 2–3 focused ones.
- Using `@main` from production repos: one bad push breaks every build in the org.
- Hiding `pull_request_target` logic in a template — the security review then has to cover every caller.

## Uncertainty
Limits and keyword lists are from the GitHub docs sources (reusing-workflow-configurations, metadata-syntax, contexts)
read 2026-10-20 and differ on GHES. Snippets pass actionlint and parse as YAML; nothing was run on GitHub's runners.

## Verify
- [ ] Each shared unit is the right type (steps → composite, jobs → reusable workflow).
- [ ] Inputs are typed with defaults; secrets passed explicitly or via `secrets: inherit` on purpose.
- [ ] Every composite `run:` has `shell:`; files referenced via `github.action_path`.
- [ ] Template repo has a self-test workflow and semver + moving-major tags.
- [ ] No production caller references `@main`.
- [ ] Outputs from the reusable workflow are readable in the caller (`needs.ci.outputs.artifact-name`).
