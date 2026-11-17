---
id: computing-software.collaboration-platform-administration.vikunja.systemd-dedicated-user-sandbox
name: systemd-dedicated-user-sandbox
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, systemd-hardening, dedicated-service-user, protectsystem-strict, readwritepaths, data-path-pinning]
level: advanced
status: docs-checked
description: "Run the packaged Vikunja service as a dedicated vikunja user with systemd sandboxing, pinning data paths first so the database is not silently recreated."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/systemd-hardening.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Create the user: `sudo useradd --system --user-group --home-dir /var/lib/vikunja --shell /usr/sbin/nologin vikunja`; create `/var/lib/vikunja` (and `/var/log/vikunja` if logging to files) owned by it. Make the config readable only by it: `chown root:vikunja /etc/vikunja/config.yml`, `chmod 640`.
2. Pin paths before restarting, or Vikunja starts with an empty database. Relative paths resolve against `service.rootpath`, which follows `WorkingDirectory`. In `config.yml` set `database.path: "/var/lib/vikunja/vikunja.db"` and `files.basepath: "/var/lib/vikunja/files"`, stop the service and move `/opt/vikunja/vikunja.db*` and `/opt/vikunja/files` across (MySQL or PostgreSQL: files only), then `chown -R vikunja:vikunja`.
3. `sudo systemctl edit vikunja.service` and set `User=vikunja`, `Group=vikunja`, `WorkingDirectory=/var/lib/vikunja`, `ExecStart`, `Environment=VIKUNJA_CONFIG=/etc/vikunja/config.yml`, `LimitNOFILE=65536`, `NoNewPrivileges=true`, `ProtectHome=true`, `PrivateTmp=true`, `ProtectSystem=strict`, `ReadWritePaths=/var/lib/vikunja` (add files and log dirs).
4. Ports below 1024 need `AmbientCapabilities` and `CapabilityBoundingSet` of `CAP_NET_BIND_SERVICE`.
5. `systemctl daemon-reload`, restart, check `ps -u vikunja -f` and `journalctl -u vikunja.service -e`.

Do not use `ProtectHome` while the service runs as root (PostgreSQL `sslmode=require` fails). Run CLI as `sudo -u vikunja vikunja migrate`; as root it leaves root-owned files, including the SQLite WAL, and the service then fails.

## Checked

2026-11-04. Confirmed against the Vikunja systemd hardening page (setup/systemd-hardening): useradd command, directories and config permissions, the empty-database warning and path pinning, data move commands, the unit settings, ProtectHome caution, capabilities for low ports, daemon-reload, verification commands and the CLI-as-service-user advice. Nothing removed.

Method: documentation only; no commands were run.
