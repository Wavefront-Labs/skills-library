---
id: computing-software.devops-ci-cd.gitlab-ci.pipeline-efficiency-retry-and-timeouts
name: pipeline-efficiency-retry-and-timeouts
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, pipeline-efficiency, pipeline-duration, git-depth, git-strategy, git-fetch-extra-flags, git-submodule-strategy, fastzip, artifact-compression-level, cache-compression-level, interruptible, auto-cancel-redundant, job-retry, retry-when, retry-max, job-timeout, timeout-keyword, runner-timeout, exit-codes, allow-failure-exit-codes, needs-optimisation, parallel-keyword, pipeline-analytics, ci-cd-analytics, pipeline-critical-path, runner-system-failure, stuck-or-timeout-failure]
level: practitioner
status: docs-checked
description: "Faster, more resilient GitLab pipelines: shallow clones and GIT_STRATEGY, fastzip, needs/parallel, interruptible auto-cancel, targeted retry, timeouts, exit-code allow_failure."
sources: ["https://docs.gitlab.com/ci/pipelines/pipeline_efficiency/", "https://docs.gitlab.com/ci/yaml/", "https://docs.gitlab.com/ci/runners/configure_runners/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline efficiency, retry and timeouts

**Goal:** shorter wall time per MR, fewer minutes burned on superseded commits, and
transient failures that heal themselves without masking real bugs.

## 1. Find the slow part first
CI/CD analytics shows pipeline health and duration; the full pipeline graph with `needs`
dependencies shows the critical path, the longest chain of `needs`. Shaving a job off the
critical path wins; shaving one that runs in parallel doesn't. Long queue time points at
runner capacity, not pipeline design.

## 2. Clone less
```yaml
variables:
  GIT_DEPTH: "20"                      # new projects default to 20; lower for build-only jobs
  GIT_STRATEGY: fetch                  # clone | fetch | none ; `none` for deploy jobs using artifacts only
  GIT_SUBMODULE_STRATEGY: none         # recursive only where needed
  GIT_FETCH_EXTRA_FLAGS: "--no-tags --prune"
  GIT_CLEAN_FLAGS: "-ffdx -e node_modules/"   # keep installed deps between jobs on the same runner
```
A shallow `GIT_DEPTH` breaks `git describe` (only part of the history is present), and a
value that is too small makes old commits unresolvable when a job is retried or queued
(`unresolved reference`) — those jobs set a deeper value.

## 3. Artifacts and cache speed
```yaml
variables:
  FF_USE_FASTZIP: "true"
  ARTIFACT_COMPRESSION_LEVEL: "fast"   # fastest | fast | default | slow | slowest
  CACHE_COMPRESSION_LEVEL: "fastest"
  TRANSFER_METER_FREQUENCY: "5s"       # progress output to see where time goes
```
`ARTIFACT_COMPRESSION_LEVEL` and `CACHE_COMPRESSION_LEVEL` work with the Fastzip archiver
only, so `FF_USE_FASTZIP` must also be enabled. Only upload what the next job needs;
`artifacts:exclude` the `.git`/`node_modules`; `cache:policy: pull` on consumer jobs.

## 4. Structure
- `needs:` to break stage barriers (DAG); `needs: []` to start at pipeline start.
- `parallel: 4` + `CI_NODE_INDEX`/`CI_NODE_TOTAL` for test splitting; `parallel:matrix` for
  version/OS grids.
- Merge jobs that each spend 60 s on setup for 10 s of work; split jobs whose parts could
  run concurrently.
- `rules:changes` to skip irrelevant jobs; `workflow:rules` to avoid duplicate branch+MR pipelines.
- Prebuilt CI image with toolchain and deps (`image: $CI_REGISTRY_IMAGE/ci:latest`) instead
  of `apt-get install` every job.

## 5. Stop wasting minutes on superseded commits
```yaml
default:
  interruptible: true          # job can be auto-cancelled when a newer pipeline on the same ref starts
deploy:
  interruptible: false         # never cancel mid-deploy
```
The *Auto-cancel redundant pipelines* feature must be enabled, or `interruptible` has no
effect. The default `workflow: auto_cancel: on_new_commit: conservative`; setting
`on_new_commit: interruptible` cancels only the interruptible jobs, and
`on_job_failure: all` cancels the rest of a pipeline when any job fails.

## 6. Retry — only on the failures that deserve it
```yaml
integration-test:
  retry:
    max: 2                    # 0–2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure   # deprecated in GitLab 19.1: use the specific stuck_* / no_updates_* reasons
      - api_failure
      - scheduler_failure
      - unknown_failure
    exit_codes: [137, 143]    # GitLab 17.5+: retry only on these exit codes
```
`retry: 2` alone retries **every** failure including real test failures, which hides flaky
tests and doubles cost — list `when:` explicitly. Flaky tests belong in a quarantine job,
not in `retry`.

## 7. Timeouts and exit codes
- `timeout: 30m` per job: the job-level timeout can be longer than the project timeout but
  not longer than the runner's maximum job timeout (the shorter one applies). Set job
  timeouts so hung jobs free runners.
- `allow_failure: { exit_codes: [3, 4] }` → job passes with a warning for *expected*
  non-zero codes (e.g. "no changes to apply").
- `after_script` has its own timeout (`RUNNER_AFTER_SCRIPT_TIMEOUT`, default 5 min);
  `RUNNER_SCRIPT_TIMEOUT` caps `script`. Keep both below the job timeout so artifacts and
  cache can still upload.
- Use `cmd || true` for optional steps, never blanket `allow_failure: true` on critical jobs.

## Verify
- [ ] Median MR pipeline time dropped and the critical path is documented.
- [ ] Pushing twice quickly cancels the first pipeline's interruptible jobs.
- [ ] A real test failure is **not** retried; a `runner_system_failure` is.
- [ ] No job runs with the project default timeout unless justified.

## Checked

2026-10-28. Confirmed against the GitLab docs pages for pipeline efficiency, the CI/CD YAML reference and configure runners: GIT_DEPTH default of 20 for new projects, `git describe` and unresolved-reference caveats, GIT_CLEAN_FLAGS and GIT_FETCH_EXTRA_FLAGS, compression level values and the Fastzip requirement, TRANSFER_METER_FREQUENCY, `workflow:auto_cancel` options and the `conservative` default, `retry:when` values, `retry:exit_codes` (GA 17.5), the `stuck_or_timeout_failure` deprecation (19.1), `allow_failure:exit_codes`, RUNNER_AFTER_SCRIPT_TIMEOUT default of 5 minutes, runner maximum job timeout. Removed: the jq/curl snippet, the Jobs API failure_reason tip, the project default and maximum timeout figures, the UI settings path, the mirror and S3/GCS cache advice, and the `set -e` claim (not in the fetched pages).

Method: documentation only; no commands were run.
