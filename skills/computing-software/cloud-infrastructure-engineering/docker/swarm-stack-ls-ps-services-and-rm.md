---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-stack-ls-ps-services-and-rm
name: swarm-stack-ls-ps-services-and-rm
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm-stack, stack-ps, stack-rm, stack-deploy, docker-swarm, task-state]
level: practitioner
status: docs-checked
description: "Operate Swarm stacks: stack ls/services/ps with filters and no-trunc errors, deploy --prune and --resolve-image, stack config, and what stack rm leaves behind."
sources: ["https://docs.docker.com/reference/cli/docker/stack/ls/", "https://docs.docker.com/reference/cli/docker/stack/ps/", "https://docs.docker.com/reference/cli/docker/stack/services/", "https://docs.docker.com/reference/cli/docker/stack/rm/", "https://docs.docker.com/reference/cli/docker/stack/config/", "https://docs.docker.com/reference/cli/docker/stack/deploy/", "https://docs.docker.com/engine/swarm/stack-deploy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swarm stack ls, ps, services and rm

## Inspect
```bash
docker stack ls                                         # stacks and service counts
docker stack services shop                              # replicas per service: 3/3 healthy, 1/3 problem
docker stack ps shop                                    # every task, including history
docker stack ps shop --no-trunc --filter desired-state=running
docker stack ps shop --filter desired-state=shutdown --format '{{.Name}} {{.Error}}'
docker stack ps shop --format '{{.Name}}\t{{.Node}}\t{{.CurrentState}}\t{{.Error}}'
```
`--no-trunc` shows full error strings in the ERROR column, the fastest way to see why tasks churn.

## Deploy options
```bash
docker stack config -c stack.yaml -c stack.prod.yaml > resolved.yaml   # merged, interpolated
docker stack deploy -c stack.yaml -c stack.prod.yaml --with-registry-auth --prune shop
docker stack deploy -c stack.yaml --resolve-image changed shop
docker stack deploy -c stack.yaml --detach=false shop                  # wait for convergence (--detach defaults to true)
```
- `--prune` removes services no longer defined in the files.
- `--resolve-image always|changed|never`: whether to query the registry for digests.
- Stack files are Compose files; unsupported keys (for example `build`, `links`) are skipped with an `Ignoring unsupported options` message.

## Remove
```bash
docker stack rm shop
```
Removes the stack from the swarm (run it on a manager). Afterwards check what remains: `docker service ls`, `docker network ls`, `docker secret ls`, `docker config ls`, and on each node `docker volume ls`.

## Gotchas
- Network, volume and service names are prefixed with the stack name (`shop_web`, `shop_default`).
- Swarm keeps a limited task history (`--task-history-limit`, default 5), so `stack ps` shows only recent tasks per slot.

## Checked
2026-10-25, against docker/docs engine and swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: `stack ls/ps/services` options and `--format` placeholders (`.Name`, `.Node`, `.CurrentState`, `.Error`, `.Replicas`); `stack ps` filters and `--no-trunc`; `docker stack config -c ... ` merges and interpolates; `docker stack deploy` flags `--prune`, `--resolve-image always|changed|never`, `--with-registry-auth`, `--detach` (default true); stack names prefix network, volume and service names; task history limit default 5. Removed: specific error strings, claims about what `stack rm` leaves behind and its asynchronous behaviour, volume-separation claim.
Method: documentation only; no commands were run.
