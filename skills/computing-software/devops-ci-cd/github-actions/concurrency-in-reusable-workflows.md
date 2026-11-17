---
id: computing-software.devops-ci-cd.github-actions.concurrency-in-reusable-workflows
name: concurrency-in-reusable-workflows
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, reusable-workflow-concurrency, concurrency-deadlock, concurrency]
level: advanced
status: docs-checked
description: "Set concurrency in reusable workflows without self-cancelling: why caller and callee sharing a group key deadlocks or cancels, and how to scope keys with inputs."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#supported-keywords-for-jobs-that-call-a-reusable-workflow", "https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrency in reusable workflows

In a called workflow, `github.workflow` resolves to the **caller's** workflow name (documented). A
callee that declares
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```
computes the **same key as the caller** if the caller uses the same expression (for the `github.workflow` part). Result: the callee run
cancels its own caller (the docs state that using the same `group` value with `cancel-in-progress: true` in both caller and called workflows causes the already-running workflow to be cancelled).

## Patterns
1. Put workflow-level concurrency only in the **caller**. Callees use **job-level** concurrency for
   the specific resource they serialise:
   ```yaml
   # reusable deploy.yml
   jobs:
     deploy:
       concurrency:
         group: deploy-${{ inputs.environment }}
         cancel-in-progress: false
   ```
2. If the callee must have its own workflow-level group, add a distinct prefix plus an input:
   `group: reusable-build-${{ inputs.component }}-${{ github.ref }}`.
3. Matrix over a reusable workflow: include the matrix value in the group or every leg cancels the
   others: `group: deploy-${{ matrix.region }}`.

## Diagnosing
- A caller that is cancelled right after its callee starts, with both using the same `github.workflow`-based group, is a key collision.
- Print the keys: add a step `run: echo "${{ github.workflow }}-${{ github.ref }}"` in both.

## Verify
- [ ] Two quick pushes: the older caller cancels as a whole, never half-way inside the callee.
- [ ] Two environments deploy in parallel; the same environment serialises.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- A called workflow uses the caller's name in github.workflow, and an identical group with cancel-in-progress true in caller and callee cancels the running caller: confirmed in the reusable workflow reference (supported keywords note).
- Job-level concurrency group and cancel-in-progress syntax, and matrix being an allowed context at job level: confirmed in the concurrency documentation.
- Removed unconfirmed deadlock and UI-annotation claims.

Method: documentation only; no commands were run.
