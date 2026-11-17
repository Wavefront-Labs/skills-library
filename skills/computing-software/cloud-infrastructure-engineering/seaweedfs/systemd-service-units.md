---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.systemd-service-units
name: systemd-service-units
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [linux, service, enable, systemd, service-unit, autostart]
level: intro
status: docs-checked
description: "Run weed master, volume and filer as systemd services: unit file layout, mount ordering with After and a start delay, and a filer working directory."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Server-Startup-via-Systemd
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# systemd service units

Create one unit per role in /etc/systemd/system/, then `systemctl start` and `systemctl enable` it.

Master:
```
[Unit]
Description=SeaweedFS Server
After=network.target
[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/weed master -ip=192.168.1.31
WorkingDirectory=/usr/local/bin
SyslogIdentifier=seaweedfs-master
[Install]
WantedBy=multi-user.target
```
Volume: `ExecStart=/usr/local/bin/weed volume -dir="/path/to/data"`. If the data directory is on a separate mount, add that mount unit to `After=` and optionally `ExecStartPre=/bin/sleep 30`.

Filer: `ExecStart=/usr/local/bin/weed filer`, plus `ExecReload=/bin/kill -HUP $MAINPID`. The page's example sets `WorkingDirectory` to a directory on its HDD that holds a `filer.toml` with the desired configuration. The page's volume and filer units also use `ExecStartPre=/bin/sleep 30` to wait for the mount.

The page's units all use `Type=simple`, `User=root`, `Group=root` and `WantedBy=multi-user.target`; the service files are named seaweedmaster, seaweedvolume and seaweedfiler. Its volume example uses `After=network.target media-jmn-LENOVO.mount`; the mount ordering is not needed if the data directory is not a separate mount.

Commands: `systemctl start seaweedmaster.service`, `systemctl enable seaweedmaster.service` (same for the volume and filer units).

## Checked

2026-11-08. Confirmed against the Server Startup via Systemd wiki page, which calls it a sample setup. Removed the unsupported "systemctl status / master UI" verification and the claim that filer.toml is "read from" the working directory (the page only shows it placed there); added the naming and ordering details.

Method: documentation only; no commands were run.
