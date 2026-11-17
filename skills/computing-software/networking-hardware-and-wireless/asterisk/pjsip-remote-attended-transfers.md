---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-remote-attended-transfers
name: pjsip-remote-attended-transfers
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, transfer, refer, replaces, external-replaces, attended-transfer, dialplan]
level: advanced
status: docs-checked
description: "Handle PJSIP remote attended transfers (REFER with Replaces to a dialog on another server) by writing an external_replaces dialplan extension using SIPREFERTOHDR."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/res_pjsip-Remote-Attended-Transfers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip remote attended transfers
A remote attended transfer happens when a REFER carries a `Replaces` dialog that is not on this Asterisk (for example Bob on another PBX transfers Alice, connected via Asterisk A, to Carol). If Asterisk finds the dialog locally it does a local attended transfer instead.

Asterisk does not send the INVITE with `Replaces` directly (to avoid transfers being used to reach unwanted destinations). It runs the dialplan extension `external_replaces`, with variables:
- `SIPTRANSFER`: set to `yes`.
- `SIPREFERRINGCONTEXT`: context where `external_replaces` was found.
- `SIPREFERTOHDR`: the Refer-To SIP URI.

With no `external_replaces` extension, remote attended transfers fail. To refuse, call `Hangup()`; the phone is notified the transfer failed and decides what to do. To accept, use Dial, for example:
```
exten => external_replaces,1,NoOp()
 same => n,Dial(PJSIP/default_outgoing/${SIPREFERTOHDR})
```
Use `SIPREFERTOHDR`, `CHANNEL()` values and the `PJSIP_PARSE_URI` function to decide whether to allow it.

## Checked

2026-11-09. Confirmed against the Asterisk res_pjsip Remote Attended Transfers page: REFER with Replaces scenario, local-transfer optimisation, the external_replaces extension and its three variables, Hangup behaviour, the Dial example, CHANNEL() and PJSIP_PARSE_URI. Nothing changed.
Method: documentation only; no commands were run.
