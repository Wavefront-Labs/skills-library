---
id: computing-software.systems-network-administration.immich.scaling-immich
name: scaling-immich
category: computing-software
field: systems-network-administration
product: immich
tags: [scaling, multiple-instances, redis, postgres, workers]
level: advanced
status: docs-checked
description: "Run several immich-server instances against shared Postgres, Redis and storage, disable the API worker on job nodes, and scale down safely."
sources:
  - https://docs.immich.app/guides/scaling-immich
  - https://docs.immich.app/administration/jobs-workers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: spread Immich across several machines, for example a gaming PC for transcoding and thumbnails, or a Kubernetes cluster.

The backend is designed to run multiple instances in parallel. The single requirement is that every instance connects to the same Postgres database, the same Redis, and the same filesystem for media.

All state lives in Postgres, Redis and the filesystem, so there is no risk in stopping a running `immich-server` container when you scale down.

If you only want more background-task capacity, you can disable the API worker on the extra containers so they only process jobs:

```yaml
environment:
  IMMICH_WORKERS_EXCLUDE: 'api'
```

Run the user-facing container with `IMMICH_WORKERS_INCLUDE: 'api'` if you want a dedicated API node. See the jobs and workers split skill.

For each additional node, point it at the shared services with the usual variables: `DB_HOSTNAME` (or `DB_URL`), `REDIS_HOSTNAME`, and the same mount for `UPLOAD_LOCATION`. A remote machine learning container can be shared too; see the remote machine learning skill.

Single machine caveat: if you have only one host, extra containers are unlikely to help. An Immich container already runs multiple background tasks at once, and you can raise their number from the admin panel (System Settings, Job Settings).

The docs deliberately give no step-by-step instructions for multi-machine setups, because environments vary widely. In some environments, scaling up is as simple as increasing the replica count.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading guides/scaling-immich in full and administration/jobs-workers in full; variable names checked in install/environment-variables.
Removed: nothing.
Method: documentation only; no commands were run.
