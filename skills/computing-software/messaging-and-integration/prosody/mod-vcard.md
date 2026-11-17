---
id: computing-software.messaging-and-integration.prosody.mod-vcard
name: mod-vcard
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, vcard, xep-0054, avatars, muc]
level: intro
status: docs-checked
description: "mod_vcard in Prosody: XEP-0054 user vCards, room avatars on MUC hosts, and the optional vcard_store_name override that should stay at default."
sources:
  - https://prosody.im/doc/modules/mod_vcard
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_vcard

Implements XEP-0054 so users can publish contact information in a vCard, as much or as little as they like. On MUC hosts it also lets room owners set a room picture. Participant avatars do not depend on it.

```lua
modules_enabled = { "vcard"; }
```

No configuration is required. `vcard_store_name` can override the data store name; the right name is detected automatically and the docs recommend leaving it at the default.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_vcard. Removed a generic verify line.
Method: documentation only; no commands were run.
