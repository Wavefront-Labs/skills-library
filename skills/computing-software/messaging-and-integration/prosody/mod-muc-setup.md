---
id: computing-software.messaging-and-integration.prosody.mod-muc-setup
name: mod-muc-setup
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, muc, chatrooms, component, room-creation]
level: intro
status: docs-checked
description: "Set up mod_muc multi-user chat in Prosody: the Component line, restrict_room_creation values, max_history_messages, room locking and the room cache."
sources:
  - https://prosody.im/doc/modules/mod_muc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_muc setup

```lua
Component "conference.example.com" "muc"
    name = "The example.com chatrooms server"
    restrict_room_creation = true
```

The address must differ from every other host and is usually a subdomain.

Service options:

- `name`: label shown in service discovery.
- `restrict_room_creation`: `false` anyone; `true` admins only; `"local"` users of the parent domain.
- `max_history_messages = 20`: maximum history a room can be configured to keep.
- `muc_room_locking = true` with `muc_room_lock_timeout = 300`: new rooms must be configured within 5 minutes.
- `muc_room_cache_size = 100`: rooms kept in memory; `muc_max_rooms` is a hard limit (unset by default).
- `enforce_registered_nickname = false`: force users to their reserved nickname.

Verify: a user creates a room under conference.example.com and, with `restrict_room_creation = true`, a non-admin gets a refusal.

## Checked

2026-11-04. Read the mod_muc page: the Component line and address rule, name, restrict_room_creation (false, true, "local"), max_history_messages 20, muc_room_locking with a 300 second timeout, muc_room_cache_size 100, muc_max_rooms with no default, and enforce_registered_nickname false all match. Nothing removed.

Method: documentation only; no commands were run.
