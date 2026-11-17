---
id: computing-software.messaging-and-integration.prosody.mod-cloud-notify
name: mod-cloud-notify
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, push, xep-0357, mobile, notifications]
level: practitioner
status: docs-checked
description: "mod_cloud_notify in Prosody: XEP-0357 push notifications for mobile clients, required companion modules, and options such as push_max_devices and push_max_errors."
sources:
  - https://prosody.im/doc/modules/mod_cloud_notify
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_cloud_notify

Implements XEP-0357 push. When a message arrives for a disconnected device, Prosody notifies the app developer's push gateway, which relays through the OS vendor so the app can wake and fetch messages. It needs `mod_smacks`, `mod_mam` and `mod_carbons` enabled to work reliably.

| Option | Default |
|---|---|
| `push_notification_important_body` | `New Message!` (empty sends no body) |
| `push_max_errors` | 16 |
| `push_max_devices` | 5 (oldest removed at limit) |
| `push_max_hibernation_timeout` | 259200 (72h) |
| `push_notification_with_body` | false |
| `push_notification_with_sender` | false |

The page advises against enabling `push_notification_with_body` without end-to-end encryption, and against `push_notification_with_sender` because it may expose contacts to the push service.

```lua
modules_enabled = { "smacks"; "mam"; "carbons"; "cloud_notify"; }
push_max_devices = 5
```

Verify: a mobile client registers push, goes to background, and a new message wakes it.

## Checked

2026-11-04. Read the mod_cloud_notify page: XEP-0357 flow through the developer's push gateway, the smacks, mam and carbons requirement, and all six options with defaults (New Message!, 16, 5, 259200, false, false) and the privacy warnings match. Nothing removed.

Method: documentation only; no commands were run.
