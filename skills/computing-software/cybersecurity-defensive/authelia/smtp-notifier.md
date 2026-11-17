---
id: computing-software.cybersecurity-defensive.authelia.smtp-notifier
name: smtp-notifier
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, smtp, notifier, email, starttls, submissions, identity-verification]
level: practitioner
status: docs-checked
description: "Configure Authelia's SMTP notifier with the smtp, submission or submissions address scheme, sender, identifier, startup check and TLS requirement."
sources:
  - https://www.authelia.com/configuration/notifications/smtp/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia's notifier can deliver email through an SMTP server.

```yaml
notifier:
  smtp:
    address: 'submissions://smtp.example.com:465'
    timeout: '5s'
    username: 'authelia@example.com'
    password: '<SMTP_PASSWORD>'
    sender: 'Authelia <authelia@example.com>'
    identifier: 'authelia.example.com'
    subject: '[Authelia] {title}'
    startup_check_address: 'test@authelia.com'
```

- `address` takes a scheme of `smtp`, `submission` or `submissions`, differing mainly in default port. `submissions` requires a TLS transport, while `smtp` and `submission` use plain TCP and typically enforce StartTLS.
- `sender` forms the `MAIL FROM` command and the `From` header and must be RFC 5322 format. Only the header carries the display name.
- `identifier` is sent with HELO/EHLO. Some providers, including Google Mail, reject `localhost`, so set a real name.
- `subject` supports the `{title}` placeholder, which should stay in all emails.
- `startup_check_address`: Authelia asks the server if it could send from you to that address at startup; no mail is sent.
- `disable_require_tls` sends mail in the clear and is described as unsupported. By default Authelia requires the SMTP connection to be encrypted by TLS; disabling that sends email in the clear, leaks security-critical values and is highly discouraged.
- `disable_starttls`: some servers falsely claim STARTTLS support and Authelia refuses to send to them by default; enabling this is at your own risk, and the docs prefer fixing the server.
- `startup_check_address` defaults to `test@authelia.com`; `identifier` defaults to `localhost`; `timeout` defaults to 5 seconds.

Check: start Authelia with a valid configuration, request a password reset and confirm the message arrives.

## Checked

2026-11-08. Read the full Authelia SMTP page. Confirmed address schemes, sender RFC 5322 format, identifier and startup_check_address defaults, subject placeholder, timeout default and the TLS security notes for disable_require_tls and disable_starttls. Removed the unsourced statement about password resets and security events and an unsupported attack-scenario sentence.

Method: documentation only; no commands were run.
