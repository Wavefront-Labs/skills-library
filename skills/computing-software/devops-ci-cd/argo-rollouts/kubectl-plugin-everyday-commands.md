---
id: computing-software.devops-ci-cd.argo-rollouts.kubectl-plugin-everyday-commands
name: kubectl-plugin-everyday-commands
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [kubectl-argo-rollouts, promote, abort, retry, undo, status, lint, set-image, cli, argo-rollouts]
level: practitioner
status: docs-checked
description: "Drive rollouts from the CLI: get -w, promote --full, abort, retry, undo, set image, status and lint."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/
  - https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run `kubectl argo rollouts` to list commands; flags mirror kubectl (`-n`, `-w`).

- `get rollout NAME -w` draws a live tree of the Rollout, its revisions, ReplicaSets, pods, AnalysisRuns, Experiments and Jobs, updating as it progresses.
- `promote NAME` resumes a rollout paused at a canary step or a blue-green pre-promotion. `promote NAME --full` skips analysis, pauses and steps entirely.
- `abort NAME` stops progression and reverts all steps; the previous ReplicaSet becomes active. Note `spec.template` still holds the new version, so leaving the aborted state tries the new version again; set the template back to fully revert.
- `retry rollout NAME` retries an aborted rollout; `retry experiment` exists too.
- `undo NAME` rolls back to the previous revision; `--to-revision=3` picks one.
- `set image NAME CONTAINER=IMAGE` updates an image; `*=IMAGE` sets all containers.
- `status NAME` watches until the rollout finishes and returns success only if healthy; `--timeout 60s` bounds it and `--watch=false` just prints. Good for CI gates.
- `lint -f my-rollout.yaml` validates a Rollout file.
- `pause`, `restart`, `list rollouts`, `list experiments`, `terminate analysisrun|experiment`, `create analysisrun`, `dashboard`, `notifications` are also available.

Example CI gate: `kubectl argo rollouts status my-app --timeout 10m`.

Verify the plugin is installed with `kubectl argo rollouts version`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_promote/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_undo/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_set_image/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_status/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_lint/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_retry_rollout/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_retry_experiment/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_list_experiments/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_terminate/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_abort/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_get_rollout/.

Removed or corrected: the dry-run verification step.

Method: documentation only; no commands were run.
