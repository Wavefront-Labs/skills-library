---
id: computing-software.messaging-and-integration.ntfy.smtp-config
name: smtp-config
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, smtp, smtp-sender, email-server, smtp-sender-verify]
level: practitioner
status: docs-checked
description: "Server keys for ntfy outgoing email (smtp-sender-*) and incoming email publishing (smtp-server-*)."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMTP configuration

## Outgoing: email notifications

Keys: `base-url`, `smtp-sender-addr`, `smtp-sender-user`, `smtp-sender-pass`, `smtp-sender-from`, `smtp-sender-verify`.

- `smtp-sender-verify` defaults to off: any user, including anonymous, can email any address. When true, anonymous users cannot send and logged-in users can only send to addresses they verified.
- Only PLAIN or LOGIN auth with STARTTLS is supported.
- Anonymous limits default to a burst of 16 emails then one per hour (`visitor-email-limit-burst`, `visitor-email-limit-replenish`).

## Incoming: email publishing

```yaml
smtp-server-listen: ":25"
smtp-server-domain: "ntfy.example.com"
smtp-server-addr-prefix: "ntfy-"
```

`smtp-server-addr-prefix` is optional. With `ntfy-` set, only mail to `ntfy-<topic>@<domain>` is accepted; without it all mail to `<topic>@<domain>` is accepted, which may be a spam problem.

## Gotchas

- Outgoing mail needs the SMTP sender settings above; `smtp-sender-addr` is the hostname:port.
- Regardless of `smtp-sender-verify`, a logged-in user can pass `yes`, `true` or `1` as `X-Email` to send to their primary verified address.
- Incoming mail also needs an MX record and a matching A record; `smtp-server-domain` must be identical to the MX record.
- See email-notifications and email-publishing for client-side use.

## Checked

2026-11-04. Confirmed against the ntfy config page (E-mail notifications and E-mail publishing: keys, PLAIN/LOGIN with STARTTLS, smtp-sender-verify behaviour, yes/true/1, addr prefix, MX/A records). Corrected: smtp-sender-verify wording. Removed: the Verify step.
Method: documentation only; no commands were run.
