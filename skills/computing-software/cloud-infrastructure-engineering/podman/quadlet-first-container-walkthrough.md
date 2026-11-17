---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-first-container-walkthrough
name: quadlet-first-container-walkthrough
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, walkthrough, hello-container, daemon-reload, journalctl, rootless, systemctl]
level: intro
status: docs-checked
description: "Run a first Quadlet container end to end: write hello.container, copy it into the rootless or rootful path, daemon-reload, start the service and read journal output."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-quadlet-basic-usage.7.html
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a Quadlet from file to running service.

Create `hello.container`:

```ini
[Unit]
Description=Hello Alpine Container

[Container]
Image=alpine
Exec=echo Hello from Quadlet!

[Install]
WantedBy=multi-user.target
```

Place it. Rootless: `mkdir -p ~/.config/containers/systemd` then `cp hello.container ~/.config/containers/systemd/`. Rootful: `sudo cp hello.container /etc/containers/systemd/`.

Reload and start. Rootless: `systemctl --user daemon-reload` then `systemctl --user start hello.service`. Rootful: `sudo systemctl daemon-reload` then `sudo systemctl start hello.service`. You cannot `systemctl enable` a Quadlet service because it is generated; the `[Install]` section handles boot behaviour.

Check the logs with `journalctl --user -u hello.service` (rootless) or `journalctl -u hello.service`. You should see `Hello from Quadlet!`, showing that the container ran the echo and exited.

If `systemctl` cannot find `foo.service`, the page says it usually means a syntax error in your Quadlet file; find details with `systemd-analyze --user --generators=true verify foo.service`.


The example works because Quadlet maps `Image=` and `Exec=` onto a `podman run` of the alpine image in the generated `ExecStart`, and the default service type for a container unit is `notify`. The `Description=` in `[Unit]` is passed to systemd untouched.

## Checked

2026-11-03. Read against the official page text (podman-quadlet-basic-usage.7, podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
