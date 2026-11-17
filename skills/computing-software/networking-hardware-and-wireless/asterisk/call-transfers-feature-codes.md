---
id: computing-software.networking-hardware-and-wireless.asterisk.call-transfers-feature-codes
name: call-transfers-feature-codes
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, call-transfer, blind-transfer, attended-transfer, features-conf, atxfer, featuremap]
level: practitioner
status: docs-checked
description: "Enable core blind and attended transfers with featuremap blindxfer and atxfer codes, Dial t/T options, atxferabort/complete/threeway/swap codes and callback timers."
sources:
  - https://docs.asterisk.org/Configuration/Features/Feature-Code-Call-Transfers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# call transfers with feature codes
Core transfers (blind and attended) are configured in `features.conf` and are separate from the native transfer support in chan_sip and chan_pjsip.

Requirements: the transfer type has a DTMF string, the application invoking the channel allows it, and the channels are answered and bridged.
```
[featuremap]
blindxfer = #1
atxfer = *2
```
In `Dial`, `t` lets the called party transfer the caller and `T` the calling party (the same applies to Queue).

Attended transfer control codes (in `[general]`): `atxferabort`, `atxfercomplete` (finish and drop out), `atxferthreeway` (finish and join a bridge with both), `atxferswap` (switch between parties before completing). Example values `*3`, `*4`, `*5`, `*6`.

Callbacks when the initiator hangs up early and the target does not answer:
- `atxfernoanswertimeout` (seconds to ring the target);
- `atxferdropcall` (default `no`, meaning call back the initiator);
- `atxferloopdelay` (seconds between retries, only with `atxferdropcall=no`);
- `atxfercallbackretries` (default 2).

## Checked
2026-11-04: read the cited Asterisk documentation pages (Feature-Code-Call-Transfers) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
