---
id: computing-software.devops-ci-cd.concourse-ci.resource-check-load-tuning
name: resource-check-load-tuning
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [resource-checking, check-interval, max-checks-per-second, webhook, pause-pipelines, timeouts, tuning]
level: advanced
status: docs-checked
description: "Reduce Concourse load as you scale: default check interval, webhook-resource interval, checks per second cap, auto-pausing idle pipelines, default task limits and step timeouts."
sources:
  - https://concourse-ci.org/docs/operation/tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Out of the box Concourse checks each resource about every minute so it feels snappy; at scale this becomes aggressive. Web node settings from the Performance Tuning page:

- `CONCOURSE_RESOURCE_CHECKING_INTERVAL`: the default check interval for every resource (the source of the 1 minute). Users override with `resource.check_every`.
- `CONCOURSE_RESOURCE_WITH_WEBHOOK_CHECKING_INTERVAL`: same, for resources with webhooks only. A large value such as `99h` effectively disables polling for them.
- `CONCOURSE_MAX_CHECKS_PER_SECOND`: cap on checks started per second, calculated as number of resources divided by the checking interval. A value of `-1` removes the cap. Use it when too many simultaneous checks overload workers.
- `CONCOURSE_PAUSE_PIPELINES_AFTER`: days since a pipeline last ran before it is auto-paused. With `90`, pipelines last run 91 days ago are paused. Forgotten pipelines still run resource checks, so this can pause up to roughly half of pipelines on large instances.
- `CONCOURSE_DEFAULT_TASK_{CPU/MEMORY}_LIMIT`: global defaults for tasks only, not check, get or put containers. Users can override via `container_limits`.
- `CONCOURSE_DEFAULT_{GET/PUT/TASK}_TIMEOUT`: global step timeouts so stuck tasks eventually finish. Users can override.

The page's main caveat: track metrics first so you have a before-and-after picture.

## Checked

2026-11-04. All variables and descriptions confirmed on the Performance Tuning page (The Big Caveat, Resource Checking, Pipeline Management sections).

Method: documentation only; no commands were run.
