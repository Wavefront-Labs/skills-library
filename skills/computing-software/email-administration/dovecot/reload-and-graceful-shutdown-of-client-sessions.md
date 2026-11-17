---
id: computing-software.email-administration.dovecot.reload-and-graceful-shutdown-of-client-sessions
name: reload-and-graceful-shutdown-of-client-sessions
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-reload, service-shutdown-clients-timeout, kick-timeout, doveadm-stop, systemd, process-status]
level: practitioner
status: docs-checked
description: "Reload config without dropping sessions using service_shutdown_clients_timeout, understand preserved old-generation processes and clean shutdown."
sources:
  - https://doc.dovecot.org/main/core/admin/running.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start Dovecot by running `dovecot` as root; startup problems print to the terminal and may also reach the error log. Reload with `doveadm reload`. Internal processes (config, stats, auth, dict) are always replaced. For processes serving clients, `service_shutdown_clients_timeout` decides:
- `0` (default): clients are disconnected immediately.
- a time: sessions keep running up to that long.
- `infinite`: never disconnected.

This lets you adopt a new TLS certificate without kicking anyone: new connections use it at once while open sessions run for at most the timeout (the page example allows four hours). It can also be set per service, for example in `service pop3`. When the time is up, remaining clients are disconnected even mid-command, and logins in progress abort. Both processes of a session need the timeout, because with TLS the login process keeps proxying, so killing either imap or imap-login ends the session. On a proxy there are no local imap processes.

`doveadm reload --kick-timeout` overrides the timeout for all services in one reload, including processes preserved by earlier reloads; `--kick-timeout 0` disconnects every preserved client.

`doveadm process status` shows preserved processes: the generation column rises per reload, and `kill_time` shows when the master disconnects them. They keep the old configuration, including passdb, userdb and mail settings, except hibernated IMAP sessions, which resume on new config.

A TERM signal to the master (easily sent with `doveadm stop`) does a clean shutdown, and the same timeout controls how long existing IMAP and POP3 sessions survive without a master; nobody is left to escalate to SIGKILL, so the processes stop themselves at the deadline. Under systemd the page says to set `KillMode=none` and `ExecStop=/usr/bin/doveadm stop` so systemd does not kill processes on restart.

## Checked
2026-11-09. Read the whole Dovecot "Running Dovecot" page (doc.dovecot.org/main/core/admin/running.html; the old main/admin/running.html URL is a script shell with no text, so the source was replaced) and confirmed every statement above, including the timeout values, `--kick-timeout`, `doveadm process status` columns and the systemd settings.

Method: documentation only; no commands were run.
