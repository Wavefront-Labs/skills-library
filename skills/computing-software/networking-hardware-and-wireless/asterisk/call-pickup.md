---
id: computing-software.networking-hardware-and-wireless.asterisk.call-pickup
name: call-pickup
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, call-pickup, pickup, pickupchan, callgroup, pickupgroup, pickupexten, features]
level: practitioner
status: docs-checked
description: "Enable call pickup with Pickup and PickupChan, the pickupexten feature code, numeric and named callgroup and pickupgroup via CHANNEL(), and pickup sounds in features.conf."
sources:
  - https://docs.asterisk.org/Configuration/Features/Call-Pickup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# call pickup
Pickup answers a call ringing another phone or group. Request it with the `Pickup` or `PickupChan` applications, or by dialing the `pickupexten` extension from `features.conf`. The page says support was added in Asterisk 11.

Groups:
- Numeric: `callgroup` (groups the channel is in) and `pickupgroup` (groups it can pick up), values 0 to 63, lists like `1,5-7`, max 64 groups.
- Named: `namedcallgroup`, `namedpickupgroup`.
- Dialplan: `Set(CHANNEL(callgroup)=1,5-7)`, `Set(CHANNEL(namedpickupgroup)=engineering,sales)`.
- `callgroup` must be set on the outgoing (ringing) channel, via a channel driver `setvar`/`set_var` option or a pre-dial handler. Pickup groups must be set before running Pickup or dialing `pickupexten`.

`features.conf`:
```
pickupexten = *8
pickupsound = beep
pickupfailsound = beeperr
```
Drivers supporting `pickupexten`: chan_dahdi/analog, chan_mgcp, chan_misdn, chan_sip, chan_unistim, chan_pjsip.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Call-Pickup) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
