---
id: computing-software.cloud-infrastructure-engineering.garage.systemd-service-unit
name: systemd-service-unit
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [systemd, dynamic-user, garage-service, journalctl]
level: practitioner
status: docs-checked
description: "Run Garage under systemd with DynamicUser hardening, which requires specific metadata and data paths."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/cookbook/systemd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The cookbook unit assumes the binary at `/usr/local/bin/garage` and config at `/etc/garage.toml`. Create `/etc/systemd/system/garage.service`:

`[Unit]` with `After=network-online.target` and `Wants=network-online.target`; `[Service]` with `Environment='RUST_LOG=garage=info' 'RUST_BACKTRACE=1'`, `ExecStart=/usr/local/bin/garage server`, `StateDirectory=garage`, `DynamicUser=true`, `ProtectHome=true`, `NoNewPrivileges=true`, `LimitNOFILE=42000`; and `[Install]` with `WantedBy=multi-user.target`.

For `DynamicUser` to work, `garage.toml` must use `metadata_dir=/var/lib/garage/meta` and `data_dir=/var/lib/garage/data`; on the host, data lives in `/var/lib/private/garage`. If `/var/lib/garage` already exists before the first start, the service might not start correctly.

Hardening effect: unprivileged dynamic user, no access to `/home`, `/root` or `/run/user`, rest of the filesystem read-only, only the state path writable, no new privileges.

Start and enable with `sudo systemctl start garage` and `sudo systemctl enable garage`; check with `systemctl status garage` and `sudo journalctl -u garage`. Run `systemctl daemon-reload` after editing the unit.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Starting Garage with systemd. Confirmed on the systemd cookbook page: file assumptions, the unit contents, the path requirements and `/var/lib/private/garage`, the hardening effects, start, enable, status, journalctl and daemon-reload. Removed: the 'directive notes' paragraph (purposes of `LimitNOFILE` and `StateDirectory` are not stated on the page).

Method: documentation only; no commands were run.
