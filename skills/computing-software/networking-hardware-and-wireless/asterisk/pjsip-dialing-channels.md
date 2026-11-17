---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-dialing-channels
name: pjsip-dialing-channels
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, dial, pjsip-dial-contacts, aor, contact, dialplan]
level: intro
status: docs-checked
description: "Dial PJSIP endpoints from the dialplan: Dial(PJSIP/endpoint), PJSIP_DIAL_CONTACTS(), and dialing an explicit SIP URI or a user@endpoint through a trunk AoR."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/Dialing-PJSIP-Channels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip dialing channels
- `Dial(PJSIP/${EXTEN})` looks at the AoR with the same name as the endpoint and dials the first contact.
- `Dial(${PJSIP_DIAL_CONTACTS(${EXTEN})})` evaluates to a list of all the endpoint contacts separated by `&`, so Dial rings them simultaneously.
- Explicit URI via an endpoint, bypassing its AoR contacts: `Dial(PJSIP/mytrunk/sip:${EXTEN:1}@203.0.113.1:5060)`.
- `Dial(PJSIP/${EXTEN:1}@mytrunk)` uses the contact and domain from the AoR of endpoint `mytrunk` but sets the user part itself. For this, define the AoR contact without a user name (for example `contact=sip:203.0.113.1:5060`).

Full help: `core show application Dial`.

## Checked

2026-11-09. Confirmed against the Asterisk Dialing PJSIP Channels page: the four Dial forms, the PJSIP_DIAL_CONTACTS separator and the AoR contact without a user name. Nothing changed.
Method: documentation only; no commands were run.
