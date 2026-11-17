---
id: computing-software.collaboration-platform-administration.zulip.outgoing-email-troubleshooting
name: outgoing-email-troubleshooting
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [send-test-email, email-troubleshooting, send-email-log]
level: practitioner
status: docs-checked
description: "Debug Zulip outgoing email with send_test_email, the noreply token setting, send_email.log, errors.log and provider logs, plus common firewall and password causes."
sources: ["https://zulip.readthedocs.io/en/latest/production/email.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting Zulip outgoing email

Run the built-in test as the Zulip user:

```
su zulip -c '~zulip/deployments/current/manage.py send_test_email user@example.com'
```

No error probably means success. Check for two emails: one from the default From address and one from the noreply address. The command reads the latest config files even while the server still runs old settings, so you can test before restarting.

Common causes of failure:

- The hosting provider's default firewall blocks the SMTP port in `EMAIL_PORT`.
- The SMTP account may not be permitted to send from the noreply addresses. Zulip sends confirmation emails from random addresses starting with `noreply-`. If that is a problem, set `ADD_TOKENS_TO_NOREPLY_ADDRESS = False` so they come from a fixed `noreply@` address. It is generally safe unless you let anyone with an address in a given domain create accounts, because the tokens protect against a helpdesk-software style attack.
- `email_password` missing from `/etc/zulip/zulip-secrets.conf`, or typos in username or password.
- No restart after editing `settings.py` or the secrets file: use `~zulip/deployments/current/scripts/restart-server`.

Deeper checks:

- Your provider's outgoing log shows whether mail arrived and whether it was flagged.
- `/var/log/zulip/send_email.log` records each attempt and result.
- Exceptions appear with tracebacks in `/var/log/zulip/errors.log`.
- Configuration follows Django's SMTP backend, so Django documentation for your provider applies, except that the password goes in `email_password`.

## Checked

2026-11-08. Checked: read against the Zulip email page (docs/production/email.md, read in full). Removed: nothing.

Method: documentation only; no commands were run.
