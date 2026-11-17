---
id: computing-software.email-administration.mail-server-administration.quota-plugin-setup
name: quota-plugin-setup
category: computing-software
field: email-administration
product: mail-server-administration
tags: [quota-plugin-setup, dovecot-quota, quota-plugin, quota-warning]
level: practitioner
status: docs-checked
description: "Enable the Dovecot quota plugin with per-user limits, quota warnings and over-quota behaviour."
sources:
  - https://doc.dovecot.org/2.3/configuration_manual/quota_plugin/
  - https://doc.dovecot.org/2.3/configuration_manual/quota/
  - https://doc.dovecot.org/main/core/man/doveadm-quota.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quota plugin setup

**Goal:** cap mailbox sizes.
## Steps
1. `mail_plugins = $mail_plugins quota` and `protocol imap { mail_plugins = $mail_plugins imap_quota }`.
2. `plugin { quota = count:User quota  quota_rule = *:storage=1G  quota_vsizes = yes }` (2.3 syntax; `count` is the recommended backend for new installs and needs `quota_vsizes = yes`; Dovecot 2.4 splits `quota` and `quota_rule` into separate quota settings).
3. Per-user override: return `quota_rule` from userdb, for example `*:storage=5G`.
4. Let the Trash mailbox exceed the limit slightly so move-to-Trash works when full, e.g. `quota_rule2 = Trash:storage=+100M`.
5. Warnings: `quota_warning = storage=95%% quota-warning 95 %u` (runs the `quota-warning` service).
## Failure modes
- A full mailbox makes COPY to Trash fail, so clients cannot delete mail; see the Trash rule above.
- Quota recalculation: `doveadm quota recalc -u user`.
## Verify
- `doveadm quota get -u alice@example.com` shows usage and limit.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 Quota Plugin and Quota Configuration pages (mail_plugins quota and imap_quota, `count:User quota`, `quota_vsizes = yes` required for count, `quota_rule`/`quota_rule2` and the Trash example, `quota_warning` form, recalc and `doveadm quota get`), and the 2.3 to 2.4 converted-settings table. Added the missing `quota_vsizes`. Removed the LMTP over-quota claim (not stated).

Method: documentation only; no commands were run.
