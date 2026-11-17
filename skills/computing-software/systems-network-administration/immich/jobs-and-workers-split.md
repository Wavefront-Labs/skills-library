---
id: computing-software.systems-network-administration.immich.jobs-and-workers-split
name: jobs-and-workers-split
category: computing-software
field: systems-network-administration
product: immich
tags: [workers, microservices, immich-workers-include, immich-workers-exclude, api]
level: practitioner
status: docs-checked
description: "Split the immich-server container into an API-only service and a microservices service with IMMICH_WORKERS_INCLUDE and IMMICH_WORKERS_EXCLUDE."
sources:
  - https://docs.immich.app/administration/jobs-workers
  - https://docs.immich.app/install/environment-variables
  - https://docs.immich.app/guides/scaling-immich
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run the web/API workload and the background job workload in separate containers so jobs cannot starve the UI.

The `immich-server` container holds two workers:

- `api` answers requests from the web and mobile apps.
- `microservices` does everything else as background jobs (thumbnail generation, video encoding and so on).

To split them:

1. In `docker-compose.yml`, copy the whole `immich-server` block as a new service named `immich-microservices` with `container_name: immich_microservices`.
2. Remove the `ports:` mapping (`2283:2283`) from the copy, since only the API container serves clients.
3. Set an environment variable on each service.

```yaml
services:
  immich-server:
    environment:
      IMMICH_WORKERS_INCLUDE: 'api'

  immich-microservices:
    environment:
      IMMICH_WORKERS_EXCLUDE: 'api'
```

`IMMICH_WORKERS_INCLUDE` runs only the listed workers. `IMMICH_WORKERS_EXCLUDE` runs every default worker except the listed ones; if INCLUDE is also set, it matches against that list instead. Both variables apply to the server container.

Both containers must reach the same Postgres, Redis and media files (see the scaling guide). Job status is visible under Administration, Jobs.

Use this when you want to throttle or distribute the workers. The scaling guide says extra containers on a single machine are unlikely to help; raise job concurrency in the admin panel instead.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading administration/jobs-workers in full, the Workers table in install/environment-variables, and guides/scaling-immich in full.
Reworded: the shared-configuration sentence and the when-to-use sentence, to what the pages state.
Method: documentation only; no commands were run.
