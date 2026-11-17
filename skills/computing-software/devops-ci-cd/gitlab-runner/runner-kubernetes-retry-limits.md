---
id: computing-software.devops-ci-cd.gitlab-runner.runner-kubernetes-retry-limits
name: runner-kubernetes-retry-limits
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [retry-limit, retry-limits, kubernetes-api, backoff, resource-availability]
level: advanced
status: docs-checked
description: "Control retry of Kubernetes API calls and pod availability checks."
sources: ["https://docs.gitlab.com/runner/executors/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kubernetes retry settings

The executor retries failed Kubernetes API requests. `retry_limit` sets the maximum attempts to communicate with the Kubernetes API (the example config uses `5`). Backoff starts at 500 ms and `retry_backoff_max` (default 2000 ms, minimum 500 ms) caps it.

`retry_limits` sets how many times each request error is retried.

`resource_availability_check_max_attempts` is the maximum number of attempts to check that the service account or pull secret is available, with 5 seconds between attempts.

## Checked

2026-11-03. Confirmed against retry_limit, retry_backoff_max, retry_limits and resource_availability_check_max_attempts on the Kubernetes executor page. Removed the generic closing tip and the unconfirmed default.

Method: documentation only; no commands were run.
