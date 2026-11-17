---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-pod-unit
name: quadlet-pod-unit
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, pod-unit, exitpolicy, podname, restart, pod-create, publishport]
level: practitioner
status: docs-checked
description: "Define a Podman pod as a Quadlet .pod: naming, PodName, ExitPolicy stop versus continue, the Restart=on-failure default trap, and pod-level network, ports and IPs."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create a pod that containers can join and that restarts the way you expect.

A `.pod` file has a `[Pod]` section. The generated service runs `ExecStartPre=podman pod create ...`. `$name.pod` creates the unit `$name-pod.service` and a Podman pod `systemd-$name`; `PodName=` overrides the pod name. Keys map to `podman pod create` options: `AddHost`, `DNS`, `DNSOption`, `DNSSearch`, `HostName`, `IP`, `IP6`, `Label`, `Network`, `NetworkAlias`, `PublishPort`, `ShmSize`, `StopTimeout` (`--time`), `SubUIDMap`, `SubGIDMap`, `UIDMap`, `GIDMap`, `UserNS`, `Volume`, `ServiceName`, and `PodmanArgs` such as `--cpus=2`.

Restart trap: the generated service defaults to `Restart=on-failure`. `ExitPolicy=stop` is the Quadlet default, so when all containers stop the pod exits cleanly with code 0, and `on-failure` does not restart it. To restart the pod when containers exit, set `Restart=always` in the `[Service]` section of the `.pod` file. To keep the pod alive after its last container exits, use `ExitPolicy=continue`.

Static addresses: `IP=` takes an IPv4 such as 10.88.64.128 and `IP6=` an IPv6 such as fd46:db93:aa76:ac37::10. Containers join with `Pod=name.pod` in their `[Container]` section.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
