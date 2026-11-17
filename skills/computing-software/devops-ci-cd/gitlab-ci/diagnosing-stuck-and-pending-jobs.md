---
id: computing-software.devops-ci-cd.gitlab-ci.diagnosing-stuck-and-pending-jobs
name: diagnosing-stuck-and-pending-jobs
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, job-stuck-pending, runner-tags-mismatch, troubleshooting, resource-group, stuck-jobs]
level: practitioner
status: docs-checked
description: "Find why a GitLab CI job is pending, stuck or dropped: runner tag mismatch, protected runners, environments, resource groups, and the failure reasons GitLab sets."
sources: ["https://docs.gitlab.com/ci/jobs/job_troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing stuck and pending jobs

## Pending: no runner picks it up
1. Compare the job `tags:` and protected status with the runners available to the project (the docs list tags and protected status as matching requirements); check the runner is online.
2. Capacity: all matching runners busy; read the runner's logs.
3. With no matching runner GitLab drops the job after 1 hour (`stuck_pending_no_matching_runners`); with matching runners that stay busy, after 24 hours (`stuck_pending_with_matching_runners`).

## Pending for other reasons
- Manual job on a protected environment: your user must be in *Allowed to deploy*.
- *Prevent outdated deployment jobs* blocks a job that would overwrite a newer deployment.
- A `resource_group` held by another job serialises runs.

## Dropped while running
No log update for 30 minutes: `no_updates_running`. Past `timeout` plus 15 minutes: `server_timeout_running`.

## Config seems ignored
CI config is read when the pipeline is created; retrying a job reuses it. Start a new pipeline.

## Check
Read the failure reason on the job page and the runner log.

## Verify
The job moves to running within the expected queue time; no `stuck_` failure reason appears.

## Checked

2026-11-02. Confirmed: drop thresholds and reasons (pending 24 h `stuck_pending_with_matching_runners`, pending 1 h `stuck_pending_no_matching_runners`, running 30 min no updates `no_updates_running`, configured timeout plus 15 min `server_timeout_running`); protected environment 'Allowed to deploy' and 'Prevent outdated deployment jobs' (GitLab job troubleshooting and environments docs). Removed: runner-setting specifics, gitlab-runner verify, admin menu path, glab commands.

Method: documentation only; no commands were run.
