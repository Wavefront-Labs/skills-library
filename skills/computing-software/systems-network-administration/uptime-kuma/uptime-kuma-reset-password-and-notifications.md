---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-reset-password-and-notifications
name: uptime-kuma-reset-password-and-notifications
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [reset-password, npm-run-reset-password, notification-providers, apprise, admin-recovery]
level: intro
status: docs-checked
description: "Reset a lost Uptime Kuma admin password from the CLI and know how notification providers and Apprise fit in."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Reset-Password-via-CLI", "https://github.com/louislam/uptime-kuma/wiki/Notification-Methods"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reset password and notification providers

Lost the admin password? Run the reset script on the host that holds the data directory.

Docker:
```bash
docker exec -it <container name> bash
npm run reset-password
```

Non-Docker: `cd` to the Uptime Kuma working directory and run `npm run reset-password`.

Notifications: Uptime Kuma supports many services natively; the authoritative list is the `server/notification-providers` directory of the repository. For anything not covered, it integrates with Apprise, which supports many more services (see the Apprise wiki). To send notifications through a proxy set `NOTIFICATION_PROXY` (2.0.0) with a full URL such as `http://proxy.example.com:8080`.

Email (SMTP) templates in v2 use LiquidJS with case-sensitive variables (`name`, `msg`, `status`, `heartbeatJSON`, `monitorJSON`, `hostnameOrUrl`).

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Reset Password via CLI and Notification Methods pages, plus Environment Variables (NOTIFICATION_PROXY) and Migration From v1 To v2 (LiquidJS variables). Removed: The prompts claim, the advice to prefer maintenance windows over disabling providers, and the generic verify line.

Method: documentation only; no commands were run.
