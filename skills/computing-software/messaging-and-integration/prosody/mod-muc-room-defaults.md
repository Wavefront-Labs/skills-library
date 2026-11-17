---
id: computing-software.messaging-and-integration.prosody.mod-muc-room-defaults
name: mod-muc-room-defaults
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, muc, room-defaults, tombstones, persistence]
level: practitioner
status: docs-checked
description: "Default settings for new Prosody MUC rooms: muc_room_default_* options, history length, persistence, and tombstones that stop destroyed rooms being recreated."
sources:
  - https://prosody.im/doc/modules/mod_muc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MUC room defaults and tombstones

Settings that influence the defaults for newly created rooms, set on the MUC component. The values shown are the defaults used if the option is not present in the config:

```lua
Component "conference.example.com" "muc"
    muc_room_default_public = true
    muc_room_default_persistent = false
    muc_room_default_members_only = false
    muc_room_default_moderated = false
    muc_room_default_public_jids = false
    muc_room_default_change_subject = false
    muc_room_default_history_length = 20
    muc_room_default_language = "en"
```

Each room has its own configuration, which room owners can change with supporting clients.

When a room is destroyed it leaves behind a tombstone, which prevents the room being entered or recreated. It lets anyone who was not in the room learn about the destruction and update bookmarks, and prevents someone recreating a previously semi-anonymous room to learn the real JIDs of its regulars. Two settings:

```lua
muc_tombstones = true            -- false disables the behaviour
muc_tombstone_expiry = 86400 * 31 -- default 31 days; after this the room can be created again
```

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_muc (room configuration defaults, tombstone behaviour and both tombstone settings). Removed a generic verify line.
Method: documentation only; no commands were run.
