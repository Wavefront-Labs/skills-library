---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-mail-and-webhooks
name: bookstack-mail-and-webhooks
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, mail, smtp, sendmail, mail-driver, webhooks, slack-compatible, mail-verify-ssl]
level: practitioner
status: docs-checked
description: "Configure BookStack outbound email with the MAIL_ variables for SMTP or sendmail, and note how outgoing webhooks are set up and what format they send."
sources: ["https://www.bookstackapp.com/docs/admin/email-webhooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack email and webhooks

Variables in `.env`: `MAIL_DRIVER` (`smtp` or `sendmail`), `MAIL_HOST`, `MAIL_PORT`, `MAIL_ENCRYPTION`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`, `MAIL_FROM_NAME`, `MAIL_VERIFY_SSL`, `MAIL_SENDMAIL_COMMAND`.

```
MAIL_DRIVER=smtp
MAIL_HOST=smtp.provider.tld
MAIL_PORT=587
MAIL_ENCRYPTION=tls
MAIL_USERNAME=user@provider.tld
MAIL_PASSWORD=onlyifneeded
MAIL_FROM=noreply@yourdomain.tld
MAIL_FROM_NAME=BookStack
```
```
MAIL_DRIVER=sendmail
MAIL_FROM=noreply@yourdomain.tld
MAIL_SENDMAIL_COMMAND="/usr/sbin/sendmail -bs"
```

`MAIL_VERIFY_SSL=false` disables certificate verification and the docs warn it exposes you to man-in-the-middle attacks.

Webhooks are configured under Settings > Webhooks. The POST payload example is shown when you create or edit one, and it is "Slack compatible": it includes a `text` property with a readable event description, so Discord, Zulip and Teams endpoints that accept that format work. Webhooks can slow the system; the docs cover running them asynchronously under async action handling. `ALLOWED_SSR_HOSTS` (default `*`, prefix match) restricts which hosts webhooks may call.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/email-webhooks/ and admin/security/ (ALLOWED_SSR_HOSTS) (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
