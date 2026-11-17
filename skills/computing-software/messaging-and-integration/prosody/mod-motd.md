---
id: computing-software.messaging-and-integration.prosody.mod-motd
name: mod-motd
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, motd, login-message, modules]
level: intro
status: docs-checked
description: "mod_motd in Prosody: a message of the day sent at every login, motd_text for the body (multi-line with [[ ]]) and motd_jid for the sender."
sources:
  - https://prosody.im/doc/modules/mod_motd
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_motd

Sends a fixed message to users on each login. For new registrants only, use `mod_welcome`.

```lua
modules_enabled = { "motd"; }
motd_text = [[Welcome to the server!
Please enjoy your stay.]]
```

- `motd_text`: default `"MOTD: (blank)"`. Use `[[ ... ]]` for multi-line text.
- `motd_jid`: sender address, defaulting to the current VirtualHost; set another JID such as an admin to send from there.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_motd (motd_text and motd_jid defaults, multi-line syntax, mod_welcome pointer). Removed a generic verify line.
Method: documentation only; no commands were run.
