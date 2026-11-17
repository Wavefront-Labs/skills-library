---
id: computing-software.messaging-and-integration.ntfy.email-publishing
name: email-publishing
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, email, email-publishing, smtp-server, topic-address]
level: practitioner
status: docs-checked
description: "Publish to an ntfy topic by sending an email to ntfy-<topic>@host, including token auth, what is supported, and the server keys."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing by email

Send an email to `ntfy-$topic@ntfy.sh`. With an access token: `ntfy-$topic+$token@ntfy.sh`.

- Authentication is required if access control applies to the topic. Username and password work through SMTP AUTH PLAIN.
- Only the message title (the email subject) is supported as an option. Tags, priority, delay and other features are not.

## Self-hosted server config

```yaml
smtp-server-listen: ":25"
smtp-server-domain: "ntfy.example.com"
smtp-server-addr-prefix: "ntfy-"
```

- `smtp-server-listen` (for example `:25`) and `smtp-server-domain` enable the feature.
- `smtp-server-addr-prefix` is optional.
- There is a "local-only email" variant in the config docs for servers not exposed to the internet.

## Gotchas

- Do not expect priority or tags from email; use JSON or headers instead.

## Checked

2026-11-04. Confirmed against the ntfy publish page (E-mail publishing) and config page (E-mail publishing, SMTP server options): address formats, token form, SMTP AUTH PLAIN, title-only support, the three `smtp-server-*` keys, `:25` example, optional prefix, local-only variant. Removed: the Verify step.
Method: documentation only; no commands were run.
