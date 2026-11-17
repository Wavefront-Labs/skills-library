---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-install-section-and-service-type
name: quadlet-install-section-and-service-type
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, install-section, wantedby, service-type, oneshot, remainafterexit, boot]
level: practitioner
status: docs-checked
description: "Start Quadlet units on boot with [Install], learn which keys work, the default Type per unit kind, and how oneshot with RemainAfterExit behaves."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enable a Quadlet at boot and choose the right service type.

Generated services are transient to systemd, so `systemctl enable` does not work on them. Instead the generator applies the `[Install]` section itself during generation, as enable would. For example:

```
[Install]
WantedBy=default.target
```

Only `Alias`, `WantedBy`, `RequiredBy` and `UpheldBy` are supported. The section can live in the main file or in a drop-in, which lets you install a non-enabled unit now and enable it later by adding the drop-in.

Default `Type`: you normally do not set it. Quadlet uses `notify` for `.container` and `.kube`, `forking` for `.pod`, and `oneshot` for `.volume`, `.network`, `.build`, `.image` and `.artifact`. You may set `Type=oneshot` on `.container` and `.kube` when no container is expected to be running after `podman` exits, for example an image that exits after its entrypoint, or a `.kube` file with only PVCs.

With `Type=oneshot` set `RemainAfterExit=yes` to avoid the state becoming `inactive (dead)`. When a timer activates the service, that setting leaves the job "started" and blocks later activations.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
