---
id: computing-software.collaboration-platform-administration.vikunja.config-mailer-smtp
name: config-mailer-smtp
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, mailer-section, smtp-authtype, forcessl, testmail, email-reminders]
level: practitioner
status: docs-checked
description: "Configure Vikunja's SMTP mailer: host, port, auth type, TLS options and queue, what breaks when it is disabled, and how to test it."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/docker-start-to-finish.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Options under `mailer.*`:
- `enabled` default false. While disabled, all users are enabled right away and password reset is not possible.
- `host`, `port` (default 587; if the only log error is `EOF`, try port 25), `username` (default `user`), `password`.
- `authtype`: `plain` (default), `login` or `cram-md5`.
- `fromemail` default `mail@vikunja`.
- `skiptlsverify` default false.
- `forcessl` default false. By default Vikunja uses STARTTLS when offered and falls back to plaintext; set true to always use implicit TLS (usually port 465) and refuse unencrypted connections.
- `queuelength` 100; `queuetimeout` 30 seconds before an open connection to the mail server is closed.

Task reminder emails also depend on `service.enableemailreminders`.

Test with the `testmail` command. It sends an SMTP `NOOP`, which minimal relays such as `msmtpd` do not support, so a "not connected to SMTP server" error may be the relay. Define SMTP settings in one place only, because environment variables override the config file.

For logs, `log.mail` shows mail events without contents.

## Checked

2026-11-04: options and defaults checked against config-raw.json (mailer section, service.enableemailreminders); `testmail`, the NOOP note and the one-place rule against the Docker start-to-finish page.

Method: documentation only; no commands were run.
