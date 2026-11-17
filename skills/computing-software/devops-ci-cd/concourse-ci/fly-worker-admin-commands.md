---
id: computing-software.devops-ci-cd.concourse-ci.fly-worker-admin-commands
name: fly-worker-admin-commands
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [fly, workers, prune-worker, land-worker, containers, volumes, curl, wall]
level: practitioner
status: docs-checked
description: "Use fly to administer a cluster: list workers, prune stalled ones, land a worker, list containers and volumes, call the API with fly curl, and set a broadcast Wall message."
sources:
  - https://concourse-ci.org/docs/operation/administration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Concourse administration commands, all run against a target such as `-t example`.

**Workers.** `fly -t example workers` lists registered workers with metadata, useful when a worker keeps dropping out or is tasked with too many containers. To remove a stalled, landing, landed or retiring worker:

```shell
fly -t example prune-worker --worker worker-name
fly -t example prune-worker --all-stalled
```

Use these only when you know the worker is not coming back. A running worker cannot be pruned because it would simply re-register. To start landing a worker so it drains and eventually exits: `fly -t example land-worker --worker worker-name`.

**Diagnostics.** `fly -t example containers` lists active containers across all workers, which helps when choosing something to `fly intercept`. `fly -t example volumes` lists active volumes, showing caches warming and giving a hint of disk use. `fly curl` is a shim around `curl` for arbitrary API requests: `fly -t example curl /api/v1/info`. To pass flags to curl, put `--` after the path:

```shell
fly -t example curl /api/v1/builds -- \
    -X PUT \
    -H "Content-type: application/json" \
    -d @plan.json
```

**Wall.** A banner shown in the web UI to tell all teams the system is unstable. `set-wall` and `clear-wall` require main team membership: `fly -t main set-wall --message="text" --ttl=5m`, `fly -t main get-wall`, `fly -t main clear-wall`.

## Checked

2026-11-04. Every command and flag copied from the Administration page (Managing Workers, Broadcast Message System, Diagnostic sections).

Method: documentation only; no commands were run.
