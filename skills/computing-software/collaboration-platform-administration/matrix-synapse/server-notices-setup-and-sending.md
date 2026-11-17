---
id: computing-software.collaboration-platform-administration.matrix-synapse.server-notices-setup-and-sending
name: server-notices-setup-and-sending
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, server-notices, send-server-notice, admin-api, motd, system-mxid-localpart, auto-join]
level: practitioner
status: docs-checked
description: "Configure the server_notices user and room in homeserver.yaml, understand the user experience, and send notices with POST or PUT /_synapse/admin/v1/send_server_notice."
sources:
  - https://element-hq.github.io/synapse/latest/server_notices.html
  - https://element-hq.github.io/synapse/latest/admin_api/server_notices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server notices give admins a channel to message users, used for policy consent and for things like a message of the day. It is Synapse specific but uses standard Matrix mechanisms, so any client works.

**User experience.** The first notice invites the user to a room, typically named "Server Notices". They cannot reject the invitation; attempts return an error. Once joined they see the notice as coming from the server notices user, and power levels stop them sending messages. They may leave, but a later notice creates a new room.

**Configuration.** Pick a user ID such as `server`, giving `@server:<your_server_name>`. It becomes a privileged user, so ensure it is not already allocated.

```yaml
server_notices:
   system_mxid_localpart: server
   system_mxid_display_name: "Server Notices"
   system_mxid_avatar_url: "mxc://example.com/oumMVlgDnLYFaPVkExemNVVZ"
   room_name: "Server Notices"
   room_avatar_url: "mxc://example.com/oumMVlgDnLYFaPVkExemNVVZ"
   room_topic: "Room used by your server admin to notice you of important information"
   auto_join: true
```

Only `system_mxid_localpart` is compulsory. `auto_join` joins users to the room instead of sending an invite.

**Sending.** Authenticate with an admin access token and call `POST /_synapse/admin/v1/send_server_notice` or `PUT /_synapse/admin/v1/send_server_notice/{txnId}`. With PUT, retransmissions using the same transaction ID are ignored, like Matrix room send. Body:

```json
{
    "user_id": "@target_user:server_name",
    "content": {
        "msgtype": "m.text",
        "body": "This is my message"
    }
}
```

Optional `type` (default `m.room.message`) and `state_key` (sends a state event). The response is `{"event_id": "<event_id>"}`. The API only works once server notices are enabled in `homeserver.yaml`.

## Checked

Method: docs-checked 2026-11-09 against docs/server_notices.md and docs/admin_api/server_notices.md (Synapse develop branch, raw markdown, both read in full).
