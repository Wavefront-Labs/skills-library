---
id: computing-software.devops-ci-cd.github-actions.debugging-workflows-and-usage-limits
name: debugging-workflows-and-usage-limits
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, workflow-debugging, debug-logging, actions-step-debug, actions-runner-debug, re-run-failed-jobs, re-run-with-debug, act, nektos-act, gh-run, gh-run-view, gh-run-watch, run-logs, log-download, tmate, ssh-into-runner, usage-limits, actions-cost, billing-minutes, minute-multipliers, concurrency-limits, api-rate-limits, workflow-run-time-limit, job-time-limit, queue-time, runner-busy, actions-metrics, usage-report]
level: practitioner
status: docs-checked
description: "Diagnose failing or slow GitHub Actions runs (debug logging, gh run re-runs) and know the documented usage limits: 6 h jobs, concurrency caps, matrix and queue limits."
sources: ["https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging", "https://docs.github.com/en/actions/reference/limits", "https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs", "https://cli.github.com/manual/gh_run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging workflows and usage limits

**Goal:** get from "red X" to root cause in minutes, and keep the minutes bill and queue
times from growing unnoticed.

## 1. Read the run properly
```bash
gh run list --workflow ci.yml --branch main -L 10          # -w workflow, -b branch, -L limit
gh run view <run-id> --log-failed            # only failing steps' logs
gh run view <run-id> --job <job-id> --log    # one job
gh run watch <run-id> --exit-status          # block until done, exit non-zero on failure
gh run download <run-id> -n <artifact>
gh run rerun <run-id> --failed               # re-run only failed jobs (keeps successful ones)
gh run rerun <run-id> --debug                # re-run with debug logging on
```
Re-runs use the privileges of the actor who first triggered the workflow and the same `GITHUB_SHA` and
`GITHUB_REF` as the original run, and a run can be re-run at most 50 times (full and partial re-runs together).
To test a change, push a new commit.

## 2. Debug logging
- Set the secret or variable `ACTIONS_STEP_DEBUG` to `true` in the repository for step debug logging (more debug
  events in the step logs). Set `ACTIONS_RUNNER_DEBUG` to `true` for runner diagnostic logging: the log archive then
  contains the runner process log and worker process log in a `runner-diagnostic-logs` folder. If both a secret and
  a variable exist, the secret wins.
- Anyone who can run a workflow can enable both for a re-run (`gh run rerun --debug`).
- The `runner.debug` context lets a step run only when debug logging is on.
- Dump context once when expressions misbehave: `echo '${{ toJSON(github) }}'`.
- "Resource not accessible by integration" usually means a missing `GITHUB_TOKEN` permission (see the dedicated skill).

## 3. Usage limits (documented values)
| limit | value |
|---|---|
| job execution time, GitHub-hosted | 6 hours; set `timeout-minutes` lower (default 360) |
| job execution time, self-hosted | 5 days; job queue time 24 hours |
| workflow run time | 35 days, including waiting and approval; environment approval wait up to 30 days |
| job matrix | 256 jobs per workflow run |
| workflow runs queued | 500 workflow runs per 10 seconds; trigger events 1500 per 10 seconds per repository |
| concurrency group queue (`queue: max`) | 100 per group |
| concurrent jobs, standard hosted | Free 20, Pro 40, Team 60, Enterprise 500; macOS jobs 5, 5, 5, 50 |
| workflow file size | 500 KB |
| cache API limits | 200 uploads, 1500 downloads, 400 deletes per minute per repository |
Support can increase some concurrency limits (support ticket). Jobs beyond the concurrency limit queue.
For billing details (minutes, multipliers, storage) read the Actions billing documentation; no multiplier is
stated here.

## 4. Cost levers
Use `concurrency` with `cancel-in-progress` on pull requests, path filters, `timeout-minutes`, cache hits and
short artifact `retention-days`.

## Verify
- [ ] `gh run view --log-failed` gives the failing command and exit code.
- [ ] Debug re-run shows the extra debug events and the `runner-diagnostic-logs` folder.
- [ ] Every job has `timeout-minutes` well under 360.
- [ ] Jobs that could hang have a lower `timeout-minutes` than the default.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23 and cli/cli source (gh v2.103.2).
- gh run subcommand flags (list -w/-b/-L, view --log/--log-failed/--job, watch --exit-status, rerun --failed/--job/--debug, download -n): confirmed in cli/cli source (v2.103.2) and the re-run documentation.
- Debug logging variables, runner-diagnostic-logs folder, secret precedence, runner.debug context: confirmed in enable-debug-logging. Re-run semantics and the 50-run maximum: confirmed in re-run-workflows-and-jobs.
- Limits table values (6 h, 5 days, 24 h queue, 35 days, 30 days approval, matrix 256, 500 runs per 10 s, concurrency by plan, 500 KB file, cache API rates): confirmed in the limits reference. The earlier Enterprise figure of 180 was wrong (500).
- Removed act, tmate, OOM and memory claims, the GITHUB_TOKEN API rate figure, minute multipliers, per-workflow timing endpoint, metrics tab and log-size claims, which no fetched page confirms.

Method: documentation only; no commands were run.
