---
id: computing-software.messaging-and-integration.prosody.mod-smacks
name: mod-smacks
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, smacks, xep-0198, stream-management, resumption]
level: practitioner
status: docs-checked
description: "mod_smacks in Prosody: XEP-0198 stream management, hibernation time 600s, queue size 500, ack delay, s2s resend and old-session settings."
sources:
  - https://prosody.im/doc/modules/mod_smacks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_smacks

Implements XEP-0198 Stream Management so a client can resume a dropped session without losing stanzas. Both ends queue recent stanzas until acknowledged. A disconnected session "hibernates"; if the client does not return in time it goes offline, messages go to offline storage (needs `mod_offline`) and other stanzas get recipient-unavailable.

| Option | Default |
|---|---|
| `smacks_hibernation_time` | 600 (seconds resumable) |
| `smacks_max_queue_size` | 500 unacked stanzas |
| `smacks_enabled_s2s` | true |
| `smacks_s2s_resend` | false (experimental) |
| `smacks_max_unacked_stanzas` | 0 |
| `smacks_max_ack_delay` | 30 seconds |
| `smacks_max_old_sessions` | 10 |

```lua
smacks_hibernation_time = 600
smacks_max_queue_size = 500
```

Verify: kill a client's network for less than the hibernation time and reconnect; the stream resumes with no lost messages.

## Checked

2026-11-04. Read the mod_smacks page: XEP-0198 queues and resumption, hibernation then offline storage or recipient-unavailable (mod_offline needed), and all seven options with defaults (600, 500, true, false, 0, 30, 10) match. Nothing removed.

Method: documentation only; no commands were run.
