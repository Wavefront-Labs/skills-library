---
id: computing-software.networking-hardware-and-wireless.asterisk.confbridge-runtime-control
name: confbridge-runtime-control
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, confbridge, conferencing, confbridge-cli, ami, confbridge-function, confbridge-info]
level: practitioner
status: docs-checked
description: "Control live ConfBridge conferences: confbridge CLI commands (list, kick, lock, mute), AMI actions, and the CONFBRIDGE and CONFBRIDGE_INFO dialplan functions."
sources:
  - https://docs.asterisk.org/Configuration/Applications/Conferencing-Applications/ConfBridge/ConfBridge-CLI-Commands/
  - https://docs.asterisk.org/Configuration/Applications/Conferencing-Applications/ConfBridge/ConfBridge-AMI-Actions/
  - https://docs.asterisk.org/Configuration/Applications/Conferencing-Applications/ConfBridge/ConfBridge-Functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# confbridge runtime control
CLI commands:
- `confbridge list` (all bridges: users, marked, locked) and `confbridge list <conference>` (channel, user profile, bridge profile, menu).
- `confbridge kick <conference> <channel>`; `confbridge mute|unmute <conference> <channel>`.
- `confbridge lock <conference>` / `confbridge unlock <conference>`; locking admits only Admin users.

AMI actions include `ConfbridgeList` (users, ending with `ConfbridgeListComplete`), `ConfbridgeListRooms` and `ConfbridgeMute` (Conference, Channel). Each takes Conference and results come back as events.

Dialplan functions:
- `CONFBRIDGE(type,option)` sets a profile option on the channel; type is `bridge` or `user`, option is any `confbridge.conf` option, and `template` bases it on an existing profile:
```
exten => 1,n,Set(CONFBRIDGE(user,template)=default_user)
exten => 1,n,Set(CONFBRIDGE(user,admin)=yes)
exten => 1,n,ConfBridge(1)
```
- `CONFBRIDGE_INFO(type,conf)` returns `parties`, `admins`, `marked` or `locked` for a conference.

## Checked
2026-11-04: read the cited Asterisk documentation pages (ConfBridge-CLI-Commands, ConfBridge-AMI-Actions, ConfBridge-Functions) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
