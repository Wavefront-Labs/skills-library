---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-init-join-tokens-and-manager-quorum
name: swarm-init-join-tokens-and-manager-quorum
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm, docker-swarm, swarm-manager, swarm-quorum, advertise-addr, listen-addr, join-token, token-rotate, node-promote, node-demote, node-drain, node-labels, node-availability]
level: advanced
description: "Bootstrap a Swarm with correct advertise/listen/data-path addresses, manage and rotate join tokens, keep an odd manager quorum, and drain and label nodes for maintenance."
sources: ["https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/", "https://docs.docker.com/engine/swarm/join-nodes/", "https://docs.docker.com/engine/swarm/admin_guide/", "https://docs.docker.com/engine/swarm/manage-nodes/", "https://docs.docker.com/reference/cli/docker/swarm/init/", "https://docs.docker.com/reference/cli/docker/node/update/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Swarm init, join tokens and manager quorum

## Init with explicit addresses
```sh
docker swarm init --advertise-addr 10.0.1.11 --listen-addr 10.0.1.11:2377 \
  --data-path-addr 10.0.2.11 --default-addr-pool 10.20.0.0/16 --default-addr-pool-mask-length 24
```
- `--advertise-addr`: address other nodes use to reach this manager (must be specified when the
  host has several IP addresses; with a single IP it is detected).
- `--listen-addr`: where the manager listens for cluster management (default `0.0.0.0:2377`).
- `--data-path-addr`: interface for overlay (VXLAN) data traffic - separate control and data.
- Address pools must not overlap VPC/VPN ranges.

## Join tokens
```sh
docker swarm join-token worker          # prints the full join command
docker swarm join-token -q manager      # token only
docker swarm join --token SWMTKN-1-... --advertise-addr 10.0.1.21 10.0.1.11:2377
docker swarm join-token --rotate worker # invalidates the old worker token
```
Tokens embed the CA hash; a leaked **manager** token lets anyone join as a manager - rotate
after use or exposure. Rotation doesn't affect already-joined nodes.

## Quorum
Raft needs a majority of managers: with N managers, tolerate (N-1)/2 failures.
| Managers | Tolerates |
|---|---|
| 1 | 0 |
| 3 | 1 |
| 5 | 2 |
| 7 | 3 |
Use 3 or 5, spread across failure domains; even numbers add no tolerance. Losing quorum
freezes the control plane (existing tasks keep running, no scheduling/updates).
```sh
docker node promote worker-3
docker node demote manager-4          # demote before removing a manager
docker node ls                        # MANAGER STATUS: Leader / Reachable / Unreachable
```
Make managers manager-only: `docker node update --availability drain manager-1`.

## Maintenance and labels
```sh
docker node update --availability drain worker-2     # reschedule its tasks elsewhere
docker node update --availability pause worker-2     # keep tasks, no new ones
docker node update --availability active worker-2
docker node update --label-add zone=eu-1a --label-add disk=ssd worker-2
docker node inspect worker-2 -f '{{json .Spec.Labels}}'
docker node rm --force dead-node                      # after it's gone for good
```
Node labels (set by managers) drive placement constraints `node.labels.zone==eu-1a`; engine
labels are set in the daemon configuration and match `engine.labels.*`.

## Verify
`docker node ls` shows the expected managers Reachable and one Leader.

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: `--advertise-addr`, `--listen-addr` (default 0.0.0.0:2377), `--data-path-addr`, `--default-addr-pool` and `--default-addr-pool-mask-length` (default 24); `join-token --quiet` and `--rotate`; tokens are used only at join time; odd manager count recommended and more than two; Leader/Reachable in MANAGER STATUS; `node update --availability active|pause|drain`, `--label-add`; `node rm --force`; promote/demote before removing a manager. Removed: reliability ranking of labels and the `docker info` Swarm format fields.
Method: documentation only; no commands were run.
