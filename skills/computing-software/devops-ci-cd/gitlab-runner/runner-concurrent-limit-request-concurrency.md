---
id: computing-software.devops-ci-cd.gitlab-runner.runner-concurrent-limit-request-concurrency
name: runner-concurrent-limit-request-concurrency
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [concurrency, concurrent, limit, request-concurrency, job-flow]
level: advanced
status: docs-checked
description: "How concurrent, limit and request_concurrency interact and what each one bounds."
sources: ["https://docs.gitlab.com/runner/fleet_scaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Concurrent, limit and request_concurrency

Three settings shape throughput:

- `concurrent` (global): jobs that can run at once using all configured runners on the host system.
- `limit` (per `[[runners]]`): the number of sub-processes (workers) that runner can create. On runners that do not autoscale it is the capacity of the runner on the host system. On autoscaling runners it is the total number of runners you want to run.
- `request_concurrency` (per `[[runners]]`): concurrent requests for new jobs from GitLab; default `1`.

The simplest setup uses one `[[runners]]` section with the shell executor and `concurrent = 1`, so only one worker executes jobs. Registering several runners on one machine gives several `[[runners]]` sections that share the global `concurrent` budget.

The docs point to a GitLab knowledge-base article on concurrency tuning for how the three interact in detail.

## Checked

2026-11-03. Confirmed against concurrent, limit and request_concurrency definitions on Advanced configuration and Fleet scaling.

Method: documentation only; no commands were run.
