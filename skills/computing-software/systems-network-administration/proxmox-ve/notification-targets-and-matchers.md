---
id: computing-software.systems-network-administration.proxmox-ve.notification-targets-and-matchers
name: notification-targets-and-matchers
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [notifications, matcher, sendmail, gotify]
level: practitioner
status: docs-checked
description: "Route Proxmox VE events to email or Gotify with notification targets and matchers, and configure Postfix relay for sendmail."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-notifications.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Proxmox VE emits notification events for storage replication failures, node fencing, finished or failed backups and more. Each event carries metadata such as timestamp, severity, type and extra fields. Matchers route events to targets and can use match rules on that metadata. Targets are destinations: Sendmail, SMTP, or Gotify.

Settings are in the GUI under Datacenter, Notifications, and stored in `/etc/pve/notifications.cfg`. Secrets such as passwords and tokens are stored in `/etc/pve/priv/notifications.cfg`, readable only by root.

Sendmail target:

- Sends mail through the `sendmail` binary, which is provided by Postfix on standard installs. Postfix may need an external mail relay (smart host). If delivery fails, check the system logs for Postfix messages.
- Options include `mailto` (address, repeatable), `mailto-user` (looks up the address from the user's settings), `author` (default Proxmox VE) and `from-address`.
- `from-address` falls back to `email_from` in `datacenter.cfg`, then to `root@$hostname`.
- A user without an email address gets no mail. For `root@pam` it is the address entered during installation.

SMTP target: `mode` selects insecure, starttls or tls (default tls). An unset port defaults to 25 (insecure), 465 (tls) or 587 (starttls).

Matchers are named sections such as `matcher: always-matches`, and examples in the docs include backup-failures and cluster-failures. Default templates are in `/usr/share/pve-manager/templates/default/`, and overrides go in `/etc/pve/notification-templates/default/`.

## Checked

2026-11-09. Compared with the sendmail, SMTP, matcher and template sections of https://pve.proxmox.com/pve-docs/chapter-notifications.html; config paths, option names, fallbacks and port defaults match.

Method: documentation only; no commands were run.

