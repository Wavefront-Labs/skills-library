---
id: computing-software.systems-network-administration.virtualisation.proxmox-notification-targets-and-matchers
name: proxmox-notification-targets-and-matchers
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-notifications, notifications, smtp, gotify, webhook, proxmox]
level: practitioner
status: docs-checked
description: "Configure the Proxmox VE notification system: sendmail, SMTP, Gotify and webhook targets, matchers by severity and event type, and backup job notification mode."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-notifications.html
  - https://github.com/proxmox/pve-docs/blob/master/notifications.adoc
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Proxmox VE notification targets and matchers

**Goal:** the right people get backup, replication, fencing and update alerts through the right channel.

## Model (PVE 8.1+)
- **Targets**: `sendmail` (uses the local sendmail binary), `smtp` (direct to a relay; PLAIN and LOGIN auth, modes `insecure`, `starttls`, `tls` defaulting to `tls`), `gotify`, and `webhook` (HTTP requests to a configurable URL with Handlebars templating of url, header and body, for example for ntfy.sh).
- **Matchers**: rules that route notifications to targets by `match-severity` (`info`, `notice`, `warning`, `error`, `unknown`), `match-field` (`exact:` or `regex:`, for example `exact:type=vzdump`, `exact:hostname=pve1`) and `match-calendar` (for example `mon..fri 9:00-17:00`). A matcher without rules always matches, and each target is notified at most once per notification.
- Config: `/etc/pve/notifications.cfg`; secrets in `/etc/pve/priv/notifications.cfg`.

## Example
```
smtp: relay
	server smtp.example.com
	port 587
	mode starttls
	username pve-alerts
	from-address pve@example.com
	mailto-user root@pam

matcher: backup-failures
	match-field exact:type=vzdump
	match-severity error
	target relay

matcher: fencing
	match-field exact:type=fencing
	target relay
	target ops-webhook
```
Datacenter -> Notifications -> **Test** on each target before relying on it (testing needs the `Mapping.Use`, `Mapping.Audit` or `Mapping.Modify` privilege). The SMTP password lives in `/etc/pve/priv/notifications.cfg`, not in the example above.

## Event types
`vzdump` (backup succeeded `info` or failed `error`), `replication` (failed, `error`), `fencing` (node fenced, `error`), `package-updates` (`info`), `system-mail` (mail for root, severity `unknown`).

## Backup jobs
Each backup job has a `notification-mode`: `notification-system` (global targets and matchers), `legacy-sendmail` (sends via the system sendmail to the job's mailto and ignores targets and matchers; may be removed in a later release) or `auto` (the default: email if mailto is set, otherwise the notification system). Switch old jobs to `notification-system` so routing is central.

## Gotchas
- `mailto-user` entries are resolved to the email address stored for that user in `users.cfg`; set the address in the user settings.
- SMTP targets have no queueing or retry, unlike sendmail targets.
- SMTP relays may require that `from-address` is owned by the authenticating user.

## Verify
Use the target Test button, then trigger a failing backup in a lab and confirm the alert arrives once, at the right target.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: notifications.adoc, generated vzdump.conf.5-opts.adoc notification-mode) and confirmed the target types and options, matcher match-field, match-severity and match-calendar syntax, the event type table, the notification-mode values and the config file locations (/etc/pve/notifications.cfg and /etc/pve/priv/notifications.cfg). Removed the unconfirmed webhook 8.3 gate, default-matcher claim and the empty-address claim.

Method: documentation only; no commands were run.
