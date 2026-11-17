---
id: computing-software.messaging-and-integration.prosody.mod-blocklist
name: mod-blocklist
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, blocking, xep-0191, privacy, modules]
level: intro
status: docs-checked
description: "mod_blocklist in Prosody: XEP-0191 contact blocking, bounce_blocked_messages default false, and blocklist_cache_size default 64."
sources:
  - https://prosody.im/doc/modules/mod_blocklist
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_blocklist

Implements XEP-0191 so users can block specific users from contacting them, provided their clients support it.

```lua
modules_enabled = { "blocklist"; }
bounce_blocked_messages = false
blocklist_cache_size = 64
```

- `bounce_blocked_messages` defaults to false.
- `blocklist_cache_size`: by default Prosody keeps an in-memory cache of the blocklists of up to 64 users.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_blocklist (XEP-0191, both options and defaults). Removed the description of what bounce does and a generic verify line, which the page does not state.
Method: documentation only; no commands were run.
