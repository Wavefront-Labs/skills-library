---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-volume-and-port-examples
name: quadlet-volume-and-port-examples
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, volume-example, publishport, nginx, persistent-volume, mydata, container-unit]
level: intro
status: docs-checked
description: "Follow the Podman basic-usage examples for a named volume unit, a container mounting it with Volume=mydata.volume:/data, and publishing 8080:80 for nginx."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-quadlet-basic-usage.7.html
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: persist data and expose a port using Quadlet files.

Volume: `mydata.volume` containing `[Volume]`, `VolumeName=mydata` and `Label=purpose=demo`. Place it as for any Quadlet, run `daemon-reload`, then create the volume with `systemctl --user start mydata-volume.service` (`systemctl start ...` for rootful).

Use it: `with-volume.container` has `Image=alpine`, `Exec=sh -c "ls /data && echo Hello > /data/hello.txt"` and `Volume=mydata.volume:/data`, plus `[Install] WantedBy=multi-user.target`. The first start does not list `hello.txt` in `systemctl status` because it has not been created yet; on the second start the output contains `hello.txt`, showing the volume persists.

Expose a port: `webserver.container` with `Image=nginx:alpine` and `PublishPort=8080:80`. After `daemon-reload` and `systemctl --user start webserver.service` (or the rootful equivalent) visit `http://localhost:8080`.

Tip from the page: to start a container on system boot use `[Install]` with `WantedBy=multi-user.target`.


What each file does in the generated service: `mydata.volume` becomes `mydata-volume.service`, a oneshot that creates the volume named `mydata` (because the unit sets `VolumeName=mydata`; otherwise it would be `systemd-mydata`). `with-volume.container` references `mydata.volume`, so Quadlet adds a dependency on that service. In `webserver.container`, `PublishPort=8080:80` is `hostPort:containerPort`, mapped to `--publish 8080:80`.

## Checked

2026-11-03. Read against the official page text (podman-quadlet-basic-usage.7, podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
