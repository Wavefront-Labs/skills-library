---
id: computing-software.devops-ci-cd.forgejo.email-smtp-and-sendmail
name: email-smtp-and-sendmail
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [mailer, smtp, sendmail, starttls]
level: practitioner
status: docs-checked
description: "Enable outbound email via SMTP or sendmail, with the TLS requirement for authentication."
sources:
  - https://forgejo.org/docs/latest/admin/setup/email/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo sends mail such as registration confirmations through Sendmail-compatible MTAs (Postfix, msmtp) or directly via an SMTP server.

SMTP example under `[mailer]`: `ENABLED = true`, `FROM = forgejo@example.com`, `PROTOCOL = smtps`, `SMTP_ADDR = mail.example.com`, `SMTP_PORT = 465`, `USER`, and `PASSWD` (wrapped in backticks). Restart Forgejo, then send a test email from Site Administration > Configuration > SMTP Mailer Configuration. For user notifications on issues and pull requests also set `[service] ENABLE_NOTIFY_MAIL = true`.

Authentication works only when the SMTP connection is encrypted with TLS or `HOST=localhost`, a protection from Go libraries against STRIPTLS attacks. TLS comes either from STARTTLS (opportunistic, port 587, upgraded after a cleartext start) or SMTPS (implicit TLS, `SMTP_PORT=465` and/or `PROTOCOL=smtps`, recommended by RFC 8314).

Sendmail example: `PROTOCOL = sendmail`, `SENDMAIL_PATH = /usr/sbin/sendmail` and `SENDMAIL_ARGS = "--"`, which stops an address being read as an option. For internet-facing sites configure TLS in your MTA and publish SPF, DMARC and DKIM DNS records so providers accept the mail.

## Checked

2026-11-04. Confirmed against the Forgejo Email setup page: the SMTP and sendmail [mailer] samples, restart, the test-email menu path, ENABLE_NOTIFY_MAIL, the TLS and STRIPTLS note, STARTTLS port 587, SMTPS and RFC 8314, and the SPF, DMARC, DKIM advice. Nothing removed.

Method: documentation only; no commands were run.
