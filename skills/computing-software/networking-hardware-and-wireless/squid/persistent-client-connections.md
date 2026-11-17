---
id: computing-software.networking-hardware-and-wireless.squid.persistent-client-connections
name: persistent-client-connections
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, persistent-connections, keep-alive, client-connections]
level: intro
status: docs-checked
description: "Keep client connections open between requests with client_persistent_connections, default on."
sources:
  - https://www.squid-cache.org/Doc/config/client_persistent_connections/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client_persistent_connections
Controls whether Squid keeps persistent connections with clients when allowed. Default `on`; it can be disabled.

## Checked

2026-11-04. Read the client_persistent_connections directive page and confirmed the default of on. Nothing was removed.

Method: documentation only; no commands were run.
