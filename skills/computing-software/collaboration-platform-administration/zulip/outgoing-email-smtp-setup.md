---
id: computing-software.collaboration-platform-administration.zulip.outgoing-email-smtp-setup
name: outgoing-email-smtp-setup
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [outgoing-email, smtp-settings, email-password, noreply-address]
level: intro
status: docs-checked
description: "Configure Zulip outgoing SMTP email: settings.py email section, email_password in zulip-secrets.conf, noreply addresses, sender permissions and a restart."
sources: ["https://zulip.readthedocs.io/en/latest/production/email.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zulip outgoing email (SMTP)

Zulip must send mail to confirm addresses, and deliver notifications.

1. Get an SMTP account. A transactional email service is recommended (see the provider skill).
2. In `/etc/zulip/settings.py`, fill in the "Outgoing email (SMTP) settings" section: host, usually the port, and `EMAIL_HOST_USER`. Leave the user empty if the server needs no authentication.
3. Fill the noreply section too: `NOREPLY_EMAIL_ADDRESS` and `TOKENIZED_NOREPLY_EMAIL_ADDRESS`, following the inline comments. `INSTALLATION_NAME` customises the display name on notification emails.
4. Put the password in `/etc/zulip/zulip-secrets.conf` as `email_password`. Zulip deliberately reads it from there rather than Django's usual `EMAIL_HOST_PASSWORD`, so no secret sits in `settings.py`.
5. Make your SMTP service allow Zulip to send from `ZULIP_ADMINISTRATOR`, `NOREPLY_EMAIL_ADDRESS` and, while `ADD_TOKENS_TO_NOREPLY_ADDRESS=True` (the default), the tokenized noreply address. Transactional providers guide you through DKIM and SPF so mail is not filtered as spam.
6. Test with `send_test_email` (see the troubleshooting skill).
7. Restart: `su zulip -c '~zulip/deployments/current/scripts/restart-server'`.

Any change to configuration needs that restart before the running server sees it. Docker deployments use `SETTING_EMAIL_*` environment variables and an `email_password` secret instead of editing these files.

For prototyping with no provider, the file-based email backend described in the providers skill lets you read what would have been sent.

## Checked

2026-11-08. Checked: read against the Zulip email page (docs/production/email.md, read in full). Removed: the claim that Zulip sends password resets by this path.

Method: documentation only; no commands were run.
