---
id: computing-software.messaging-and-integration.prosody.mod-carbons
name: mod-carbons
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, carbons, xep-0280, multi-device, modules]
level: intro
status: docs-checked
description: "mod_carbons in Prosody: XEP-0280 message carbons to sync conversations across a user's online clients, no options, and why to pair it with mod_mam."
sources:
  - https://prosody.im/doc/modules/mod_carbons
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_carbons

Implements XEP-0280 Message Carbons: users keep a shared and synchronized view of all conversations across all their online clients and devices.

Enable by adding it to the module list:

```lua
modules_enabled = {
    -- other modules ...
    "carbons";
}
```

The module has no further configuration.

Limits: it only synchronizes conversations with clients that are connected at the time of the conversation and that support XEP-0280. For clients that may be offline at the time, additionally use mod_mam to store conversations on the server.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_carbons. Removed a generic verify line the page does not state.
Method: documentation only; no commands were run.
