---
id: computing-software.devops-ci-cd.github-actions.run-name-dynamic-run-titles
name: run-name-dynamic-run-titles
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, run-name, dynamic-run-name, workflow-run-title, run-title, workflow-dispatch-inputs, actor-in-run-name, run-list-readability, gh-run-list, workflow-syntax]
level: intro
status: verified
description: "Give workflow runs meaningful titles with run-name so dispatch and scheduled runs show their inputs and actor in the run list instead of a bare commit message."
sources: ["https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#run-name"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# run-name: dynamic run titles

**Goal:** make the Actions run list searchable: "Deploy prod v1.4.2 by alice" instead of
twenty identical "Deploy" rows.

## 1. Syntax
```yaml
name: Deploy
run-name: Deploy ${{ inputs.environment }} ${{ inputs.version }} by @${{ github.actor }}
on:
  workflow_dispatch:
    inputs:
      environment: { type: environment }
      version: { type: string, required: true }
```
`run-name` is a top-level key, a string with expressions. Allowed contexts: `github`,
`inputs`, `vars` only (actionlint rejects `env` there). If omitted or whitespace-only, the run name is
event-specific information such as the commit message for `push` or the PR title for `pull_request`.

## 2. Useful recipes
```yaml
# scheduled runs: stamp the trigger
run-name: Nightly ${{ github.event_name == 'schedule' && 'scheduled' || 'manual' }} ${{ github.run_number }}

# repository_dispatch: surface the payload
run-name: Rebuild for ${{ github.event.client_payload.service }}@${{ github.event.client_payload.sha }}

# PR runs: keep the number visible
run-name: CI #${{ github.event.pull_request.number }} ${{ github.event.pull_request.title }}
```
`github.run_attempt` lets re-runs show "(attempt 2)".

## 3. Limits and gotchas
- Only `github`, `inputs` and `vars` are available, so it cannot reference `env`, `secrets`, `needs` or job outputs.
- Expressions that resolve empty leave gaps ("Deploy  by @alice") — guard with
  `${{ inputs.version || 'latest' }}`.
- Titles appear in `gh run list` (JSON field `displayTitle`), so they can be grepped:
  `gh run list --workflow deploy.yml --json displayTitle,conclusion`.

## Verify
- [ ] Two dispatch runs with different inputs are distinguishable in the run list.
- [ ] `gh run list --json displayTitle` shows the dynamic title.
