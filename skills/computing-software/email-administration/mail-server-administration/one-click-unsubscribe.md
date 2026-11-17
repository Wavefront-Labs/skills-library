---
id: computing-software.email-administration.mail-server-administration.one-click-unsubscribe
name: one-click-unsubscribe
category: computing-software
field: email-administration
product: mail-server-administration
tags: [one-click-unsubscribe, list-unsubscribe, list-unsubscribe-post, rfc-8058]
level: advanced
status: draft
description: "Add List-Unsubscribe and List-Unsubscribe-Post headers for RFC 8058 one-click unsubscribe, signed by DKIM."
sources:
  - https://support.google.com/a/answer/81126
  - https://senders.yahooinc.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# One click unsubscribe

**Goal:** a header receivers can act on.
## Steps
1. Add `List-Unsubscribe: <https://example.com/u/abc123>, <mailto:unsub@example.com>`.
2. Add `List-Unsubscribe-Post: List-Unsubscribe=One-Click`.
3. The HTTPS endpoint must accept a POST with that body and unsubscribe without further interaction.
4. Both headers must be covered by the DKIM signature (RFC 8058 requirement).
## Failure modes
- Link requires login or a confirmation page: not one-click.
- Unsigned headers are ignored.
## Verify
- `curl -X POST -d 'List-Unsubscribe=One-Click' https://example.com/u/abc123` unsubscribes the test address.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
