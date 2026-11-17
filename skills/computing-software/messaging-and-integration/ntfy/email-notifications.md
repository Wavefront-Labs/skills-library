---
id: computing-software.messaging-and-integration.ntfy.email-notifications
name: email-notifications
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, email, x-email, smtp, forwarding]
level: practitioner
status: docs-checked
description: "Forward an ntfy message to an email address with X-Email, including the anonymous limits and ntfy.sh verification rules."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Email notifications

Header `X-Email` (aliases `X-E-mail`, `Email`, `E-mail`, `Mail`, `e`) or query `?email=`. Only one address is supported.

```
curl -H "Email: phil@example.com" -d "You've got mail" ntfy.sh/mytopic
```

- When logged in with a verified address, `yes`, `true` or `1` sends to your primary address (or the first verified one). This works regardless of `smtp-sender-verify`.
- Self-hosted anonymous limit: 16 emails per visitor (IP), then one per hour (`visitor-email-limit-burst` and `visitor-email-limit-replenish`). The visitor IP appears in the email body.
- ntfy.sh: anonymous email is disabled; verification is required and free users get 5 emails per visitor per day.

## Server prerequisites

The server must have SMTP sender settings (`smtp-sender-addr` and friends); see the smtp-config skill.

## Gotchas

- JSON publishing uses the `email` field.

## Checked

2026-11-04. Confirmed against the ntfy publish page (E-mail notifications, JSON table) and config page (SMTP sender, email rate limits): aliases, single address, `yes`/`true`/`1`, `smtp-sender-verify` note, 16-then-hourly anonymous limit, IP in body, ntfy.sh 5 per day, `visitor-email-limit-burst` default 16 and replenish 1h. Removed: a content claim and the Verify step.
Method: documentation only; no commands were run.
