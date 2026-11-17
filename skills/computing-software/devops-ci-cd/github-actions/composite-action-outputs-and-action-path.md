---
id: computing-software.devops-ci-cd.github-actions.composite-action-outputs-and-action-path
name: composite-action-outputs-and-action-path
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, composite-outputs, github-action-path, composite-action-shell-required, composite-inputs-env, composite-action-if, composite-secrets, composite-nested-uses, composite-working-directory, action-ref-context, composite-actions, runs-using-composite, action-yml]
level: practitioner
status: verified
description: "Write composite actions that return outputs (steps.id.outputs mapped in action.yml), locate bundled scripts via github.action_path, and avoid the shell-required, no-secrets and if-on-steps pitfalls."
sources: ["https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-composite-action", "https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runs-for-composite-actions", "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs#github-context"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite action outputs and github.action_path

**Goal:** a composite action that ships its own scripts and hands values back to the caller.

## 1. action.yml with outputs
```yaml
name: version-info
inputs:
  prefix: { default: v }
outputs:
  version:
    description: computed version
    value: ${{ steps.calc.outputs.version }}     # map a step output; required
runs:
  using: composite
  steps:
    - id: calc
      shell: bash                                 # REQUIRED on every run step in composites
      env:
        PREFIX: ${{ inputs.prefix }}
      run: |
        "${GITHUB_ACTION_PATH}/scripts/version.sh" "$PREFIX" >> "$GITHUB_OUTPUT"
    - shell: bash
      run: echo "::notice::version=${{ steps.calc.outputs.version }}"
```
Caller: `- id: v` + `uses: ./.github/actions/version-info` → `${{ steps.v.outputs.version }}`.
Each output's `value` is required. Outputs are strings (limit 1 MB per job); set step outputs with
`echo "name=value" >> "$GITHUB_OUTPUT"`.

## 2. github.action_path
`${{ github.action_path }}` / `$GITHUB_ACTION_PATH` is the path where the action is located (only
supported in composite actions). Use it for every file the action bundles. Store bundled scripts with the
executable bit in git: `git update-index --chmod=+x scripts/version.sh` records mode `100755` (checked
locally with `git ls-files -s`).

## 3. Things composites cannot do
- Read `secrets.*` — the `secrets` context does not exist inside; pass secrets as `inputs`
  (they stay masked) or rely on env vars the caller sets.
- Composite steps support `if` and `continue-on-error` per step; `shell` is required on every step that
  has `run`.
- `github.action_ref` and `github.action_repository` must not be used directly in `run`; reference them
  via the `env` context instead (GitHub docs).

## 4. Inputs as env
Pass inputs to scripts through an intermediate environment variable (GitHub's recommended defence
against script injection):
```yaml
    - shell: bash
      env: { PREFIX: "${{ inputs.prefix }}" }
      run: ./script.sh "$PREFIX"
```
Never splice `${{ inputs.x }}` into `run:` text — injection.

## 5. Nested actions
Composite steps may `uses:` other actions, including other composites (GitHub's docs: up to 10 composite
actions nested in one workflow). A `./path` reference resolves in the runner's workspace (the caller's
checkout), so reference sibling actions in another repository as `owner/repo/path@ref`.

## Verify
- [ ] Caller reads the output and it is non-empty.
- [ ] Bundled script runs from a *different* repo (path resolved via `GITHUB_ACTION_PATH`).
- [ ] `actionlint` passes: no missing `shell:` on composite steps.
