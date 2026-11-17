---
id: computing-software.web-development.ghost.ghost-config-mail-smtp
name: ghost-config-mail-smtp
category: computing-software
field: web-development
product: ghost
tags: [ghost, mail, smtp, mailgun, nodemailer, transactional-email, config]
level: practitioner
status: docs-checked
description: "Configure Ghost transactional mail in config.production.json with SMTP or Mailgun, and avoid blocked outbound SMTP ports."
sources:
  - https://github.com/TryGhost/docs/blob/main/config.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/mail-config-error-google-cloud.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make invitations, password resets and member login emails work.

Mail is required in production. Ghost uses Nodemailer under the hood. Configure `mail` in `config.production.json`, then `ghost restart`.

Mailgun SMTP example (secure connection):
```json
"mail": { "transport": "SMTP", "options": { "service": "Mailgun", "host": "smtp.mailgun.org", "port": 465, "secure": true, "auth": { "user": "postmaster@example.mailgun.org", "pass": "<MAILGUN_SMTP_PASSWORD>" } } }
```
Amazon SES is also covered in the config page.

Default sender: `"mail": { "from": "support@example.com" }`, optionally with a display name: `"'Acme Support' <support@example.com>"`. Use a real, working address to improve delivery of important emails.

Blocked ports: some hosts block outbound SMTP. DigitalOcean blocks ports 25, 465 and 587 on Droplets by default and Google Cloud blocks port 25 on Compute Engine. If your config resolves to a blocked port, set the transmission port explicitly (the Google Cloud FAQ sets 2525) or use Mailgun, which the FAQ recommends.

Test transactional email before bulk email.

Verify: send a staff invitation or password reset and confirm it arrives.

## Checked

2026-11-04. Confirmed: Nodemailer, mail config location, the Mailgun SMTP secure example, SES coverage, mail.from forms, blocked-port facts for DigitalOcean and Google Cloud, the FAQ fix (configuration page and Google Cloud mail FAQ). Removed: "API-based provider" wording, which the FAQ does not use.

Method: documentation only; no commands were run.
