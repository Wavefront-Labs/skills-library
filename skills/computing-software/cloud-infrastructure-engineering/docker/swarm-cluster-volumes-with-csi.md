---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-cluster-volumes-with-csi
name: swarm-cluster-volumes-with-csi
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-swarm, cluster-volumes, csi-plugin, volume-plugin, stateful, swarm-service]
level: sme
status: docs-checked
description: "Use Swarm cluster volumes backed by CSI plugins (Engine 23+): installing a CSI plugin, volume create flags (scope, sharing, topology, size), mount type=cluster and lifecycle."
sources: ["https://docs.docker.com/reference/cli/docker/volume/create/", "https://github.com/moby/moby/blob/master/docs/cluster_volumes.md", "https://docs.docker.com/reference/cli/docker/service/create/", "https://docs.docker.com/reference/cli/docker/volume/update/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swarm cluster volumes with CSI

Swarm services historically used node-local volumes, so a rescheduled task lost its data.
Cluster volumes let Swarm use Container Storage Interface (CSI) plugins, accessed through the
Docker managed plugin system, to provide storage to services.

## Prerequisites
- A CSI plugin available as a **Docker managed plugin**. Docs: install it on all manager nodes
  (a manager without it can break volume handling after a leadership change); workers report
  their active plugins, so install it only on the nodes that need access to its volumes.
```bash
docker plugin install --alias mycsi --grant-all-permissions <plugin-image>
docker plugin ls
```

## Create a cluster volume
```bash
docker volume create --driver mycsi \
  --type mount \
  --sharing onewriter \
  --scope single \
  --required-bytes 10G --limit-bytes 20G \
  --availability active \
  --group pg \
  --topology-required region=eu-west-1 \
  pgdata
docker volume ls --cluster
docker volume inspect pgdata
```
Run these on a swarm manager. Flags: `--type mount|block` (default `block`),
`--sharing none|readonly|onewriter|all` (default `none`), `--scope single|multi` (default
`single`), `--secret` for driver secrets, `--group` to place related volumes together,
`--availability active|pause|drain` (default `active`), `--topology-required` and
`--topology-preferred`, `--required-bytes`, `--limit-bytes`.

## Use in a service
```bash
docker service create --name pg \
  --mount type=cluster,src=pgdata,dst=/var/lib/postgresql/data \
  --replicas 1 postgres:17
```
A service can also select any volume in a group with `src=group:<group-name>`; volumes in a
group must be interchangeable and are created ahead of time.

## Lifecycle
- `docker volume ls --cluster` shows status such as `pending creation`, `created` and
  `in use (N nodes)`.
- `docker volume update --availability pause|drain pgdata`: `pause` stops use by new services
  while existing tasks continue; `drain` also stops and reschedules running tasks.
- A cluster volume can be removed only when its availability is `drain` and it is fully
  unpublished from all nodes.

## Gotchas
- The documentation lists unsupported CSI features: snapshots, cloning and volume expansion.
- Test failover (node down, task moved) before trusting a plugin with production data.
- If no CSI plugin fits, alternatives include NFS via the `local` driver or pinning stateful
  services to a node with placement constraints.

## Checked

Date: 2026-10-24. Documentation release: `docker volume create`/`update` references and moby cluster_volumes.md (docker/cli, moby/moby main).
Confirmed: cluster volume flags and their defaults (`--type`, `--sharing`, `--scope`, `--availability`, `--group`, topology
and size flags), `docker volume ls --cluster`, `--mount type=cluster` and `src=group:<name>`, availability semantics
(`active`, `pause`, `drain`), the removal precondition, plugin install requirements (managers vs workers) and unsupported
features. Removed: the Engine 23.0 gate, named third-party drivers, the lifecycle state list beyond what the docs show, the
stack-file form, and the onewriter/start-first claim, none of which the documentation states.

Method: documentation only; no commands were run.
