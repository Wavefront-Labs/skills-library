---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-service-modes-placement-and-resources
name: swarm-service-modes-placement-and-resources
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm, swarm-service, stack-deploy, global-mode, replicated-mode, deploy-key, stack-compose, service-constraint, placement-preference, swarm-reservations, swarm-limits]
level: advanced
description: "Write the deploy section of stack files: replicated vs global and job modes, placement constraints, spread preferences and max replicas per node, and resource reservations and limits."
sources: ["https://docs.docker.com/reference/compose-file/deploy/", "https://docs.docker.com/engine/swarm/services/", "https://docs.docker.com/reference/cli/docker/stack/deploy/", "https://docs.docker.com/reference/cli/docker/service/create/", "https://github.com/docker/cli/blob/master/cli/compose/schema/data/config_schema_v3.13.json"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Swarm service modes, placement and resources

## Stack file deploy section
```yaml
services:
  api:
    image: registry.example.com/api:1.4.0
    deploy:
      mode: replicated
      replicas: 4
      placement:
        constraints:
          - node.role == worker
          - node.labels.zone != eu-1c
        preferences:
          - spread: node.labels.zone       # balance across zones
        max_replicas_per_node: 2
      resources:
        limits: { cpus: "1.0", memory: 512M, pids: 200 }
        reservations: { cpus: "0.25", memory: 256M }
      restart_policy: { condition: on-failure, delay: 5s, max_attempts: 3, window: 60s }
      labels: { traefik.enable: "true" }      # service labels (not container labels)
  node-exporter:
    image: prom/node-exporter
    deploy:
      mode: global                             # exactly one per eligible node
  migrate:
    image: registry.example.com/api:1.4.0
    command: ["migrate"]
    deploy:
      mode: replicated-job                     # run to completion; also global-job
```
```sh
docker stack deploy -c stack.yaml --with-registry-auth --prune shop
```
`docker stack deploy` prints `Ignoring unsupported options` for fields it does not support, for example `build` and `links`.

## Modes
- **replicated**: N tasks anywhere eligible. Scale with `docker service scale shop_api=6`.
- **global**: one task on every node; a node added later automatically gets one -
  agents, log shippers, monitoring.
- **jobs**: one-shot tasks (`replicated-job` or `global-job`; `docker service create --max-concurrent` limits how many run at once).

## Placement
- Constraints: `node.id`, `node.hostname`, `node.role`, `node.platform.os/arch`,
  `node.labels.*` (manager-set), `engine.labels.*` (daemon-set).

## Resources
- **Reservations** are scheduling guarantees: a node only receives the task if unreserved
  CPU/memory suffice - over-reserving leaves tasks pending.
- **Limits** cap resource use (`--limit-cpu`, `--limit-memory`, `--limit-pids`); reservations and limits do not guarantee the host is never oversubscribed.
- Generic resources (GPUs) via `reservations.generic_resources` with node-advertised resources.

## Verify
`docker service ps shop_api --format '{{.Node}}'` shows spread across zones;
`docker service inspect shop_api -f '{{json .Spec.TaskTemplate.Resources}}'`.

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master) and the docker/cli stack schema v3.13. Confirmed: service modes `replicated`, `global`, `replicated-job`, `global-job` and `--max-concurrent`; placement constraint attributes node.id, node.hostname, node.role, node.platform.os/arch, node.labels, engine.labels; `--placement-pref` spread; stack keys `max_replicas_per_node`, `resources.limits.pids`, `generic_resources`; `stack deploy --prune` and `--with-registry-auth`; a task whose memory reservation cannot be met stays pending; `build` and `links` are ignored by stack deploy. Removed: Engine 20.10 version gate, the fuller ignored-keys list, soft/hard preference claim, OOM-kill wording.
Method: documentation only; no commands were run.
