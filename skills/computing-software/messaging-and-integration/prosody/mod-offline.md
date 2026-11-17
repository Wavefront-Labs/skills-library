---
id: computing-software.messaging-and-integration.prosody.mod-offline
name: mod-offline
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, offline-messages, storage, modules]
level: intro
status: docs-checked
description: "mod_offline in Prosody: loaded automatically, stores messages for offline users, needs no options, and what happens when you disable it."
sources:
  - https://prosody.im/doc/modules/mod_offline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_offline

Stores messages for offline users and delivers them at next login. It is loaded automatically and needs no configuration. It implements XEP-0160, XEP-0203 and XEP-0091 (older clients).

To turn it off:

```lua
modules_disabled = {
   "offline";
}
```

If nothing else handles offline messages, messages to offline users are returned to the sender with a "service unavailable" error.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_offline. Removed a generic verify line.
Method: documentation only; no commands were run.
