---
id: computing-software.cybersecurity-defensive.zitadel.smtp-and-sms-notification-providers
name: smtp-and-sms-notification-providers
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, smtp, sms, twilio, notifications, email]
level: practitioner
status: docs-checked
description: "Configure ZITADEL's SMTP and Twilio SMS providers, activate one, and replace the built-in test mail service before production."
sources:
  - https://zitadel.com/docs/guides/manage/console/default-settings
  - https://zitadel.com/docs/guides/manage/customize/notification-providers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL sends mail and SMS through providers. You can configure several per channel, but messages go only through the active one, so remember to activate the provider after creating it.

SMTP: templates exist for popular services such as Amazon SES, Mailgun, Mailjet and SendGrid; they prefill known host, port and default user. A generic SMTP provider lets you specify server, user and auth method. The console supports plain auth only, while the admin API can also configure XOAUTH2. Fields: sender email address, sender name, TLS on or off, host, user and password. When creating or updating a provider you can send a test, and the providers table lets you activate, deactivate, test or delete.

The built-in default SMTP provider is for testing and evaluation only; delivery may be delayed or unstable. Replace it for production. To send only from domains you own, add a custom domain to the instance.

SMS: no default provider exists. Twilio is the integrated provider. Enter your Sid, Token and either a sender number or a Verification Service Sid, which makes ZITADEL use the Twilio Verify Service rather than the Messages Service.

Message wording can be customized in message texts.

## Checked

2026-11-08. Read the notification providers page and the default settings page in full.

Method: documentation only; no commands were run.
