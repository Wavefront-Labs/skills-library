---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-implicit-network-dependencies
name: quadlet-implicit-network-dependencies
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, network-online, defaultdependencies, after-wants, user-units, systemd, podman-user-wait-network-online]
level: advanced
status: docs-checked
description: "Understand the network-online ordering Quadlet adds to units, the user-level podman-user-wait-network-online.service workaround, and DefaultDependencies=false."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know why generated units wait for the network and how to stop it.

Quadlet adds `After=` and `Wants=` properties on `network-online.target` for root units, and on `podman-user-wait-network-online.service` for user units. This ensures the network is reachable if an image must be pulled, and by the time the container starts.

The special user unit exists because user units cannot wait for system (root) units, so `network-online.target` does nothing there and is ignored. Because that caused many issues, Podman ships its own unit that checks `systemctl is-active network-online.target`.

Disable the behaviour by adding `DefaultDependencies=false` in the `[Quadlet]` section. The page warns that the systemd `[Unit]` section has an option of the same name with a different meaning, so put it under `[Quadlet]`:

```
[Quadlet]
DefaultDependencies=false
```


In short: root units get `After=` and `Wants=` on `network-online.target`; user units get the same pair against `podman-user-wait-network-online.service`. Disabling it removes the guarantee that the network is reachable when an image has to be pulled and when the container starts, so do it only when neither matters.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
