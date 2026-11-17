---
id: computing-software.devops-ci-cd.semaphore-ui.run-as-systemd-service
name: run-as-systemd-service
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [systemd, service, linux, installation, semaphore-ui]
level: practitioner
status: docs-checked
description: "Create a systemd unit so the Semaphore server starts at boot and restarts on failure."
sources:
  - https://semaphoreui.com/docs/admin-guide/installation/binary-file
  - https://semaphoreui.com/docs/admin-guide/security/encryption
  - https://semaphoreui.com/docs/admin-guide/configuration/env-vars
  - https://semaphoreui.com/docs/admin-guide/logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run Semaphore as a systemd service

Goal: keep the server running after a binary or package install.

Create the unit (replace the two paths with your binary and config file):

```ini
[Unit]
Description=Semaphore Ansible
Documentation=https://github.com/semaphoreui/semaphore
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/path/to/semaphore server --config=/path/to/config.json
SyslogIdentifier=semaphore
Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

Save it as `/etc/systemd/system/semaphore.service`, then:

```bash
sudo systemctl daemon-reload
sudo systemctl start semaphore
sudo systemctl status semaphore
sudo systemctl enable semaphore
```

`ExecReload` sends SIGHUP; on Unix `kill -HUP <pid>` forces an immediate reload of the encryption keys without a restart. Semaphore writes server logs to stdout and does not log to files; under systemd follow them with `journalctl -u semaphore.service -f`.

Gotchas:
- Environment set in the unit's `[Service]` section applies to the Semaphore server itself but not to `git`; list names in `forwarded_env_vars` (or set `env_vars`) so app and git processes receive them.

Verify: `sudo systemctl status semaphore`, as in the page.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository: admin-guide/installation/binary-file.md (its Tabs imports are the only includes), admin-guide/logs.md (first 40 lines, the server-log section; the rest was not read), admin-guide/configuration/env-vars.md, and admin-guide/security/encryption.md only from line 150 to 190 (the SIGHUP section), not the whole page; admin-guide/installation_manually.md was also read in full for the unit file variants. Confirmed: the unit file text, the install commands, SIGHUP reload on Unix, stdout logging with the journalctl command, and the forwarded_env_vars rule. Removed: the heredoc quoting advice (the page writes the file with an unquoted heredoc and does not discuss it) and the see-the-proxy-skill pointer.
Method: documentation only; no commands were run.
