---
id: computing-software.messaging-and-integration.ntfy.cli-systemd-service
name: cli-systemd-service
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, systemd, ntfy-client, service, user-service]
level: practitioner
status: docs-checked
description: "Run the ntfy client as a systemd system or user service, and which one can show desktop notifications."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ntfy-client as a service

Neither service is enabled or started by default. Both are named `ntfy-client`.

## System service

Runs as the `ntfy` user at boot; config `/etc/ntfy/client.yml`.

```
sudo systemctl enable ntfy-client
sudo systemctl restart ntfy-client
```

It cannot run commands in your X session.

## User service

Runs at desktop login; config `~/.config/ntfy/client.yml`. It can use `notify-send` and your home directory (for example `gnome-calculator`).

```
systemctl --user enable ntfy-client
systemctl --user restart ntfy-client
```

## Choosing

- Desktop pop-ups or GUI programs: user service.
- The system service runs as `ntfy`, so normal Linux permission limits apply.

Unit files live in the repo under `client/ntfy-client.service` and `client/user/ntfy-client.service`.

## Checked

2026-11-04. Confirmed against the ntfy subscribe CLI page (Using the systemd service): service name, system versus user behaviour, config paths, enable/restart commands, not enabled by default, unit file links. Removed: a headless-automation recommendation and the status-check Verify step.
Method: documentation only; no commands were run.
