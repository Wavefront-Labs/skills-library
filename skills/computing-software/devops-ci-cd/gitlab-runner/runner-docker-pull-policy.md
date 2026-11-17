---
id: computing-software.devops-ci-cd.gitlab-runner.runner-docker-pull-policy
name: runner-docker-pull-policy
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [pull-policy, always, if-not-present, never, allowed-pull-policies]
level: practitioner
status: docs-checked
description: "Pull policy values, retry lists and how allowed_pull_policies intersects with job settings."
sources: ["https://docs.gitlab.com/runner/executors/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker pull policies

`pull_policy` accepts `always`, `if-not-present` and `never`.

- `always`: pull before every job.
- `if-not-present`: use a local image if it exists, pull otherwise.
- `never`: only use images already on the host.

To retry a failed pull, repeat the same policy in `config.toml`; `pull_policy = ["always", "always"]` retries the pull one time.

`allowed_pull_policies` restricts what jobs may request with the `pull_policy` keyword in `.gitlab-ci.yml`. The effective policy is the intersection of the job's requested policies and the allowed list.

For shared runners holding private images, the security guide recommends `always` so a second user cannot run a cached private image they could not pull themselves.

## Checked

2026-11-03. Confirmed against pull policies, allowed_pull_policies intersection and retry on the Docker executor page and the Security page. Replaced the unsourced fallback example.

Method: documentation only; no commands were run.
