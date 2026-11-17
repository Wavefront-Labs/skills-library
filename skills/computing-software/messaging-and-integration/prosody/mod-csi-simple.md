---
id: computing-software.messaging-and-integration.prosody.mod-csi-simple
name: mod-csi-simple
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, csi, xep-0352, mobile, battery, traffic]
level: practitioner
status: docs-checked
description: "mod_csi_simple in Prosody: buffer unimportant stanzas for inactive clients; csi_queue_size 256, csi_resume_inactive_delay 5, and csi_important_payloads."
sources:
  - https://prosody.im/doc/modules/mod_csi_simple
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_csi_simple

Reduces traffic to clients that report inactive (Client State Indication, XEP-0286 as cited by the page). Unimportant stanzas such as presence changes are buffered and released when important traffic arrives, the queue fills, or (0.12.0+) the client sends traffic. It loads `mod_csi` itself; enable only `csi_simple`.

| Option | Default |
|---|---|
| `csi_important_payloads` | empty (0.12+) |
| `csi_queue_size` | 256 |
| `csi_resume_inactive_delay` | 5 seconds (0.12+) |

```lua
modules_enabled = { "csi_simple"; }
csi_important_payloads = {
    "{urn:example:important-namespace}",
    "{urn:example:xmpp:priority}super-important",
}
```

Verify: an inactive mobile client receives batched presence while a message still arrives at once.

## Checked

2026-11-04. Read the mod_csi_simple page: buffering of unimportant traffic released on important data or a full queue, automatic loading of mod_csi, csi_important_payloads (0.12, empty), csi_queue_size 256, csi_resume_inactive_delay 5 (0.12), the payload syntax examples, and the 0.12.0 flush on incoming client traffic all match. Nothing removed.

Method: documentation only; no commands were run.
