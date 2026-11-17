---
id: computing-software.devops-ci-cd.github-actions.managing-workflow-runs-via-api
name: managing-workflow-runs-via-api
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, workflow-runs-api, cancel-workflow-run, gh-run, force-cancel, delete-workflow-runs, rerun-failed-jobs]
level: practitioner
status: docs-checked
description: "List, watch, cancel, force-cancel, re-run and delete workflow runs with gh run, including clearing queues and understanding what cancellation does."
sources: ["https://cli.github.com/manual/gh_run", "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-cancellation", "https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing workflow runs via the CLI and API

## 1. Everyday gh run
```bash
gh run list --workflow ci.yml --branch main --status failure -L 20   # -s/--status filter, -L limit
gh run watch <run-id> --exit-status            # blocks; non-zero exit if run fails
gh run view <run-id> --log-failed              # only failed steps' logs
gh run rerun <run-id> --failed                 # re-run failed jobs (+ dependents)
gh run rerun <run-id> --debug                  # re-run with step debug logging
gh run cancel <run-id>                         # add --force to force-cancel
gh run delete <run-id>
gh run download <run-id> -n coverage
```

## 2. Bulk operations
```bash
# cancel everything queued for a branch (e.g. after a bad force-push storm)
gh run list --branch feature/x --status queued --json databaseId -q '.[].databaseId' |
  xargs -n1 gh run cancel
# delete finished runs of one workflow (review the list first)
gh run list --workflow ci.yml --status completed -L 100 --json databaseId -q '.[].databaseId' |
  xargs -n1 gh run delete
```
`gh run list --json` offers fields such as databaseId, status, conclusion, event, headBranch, workflowName,
createdAt. Deleting a run is permanent and needs write access.

## 3. What cancel does, and stuck runs
Cancellation re-evaluates `if` conditions: a job or step whose condition is true (for example `always()`) keeps
running, so use `if: ${{ !cancelled() }}` or `cancelled()` deliberately. Steps being cancelled get SIGINT, then
SIGTERM after 7500 ms, and the process tree is killed 2500 ms later; after a 5 minute cancellation timeout the
server forcibly terminates whatever is still running. `gh run cancel --force` submits a force-cancel request for a
run that will not stop.

## 4. Re-runs
Re-runs use the privileges of the actor who first triggered the workflow and the same `GITHUB_SHA` and
`GITHUB_REF`, so they do not pick up a fixed workflow file, and a run can be re-run at most 50 times.
`gh run rerun` takes `--failed` (failed jobs plus their dependencies), `--job` and `--debug`.

## Verify
- [ ] `gh run list --status queued` is empty after the bulk cancel.
- [ ] Deleted runs no longer appear in the Actions tab.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23 and cli/cli source (gh v2.103.2).
- gh run list (-w, -b, -s/--status, -L, --json including databaseId), cancel (--force, which posts to the run's force-cancel endpoint), delete, rerun (--failed, --job, --debug), view, watch --exit-status, download: confirmed in cli/cli pkg/cmd/run source (gh v2.103.2).
- Cancellation semantics (if conditions re-evaluated, SIGINT then SIGTERM after 7500 ms, 2500 ms, 5 minute timeout) and re-run rules (same GITHUB_SHA and GITHUB_REF, actor privileges, 50 re-runs): confirmed in the workflow-cancellation reference and re-run page.
- Removed unconfirmed REST filter list, logs deletion, pending_deployments and approve endpoints, rate-limit advice and the 30-day re-run window.

Method: documentation only; no commands were run.
