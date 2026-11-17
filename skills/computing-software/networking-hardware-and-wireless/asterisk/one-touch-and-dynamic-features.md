---
id: computing-software.networking-hardware-and-wireless.asterisk.one-touch-and-dynamic-features
name: one-touch-and-dynamic-features
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, features-conf, automon, automixmon, applicationmap, dynamic-features, one-touch, recording]
level: practitioner
status: docs-checked
description: "Configure one-touch features (automon, automixmon, disconnect, parkcall) with Dial and Queue option pairs, and define custom DTMF features in the features.conf applicationmap."
sources:
  - https://docs.asterisk.org/Configuration/Features/One-Touch-Features/
  - https://docs.asterisk.org/Configuration/Features/Custom-Dynamic-Features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# one-touch and dynamic features
**One-touch** codes go in `[featuremap]` of `features.conf`:
```
automon = *1
automixmon = *3
disconnect = *0
parkcall = #72
```
`automon` starts Monitor, `automixmon` starts MixMonitor, `disconnect` hangs up the channel, `parkcall` parks. Each needs an option on Dial or Queue (neither of the pair set means the feature is unusable): automon `W` (calling) / `w` (called); automixmon `X` / `x`; disconnect `H` / `h`; parkcall `K` / `k`. Example: `Dial(PJSIP/ALICE,30,X)`.

**Custom features** go in `[applicationmap]`:
`<FeatureName> = <DTMF_sequence>,<ActivateOn>[/<ActivatedBy>],<Application>[,<AppArguments>[,MOH_Class]]`
- `ActivateOn`: `self` (the channel that pressed the keys) or `peer`.
- `ActivatedBy` is no longer honored; the feature is active on whichever channel has it in `DYNAMIC_FEATURES`, so use a pre-dial handler to set it per leg.
- Use the quoted or parenthesised argument forms when arguments contain commas.
- `MOH_Class` plays music on the idle channel.

These applications run outside the PBX core, so the PBX stays in the media flow and DTMF in the media stream cannot be redirected.

## Checked
2026-11-04: read the cited Asterisk documentation pages (One-Touch-Features, Custom-Dynamic-Features) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
