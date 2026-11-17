---
id: computing-software.networking-hardware-and-wireless.squid.ecap-service
name: ecap-service
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, ecap, ecap-service, content-adaptation]
level: sme
status: docs-checked
description: "Declare an eCAP adaptation service with ecap_service: vectoring point, URI and bypass option."
sources:
  - https://www.squid-cache.org/Doc/config/ecap_service/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ecap_service
Needs `--enable-ecap`. Syntax: `ecap_service id vectoring_point uri [option ...]`.

- `*_postcache` vectoring points are not yet supported.
- Services are mandatory by default; `bypass=on` makes one optional.
- Dynamic routing is off unless enabled.
- Activate with `adaptation_access`.
```
ecap_service s1 reqmod_precache ecap://filters.R.us/leakDetector?on_error=block bypass=off
```

## Checked

2026-11-04. Read the ecap_service directive page and confirmed the syntax, build option, postcache note, bypass and routing defaults and the example. Nothing was removed.

Method: documentation only; no commands were run.
