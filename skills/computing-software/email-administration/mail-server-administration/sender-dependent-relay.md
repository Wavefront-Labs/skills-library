---
id: computing-software.email-administration.mail-server-administration.sender-dependent-relay
name: sender-dependent-relay
category: computing-software
field: email-administration
product: mail-server-administration
tags: [sender-dependent-relay, sender-dependent-relayhost-maps, sender-dependent-routing]
level: advanced
status: draft
description: "Route outbound mail through different relays by sender with sender_dependent_relayhost_maps."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sender dependent relay

**Goal:** per-domain outbound routing.
## Steps
1. `sender_dependent_relayhost_maps = hash:/etc/postfix/sender_relay`
2. Table: `@example.com  [relay1.example.net]:587`.
3. Also set `smtp_sender_dependent_authentication = yes` so the right SASL credentials are used.
4. `postmap` and reload.
## Failure modes
- Lookups keyed on the wrong address (envelope sender), so some mail misroutes.
## Verify
- Send from two senders and confirm different relays in the log.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
