---
id: computing-software.messaging-and-integration.prosody.mod-pep
name: mod-pep
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, pep, pubsub, caches, modules]
level: practitioner
status: docs-checked
description: "mod_pep in Prosody: personal eventing with pep_max_items 256 and the pep_service_cache_size and pep_info_cache_size memory caches."
sources:
  - https://prosody.im/doc/modules/mod_pep
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_pep

Enable with `"pep";` in `modules_enabled`.

| Option | Default | Meaning |
|---|---|---|
| `pep_max_items` | 256 | Cap on items a PEP node can be configured to keep |
| `pep_service_cache_size` | 1000 | User PubSub services kept in memory (0.11.11+) |
| `pep_info_cache_size` | 10000 | Cache of which events entities are interested in (0.11.11+) |

```lua
pep_max_items = 256
```

Raise the cache sizes on servers with many active users if memory allows; lower them to save memory.

Verify: a client can publish and read PEP data such as an avatar or nickname.

## Checked

2026-11-04. Read the mod_pep page: XEP-0163 on the PubSub library, pep_max_items 256, pep_service_cache_size 1000 and pep_info_cache_size 10000 both added in 0.11.11, and the cache sizing advice match. Removed the claim that the stores are named pep and pep_data, which the page does not state.

Method: documentation only; no commands were run.
