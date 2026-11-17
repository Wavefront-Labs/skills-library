---
id: computing-software.messaging-and-integration.prosody.mod-turn-external
name: mod-turn-external
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, turn, stun, voip, nat-traversal]
level: practitioner
status: docs-checked
description: "mod_turn_external in Prosody: advertise an external TURN/STUN server with turn_external_secret, host, port 3478 and ttl 86400, then test with prosodyctl check turn."
sources:
  - https://prosody.im/doc/modules/mod_turn_external
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_turn_external

Gives clients credentials for an external TURN/STUN server (Prosody 0.12.0+).

```lua
modules_enabled = { "turn_external", }
turn_external_secret = "aGVtbGlndAo="
turn_external_host = "turn.example.com"
turn_external_port = 3478
```

| Option | Default |
|---|---|
| `turn_external_secret` | required, shared with the TURN server |
| `turn_external_host` | the VirtualHost name |
| `turn_external_port` | 3478 |
| `turn_external_ttl` | 86400 seconds |
| `turn_external_user` | none; suffix on generated usernames |
| `turn_external_tcp`, `turn_external_tls_port` | uncommon extras |

Verify: `prosodyctl check turn` (optionally `--ping=stun.server.example`) passes.

## Checked

2026-11-04. Read the mod_turn_external and prosodyctl pages: included from 0.12.0, turn_external_secret required, host default VirtualHost, port 3478, ttl 86400, user suffix, tcp and tls_port extras, and prosodyctl check turn with the optional --ping flag all match. Nothing removed.

Method: documentation only; no commands were run.
