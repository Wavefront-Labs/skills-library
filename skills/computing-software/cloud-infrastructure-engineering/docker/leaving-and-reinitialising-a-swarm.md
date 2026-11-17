---
id: computing-software.cloud-infrastructure-engineering.docker.leaving-and-reinitialising-a-swarm
name: leaving-and-reinitialising-a-swarm
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-swarm, swarm-leave, force-new-cluster, swarm-init, raft-backup, disaster-recovery]
level: advanced
status: docs-checked
description: "Leave a swarm cleanly on workers and managers, tear a cluster down, re-initialise from a surviving manager with --force-new-cluster, and what state survives each step."
sources: ["https://docs.docker.com/reference/cli/docker/swarm/leave/", "https://docs.docker.com/engine/swarm/admin_guide/", "https://docs.docker.com/reference/cli/docker/swarm/init/", "https://docs.docker.com/reference/cli/docker/node/rm/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leaving and re-initialising a swarm

## Leave
```bash
docker swarm leave                 # worker: tasks stop, node shows Down on managers
docker swarm leave --force         # manager: required; demote first if the cluster should survive
```
A node that has left stays in `docker node ls` until a manager removes it (`docker node rm <node>`; a node must be Down first, or use `--force`).

## Tear down a whole cluster
```bash
docker stack rm <each stack>; docker service rm $(docker service ls -q)
# workers first
docker swarm leave
# managers: demote all but one, then on the last one
docker swarm leave --force
```

## Lost quorum: re-initialise from a survivor
When a majority of managers is gone, the cluster cannot schedule or change anything (running
tasks keep running). On one healthy manager:
```bash
docker swarm init --force-new-cluster --advertise-addr <this-node-ip>
```
- The manager keeps the previous information about services and tasks and the worker nodes; it removes all other managers.
- Makes it the single manager; promote others again (`docker node promote`) after they rejoin
  with fresh join tokens.
- Remove dead managers with `docker node demote` / `docker node rm --force` (demote before force-removing a manager).

## Restore from backup instead
If no manager has good state, restore a Raft backup onto a fresh node (stop Docker, replace
`/var/lib/docker/swarm` with the backup, start, then `--force-new-cluster`). Autolocked swarms
need the unlock key.

## Gotchas
- `--force-new-cluster` restarts the node as a single-node manager from its own data, so run it on the manager with the freshest state.
- `docker swarm leave --force` on a manager does not reconfigure the swarm to keep a quorum; use it only when the swarm will no longer be used, otherwise demote first.

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: `swarm leave` on a worker; `--force` on a manager does not preserve quorum and is for swarms that will not be reused; `--force-new-cluster` keeps services, tasks, workers, secrets and configs and drops other managers; backup/restore procedure (stop Docker, replace `/var/lib/docker/swarm`, start, `docker swarm init --force-new-cluster`, unlock key needed); `docker node rm` needs a Down node unless `--force`. Removed: what is cleared from `/var/lib/docker/swarm` on leave, container and volume survival, new-node-ID and Raft-index claims.
Method: documentation only; no commands were run.
