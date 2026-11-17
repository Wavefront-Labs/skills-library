---
id: computing-software.cloud-infrastructure-engineering.zot.systemd-install-on-linux
name: systemd-install-on-linux
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, systemd, bare-metal-install, healthcheck, socket-activation, service-user]
level: practitioner
status: docs-checked
description: "Install Zot on Linux as a systemd service: binary, htpasswd, unit file settings, service user, health checks, socket activation and verification."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/install-guides/install-guide-linux.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Get the binary: `sudo wget -O /usr/bin/zot <release-url>/zot-linux-amd64`, then `chmod +x` and `chown root:root`.
2. Create `/etc/zot/config.json`.
3. Local users: `htpasswd -bnB myUserName myPassword > /etc/zot/htpasswd` (use `>>` to add more).
4. Unit `/etc/systemd/system/zot.service`: `Type=notify`, `NotifyAccess=main`, `TimeoutStartSec=5min`, `ExecStart=/usr/bin/zot serve /etc/zot/config.json`, `Restart=on-failure`, `User=zot`, `Group=zot`, `LimitNOFILE=500000`, `MemoryHigh=30G`, `MemoryMax=32G`, `WantedBy=multi-user.target`. For older binaries use `Type=simple` without `NotifyAccess` and `TimeoutStartSec`.
5. Service user and dirs: create user `zot` (no home, no login), `/data/zot` and `/var/log/zot` owned by `zot:zot`, and `chown -R root:root /etc/zot/`.
6. Start:
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable zot
   sudo systemctl start zot
   sudo -u zot zot verify /etc/zot/config.json
   sudo systemctl status zot
   ```

Health checks: `zot healthcheck /etc/zot/config.json`, `zot healthcheck --endpoint livez /etc/zot/config.json`, `zot healthcheck --url https://registry.example.com/startupz --timeout 5s`.

Socket activation: `zot.socket` with `ListenStream=443`, `NoDelay=true`, `WantedBy=sockets.target`; add `Sockets=zot.socket` to the service, `daemon-reload`, `systemctl enable --now zot.socket`.

Test TLS afterwards with a service such as the Qualys SSL Server Test.

## Checked

2026-11-04. Confirmed against the zot bare-metal Linux install guide: binary location, service unit, Type=notify behaviour, healthcheck endpoints, socket activation and verify command.

Method: documentation only; no commands were run.
