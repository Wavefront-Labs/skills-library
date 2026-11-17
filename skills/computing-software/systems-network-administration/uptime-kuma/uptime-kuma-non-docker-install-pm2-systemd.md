---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-non-docker-install-pm2-systemd
name: uptime-kuma-non-docker-install-pm2-systemd
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [pm2, systemd-unit, nodejs, non-docker, openrc, uptime-kuma-service, npm-run-setup]
level: practitioner
status: docs-checked
description: "Install Uptime Kuma from Git with Node.js and keep it running with pm2, a systemd unit or an OpenRC script."
sources: ["https://github.com/louislam/uptime-kuma/wiki/%F0%9F%94%A7-How-to-Install", "https://github.com/louislam/uptime-kuma/wiki/Systemd-Unit-File", "https://github.com/louislam/uptime-kuma/wiki/OpenRC-Script"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Non-Docker install and service management

Requirements: a major Linux distribution or Windows 10 x64 / Server 2012 R2 or later, Node.js 20.4 or newer, Git, and pm2 for background running (Replit and Heroku are not supported).

```bash
git clone https://github.com/louislam/uptime-kuma.git
cd uptime-kuma
npm run setup
node server/server.js                         # try it
npm install pm2 -g && pm2 install pm2-logrotate
pm2 start server/server.js --name uptime-kuma
pm2 save && pm2 startup                       # start on boot
```

Listens on `http://localhost:3001`. Non-Docker settings can go in a `.env` file at the repo root (`UPTIME_KUMA_HOST=127.0.0.1`, `UPTIME_KUMA_PORT=8080`) or as server arguments (`node server/server.js --host=127.0.0.1 --port=8080`).

systemd alternative: unit with `User=uptime`, `WorkingDirectory=/path/to/uptime-kuma`, `ExecStart=/usr/bin/npm run start-server`, `Restart=on-failure`, `WantedBy=multi-user.target`, saved as `/etc/systemd/system/uptime-kuma.service`. Adjust ExecStart if npm lives elsewhere. Then `systemctl daemon-reload && systemctl enable --now uptime-kuma`.

OpenRC (Alpine, postmarketOS, Gentoo, Artix): `/etc/init.d/uptime-kuma` using `command=/usr/bin/node`, `command_args="$directory/server/server.js"`, a dedicated `uptime-kuma` user and group, data under `$directory/data`; `chmod 755` it, then `rc-service uptime-kuma start` and `rc-update add uptime-kuma`.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: How to Install, Systemd Unit File and OpenRC Script pages. Removed: The generic verify line.

Method: documentation only; no commands were run.
