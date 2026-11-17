---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-ports-and-networks
name: quadlet-container-ports-and-networks
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, publishport, network, networkalias, exposehostport, container-network, dns]
level: practitioner
status: docs-checked
description: "Publish ports and attach networks in Quadlet containers: PublishPort forms, random host ports, Network= with .network and .container references, NetworkAlias and ExposeHostPort."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose and connect Quadlet containers.

`PublishPort=` is `--publish`: forms are `ip:hostPort:containerPort`, `ip::containerPort`, `hostPort:containerPort` or `containerPort`, with equal host and container port counts for a range such as `50-59`. Add `/tcp` or `/udp` at the end; `sctp` is for rootful containers only. An IP of `0.0.0.0` or none binds all IPv4 addresses; use `[::]` for IPv6. Omitting the host port makes Podman choose one, possibly different each time the service starts, so look it up with `podman port`. The key can be repeated.

`ExposeHostPort=` is `--expose` for a port or range from host to container.

`Network=` takes the `--network` format, such as `host` or `none`. If the name ends with `.network`, the network `systemd-$name` is used and the service depends on `$name-network.service`; a `$name.network` Quadlet file can create it (the file must exist). If it ends with `.container`, the container reuses the network stack of the container created by `$name.container` and depends on `$name.service`. The key can be listed multiple times.

`NetworkAlias=` adds a network-scoped alias: setting `NetworkAlias=web` on several containers makes a DNS query for `web` resolve to all of them. Other keys: `IP=`, `IP6=`, `DNS=`, `DNSOption=`, `DNSSearch=`, `AddHost=`, `HostName=`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
