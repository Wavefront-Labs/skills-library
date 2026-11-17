---
id: computing-software.collaboration-platform-administration.zulip.outgoing-email-providers
name: outgoing-email-providers
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [email-providers, email-use-tls, email-backend, gmail-smtp]
level: practitioner
status: docs-checked
description: "Choose and configure a Zulip outgoing email provider: Mailgun-style SMTP values, port 465 SSL, local postfix, Gmail caveats and the file-based prototype backend."
sources: ["https://zulip.readthedocs.io/en/latest/production/email.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Outgoing email provider options

Transactional services (Mailgun, SendGrid, Amazon SES) are recommended, and all have free tiers. After sign-up, copy the SMTP credentials into `/etc/zulip/settings.py`:

- `EMAIL_HOST = 'smtp.mailgun.org'` (your provider's host)
- `EMAIL_HOST_USER = 'username@example.com'`
- `EMAIL_USE_TLS = True` and `EMAIL_PORT = 587` for most providers (STARTTLS)
- password as `email_password` in `/etc/zulip/zulip-secrets.conf`

For implicit TLS on port 465, set `EMAIL_PORT = 465` and replace `EMAIL_USE_TLS = True` with `EMAIL_USE_SSL = True`.

Local system mail, such as a postfix relay into corporate mail, typically uses `EMAIL_HOST = 'localhost'`, `EMAIL_PORT = 25`, `EMAIL_USE_TLS = False` and an empty `EMAIL_HOST_USER`. Ensure the downstream system signs outgoing mail, or check spam folders.

Gmail is discouraged because its anti-spam measures are annoying. If you must, create a dedicated account (never a personal one), use an app-specific password when 2-factor authentication is on, otherwise mark the account "less secure", and expect low rate limits of around 100 per day.

For prototyping, log mail to files instead:

```
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/var/log/zulip/emails'
```

Emails then land in `/var/log/zulip/emails/`. Remove these lines and restart once you configure a real provider.

## Checked

2026-11-08. Checked: read against the Zulip email page (docs/production/email.md, read in full). Removed: nothing.

Method: documentation only; no commands were run.
