---
id: computing-software.networking-hardware-and-wireless.squid.client-delay-pools
name: client-delay-pools
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, client-delay-pools, bandwidth, client-delay-parameters]
level: advanced
status: docs-checked
description: "Declare client-side delay pools with client_delay_pools, which must precede the other client_delay_* options."
sources:
  - https://www.squid-cache.org/Doc/config/client_delay_pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client_delay_pools
Sets how many client delay pools Squid uses. Default 0; needs `--enable-delay-pools`. It must precede other `client_delay_*` options. Example value: 2.

The pools are then configured with `client_delay_parameters` and `client_delay_access` (see their own pages).

## Checked

2026-11-04. Read the client_delay_pools directive page and confirmed the default of 0, the build option and the ordering rule. Nothing was removed.

Method: documentation only; no commands were run.
