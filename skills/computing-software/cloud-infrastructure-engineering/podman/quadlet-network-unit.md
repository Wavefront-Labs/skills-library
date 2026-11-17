---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-network-unit
name: quadlet-network-unit
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, network-unit, subnet, gateway, macvlan, ipam-driver, networkdeleteonstop]
level: practitioner
status: docs-checked
description: "Pre-create Podman networks with a Quadlet .network: naming, driver, subnet, gateway, IPAM, internal, IPv6, update-by-removal rule and NetworkDeleteOnStop."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control network creation options for containers.

A `.network` file's `[Network]` section creates a one-time service that ensures the network exists, creating it if needed. `$NAME.network` creates network `systemd-$NAME` through the service `$NAME-network.service`; `NetworkName=` overrides the name, and `ServiceName=` the service. Containers reference it with `Network=name.network`.

Updating: to change network parameters you must first remove the Podman network manually, then restart the service. `NetworkDeleteOnStop=true` (default false) deletes the network when the service stops.

Keys (matching `podman network create`): `Driver=` (default `bridge`; `macvlan` and `ipvlan` also supported), `Subnet=` (CIDR, repeatable), `Gateway=` (requires a subnet), `IPRange=` (CIDR or `<startIP>-<endIP>`, requires a subnet), `IPAMDriver=` (`host-local`, `dhcp`, `none`), `Internal=true` restricts external access, `IPv6=true` enables dual stack, `DisableDNS=true`, `DNS=`, `Options=` for driver options, `Label=`.

`InterfaceName=` maps to `--interface-name`: for `bridge` it is the bridge interface name; for `macvlan` and `ipvlan` it is the parent host device (same as `--opt parent=...`).


Example values: `Subnet=` in CIDR form (repeatable), `Gateway=192.168.55.3`, `IPRange=192.168.55.128/25`, `DNS=192.168.55.1`, `Driver=bridge`, `InterfaceName=enp1`, `IPAMDriver=dhcp`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
