---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-node-ls-inspect-and-rm
name: swarm-node-ls-inspect-and-rm
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-swarm, node-ls, node-rm, node-inspect, node-ps, swarm-manager]
level: practitioner
status: docs-checked
description: "Read Swarm node health with node ls/inspect/ps, understand STATUS, AVAILABILITY and MANAGER STATUS values, and remove dead workers or managers without breaking quorum."
sources: ["https://docs.docker.com/reference/cli/docker/node/ls/", "https://docs.docker.com/reference/cli/docker/node/inspect/", "https://docs.docker.com/reference/cli/docker/node/rm/", "https://docs.docker.com/engine/swarm/manage-nodes/", "https://docs.docker.com/engine/swarm/admin_guide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swarm node ls, inspect and rm

## Reading node ls
```bash
docker node ls
# ID  HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS  ENGINE VERSION
```
| Column | Values | Meaning |
|---|---|---|
| STATUS | Ready, Down | Node state as seen by managers |
| AVAILABILITY | Active, Pause, Drain | Scheduler eligibility (set by you) |
| MANAGER STATUS | Leader, Reachable, Unreachable, (blank = worker) | Raft membership health |

```bash
docker node ls --filter role=manager --format '{{.Hostname}} {{.ManagerStatus}}'
docker node ls --filter node.label=zone=a
```

## Details
```bash
docker node inspect --pretty self
docker node inspect <node> -f '{{.Status.State}} {{.Status.Addr}}'
docker node inspect <node> -f '{{json .Spec.Labels}} {{json .Description.Resources}}'
docker node ps <node>                       # tasks scheduled there, with errors
docker node ps $(docker node ls -q) --filter desired-state=running
```
`ENGINE VERSION` drift across
nodes is worth catching before upgrades.

## Removing nodes
Worker that still runs:
```bash
docker node update --availability drain worker3     # move tasks away
# on worker3:
docker swarm leave
# on a manager:
docker node rm worker3
```
Worker that is dead (host gone): `docker node rm --force worker3`.

Manager:
```bash
docker node demote mgr3          # first: shrink the Raft membership cleanly
docker node rm mgr3              # after it is a worker (and has left or is dead)
```
Never `rm --force` a manager while it is still listed as Reachable without demoting: you
reduce quorum math unexpectedly. With 3 managers you can lose 1; with 5, 2.

## Gotchas
- A node that left by itself stays in `node ls` as Down until removed; stale Down managers
  count against quorum.
- Labels live on the node object (`docker node update --label-add`).

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: `docker node ls` columns and values Ready, Active/Pause/Drain, Leader/Reachable; `--filter` keys id, label, node.label, membership, name, role; `--format` fields `.Hostname`, `.ManagerStatus`, `.EngineVersion`; `docker node ps` options and the `desired-state` filter; `docker node rm` only removes Down nodes, `--force` for inaccessible ones; demote a manager before forcibly removing it. Removed: Unknown/Disconnected status values, `Status.Message` text, node-ID-on-rebuild and label re-add claims.
Method: documentation only; no commands were run.
