---
id: computing-software.devops-ci-cd.gitea.email-setup
name: email-setup
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-mailer-smtp, gitea, mailer, sendmail, smtps, smtp-starttls, enable-notify-mail, gmail-app-password, protonmail-smtp-token]
level: practitioner
status: docs-checked
description: "Configure the Gitea [mailer] section for sendmail or SMTP (smtps vs smtp+starttls), notification flag, Gmail app passwords and Proton SMTP tokens."
sources: ["https://docs.gitea.com/administration/email-setup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea mailer setup

Gitea sends transactional mail via a sendmail-compatible MTA (Postfix, msmtp) or directly through an SMTP server. Notification mails additionally need `ENABLE_NOTIFY_MAIL=true` in `[service]`.

## Sendmail
```ini
[mailer]
ENABLED       = true
FROM          = gitea@mydomain.com
PROTOCOL      = sendmail
SENDMAIL_PATH = /usr/sbin/sendmail
SENDMAIL_ARGS = "--"   ; stops an address being parsed as an option
```
Not usable in the official Docker image (use SMTP there). For internet-facing mail, configure TLS in the MTA and publish SPF, DMARC and DKIM DNS records.

## SMTP relay
```ini
[mailer]
ENABLED   = true
FROM      = gitea@mydomain.com
PROTOCOL  = smtps
SMTP_ADDR = mail.mydomain.com
SMTP_PORT = 465
USER      = gitea@mydomain.com
PASSWD    = `password`
```
Restart Gitea afterwards. Send a test mail from Site Administration, Configuration, Summary, Mailer Configuration.
Authentication only works when the connection is TLS-encrypted or `HOST=localhost` (Go's protection against STRIPTLS). Options: `PROTOCOL=smtp+starttls` on port 587 (cleartext then upgraded), SMTPS on 465, or forced `PROTOCOL=smtps` (implicit TLS, recommended by RFC 8314).

## Gmail
`SMTP_ADDR = smtp.gmail.com`, `SMTP_PORT = 465`, `PROTOCOL = smtps`, `FROM`/`USER` the Google account. Use an **app password** (needs 2-step verification; a Workspace admin can disable them, then use the Workspace SMTP relay or another provider). Plain account passwords no longer work and Gitea's mailer does not implement OAuth (it uses `CRAM-MD5`, `PLAIN` or `LOGIN`). Port 587 works with `SMTP_PORT = 587` and `PROTOCOL = smtp+starttls`. Remove any `HOST=` line on Gitea >= 1.18.0.

## ProtonMail
Only for select business plans and custom-domain addresses (or via ProtonMail Bridge). Generate an SMTP token in Settings, IMAP/SMTP, SMTP tokens, pick a custom-domain address and use it for both `FROM` and `USER`; the token is the `PASSWD`, shown only once. Config: `PROTOCOL = smtp+starttls`, `SMTP_ADDR = smtp.protonmail.ch`, `SMTP_PORT = 587`. Login or mailbox passwords do not work.

## Checked

2026-11-03: read https://docs.gitea.com/administration/email-setup/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
