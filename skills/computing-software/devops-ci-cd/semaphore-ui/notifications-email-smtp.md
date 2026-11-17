---
id: computing-software.devops-ci-cd.semaphore-ui.notifications-email-smtp
name: notifications-email-smtp
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [email, smtp, starttls, tls, notifications, semaphore-ui]
level: practitioner
status: docs-checked
description: "Configure SMTP e-mail alerts with email_alert, host, port, StartTLS and a minimum TLS version."
sources:
  - https://semaphoreui.com/docs/admin-guide/notifications/email
  - https://semaphoreui.com/docs/admin-guide/notifications
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# E-mail (SMTP) alerts

Goal: send failure notifications by e-mail.

```json
{
  "email_alert": true,
  "email_sender": "noreply@example.com",
  "email_host": "email-smtp.us-east-1.amazonaws.com",
  "email_port": "587",
  "email_secure": true,
  "email_username": "<aws-key>",
  "email_password": "<aws-secret>",
  "email_tls": true,
  "email_tls_min_version": "1.2"
}
```

The example uses AWS SES SMTP. Key settings:
- `email_secure` enables StartTLS to upgrade the connection to an encrypted channel.
- `email_tls` forces TLS for SMTP connections.
- `email_tls_min_version` is the minimum allowed TLS version, for example `1.2`.

E-mail reports failures only (chat channels also report success and tasks waiting for confirmation), and e-mail project alerts reuse these server SMTP settings.

Gotcha: a server channel sends only if the project's Send alerts of this project to server channels switch is on and the template uses project defaults.

Verify: use Test all in the project's Alerts tab and confirm the message arrives.

## Checked

2026-11-04: checked against the email and notifications pages. Removed unconfirmed port and credential gotchas and the unconfirmed claim about recipients.

Method: documentation only; no commands were run.
