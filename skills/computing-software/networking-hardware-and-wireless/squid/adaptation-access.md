---
id: computing-software.networking-hardware-and-wireless.squid.adaptation-access
name: adaptation-access
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, adaptation-access, icap, ecap, service-activation]
level: advanced
status: docs-checked
description: "Activate ICAP or eCAP services for matching transactions with adaptation_access, first match wins."
sources:
  - https://www.squid-cache.org/Doc/config/adaptation_access/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# adaptation_access
Needs `--enable-ecap` or `--enable-icap-client`. Sends HTTP transactions to an adaptation service.

- Default: allow, unless rules exist in squid.conf.
- Rules are checked in file order; the first match stops processing.
- Allow uses the named service; deny activates none.
- Services for other vectoring points, or broken-but-bypassable ones, are skipped.
- Only one service per vectoring point can apply to a transaction.
```
adaptation_access service_1 allow all
```

## Checked

2026-11-04. Read the adaptation_access directive page and confirmed the build options, default, first-match rule, skipped services and the one-service-per-vectoring-point limit. Nothing was removed.

Method: documentation only; no commands were run.
