---
id: computing-software.messaging-and-integration.prosody.mod-muc-mam
name: mod-muc-mam
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, muc, mam, room-history, archive]
level: practitioner
status: docs-checked
description: "mod_muc_mam in Prosody: archive MUC room messages with muc_log_by_default, muc_log_presences, log_all_rooms, muc_log_expires_after and cleanup interval."
sources:
  - https://prosody.im/doc/modules/mod_muc_mam
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_muc_mam

Archives messages in rooms of a MUC component. Load it on the component:

```lua
Component "rooms.example.net" "muc"
modules_enabled = { "muc_mam" }
```

Since 13.0.4 it loads automatically when `mod_mam` is enabled globally or on the component; put it in the component's `modules_disabled` to stop that.

Example values shown on the page:

```lua
muc_log_by_default = true
muc_log_presences = false
log_all_rooms = false
muc_log_expires_after = "1w"
muc_log_cleanup_interval = 4 * 60 * 60
```

- `muc_log_by_default`: archiving on for new rooms; owners can change it.
- `muc_log_presences`: also archive joins and parts.
- `log_all_rooms = true`: force logging and remove the room option.
- `muc_log_expires_after` / `muc_log_cleanup_interval` behave like the mod_mam options.

Verify: join a room, post, rejoin from another client and fetch history.

## Checked

2026-11-04. Read the mod_muc_mam page: the component modules_enabled line, automatic loading since 13.0.4 and the modules_disabled opt-out, and the five option values with their meanings (log_all_rooms forcing logging and disabling the room option) match. Removed the claim that the store is named muc_log, which the page does not state.

Method: documentation only; no commands were run.
