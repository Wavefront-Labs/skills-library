---
id: computing-software.messaging-and-integration.prosody.mod-ping
name: mod-ping
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, ping, xep-0199, keepalive, modules]
level: intro
status: docs-checked
description: "mod_ping in Prosody: XEP-0199 pings so clients can test their connection to the server; it has no configuration options."
sources:
  - https://prosody.im/doc/modules/mod_ping
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_ping

Lets clients check that they have a stable connection to the server by sending an XMPP ping (XEP-0199). No options or defaults.

```lua
modules_enabled = {
    "ping";
}
```

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_ping (XEP-0199, no options). Removed a generic verify line.
Method: documentation only; no commands were run.
