---
id: computing-software.email-administration.mail-server-administration.quota-postfix-integration
name: quota-postfix-integration
category: computing-software
field: email-administration
product: mail-server-administration
tags: [quota-postfix-integration, quota-status, over-quota-reject]
level: advanced
status: docs-checked
description: "Make Postfix reject over-quota mail at SMTP time with a quota-status policy service instead of bouncing later."
sources:
  - https://doc.dovecot.org/2.3/configuration_manual/quota_plugin/
  - https://doc.dovecot.org/2.3/configuration_manual/nfs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quota postfix integration

**Goal:** avoid backscatter for full mailboxes.
## Steps
1. Dovecot: `service quota-status { executable = quota-status -p postfix  inet_listener { port = 12340 }  client_limit = 1 }` (any port), and in `plugin {}`: `quota_status_success = DUNNO`, `quota_status_nouser = DUNNO`, `quota_status_overquota = "552 5.2.2 Mailbox is full"` (Dovecot 2.3 syntax).
2. Postfix: `check_policy_service inet:mailstore.example.com:12340` in `smtpd_recipient_restrictions`.
## Failure modes
- Do not use the `quota-status` service on NFS.
- Quota data out of sync: run `doveadm quota recalc -u <user>`.
## Verify
- Fill a test mailbox; the sending server gets `552 5.2.2` during RCPT.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 Quota Plugin page (quota-status service example with port 12340, `check_policy_service inet:` line, the three quota_status_* values, recalc) and the NFS page (do not use quota-status). Fixed: the original used a unix socket and `unix:private/quota-status`, which the docs do not show; replaced with the documented inet listener. Removed the reject_unauth_destination ordering and the service-down behaviour (not stated).

Method: documentation only; no commands were run.
