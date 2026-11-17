---
id: computing-software.networking-hardware-and-wireless.squid.quick-abort-retrieval
name: quick-abort-retrieval
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, quick-abort, aborted-downloads, cache-fill]
level: advanced
status: docs-checked
description: "Decide whether Squid finishes a cacheable download after the client aborts using quick_abort_min, max and pct."
sources:
  - https://www.squid-cache.org/Doc/config/quick_abort_min/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# quick_abort
- `quick_abort_min` (default 16 KB): if less than this remains, Squid finishes the retrieval.
- `quick_abort_max`: if more than this remains, Squid aborts.
- `quick_abort_pct`: if more than this percentage is done, Squid finishes.

Setting min and max to 0 KB stops retrievals continuing after an abort; min of -1 KB makes cacheable retrievals always continue. Other factors, such as an unknown body length, also matter.

## Checked

2026-11-04. Read the quick_abort_min directive page and confirmed the 16 KB default, the min, max and pct rules, the 0 KB and -1 KB settings and the unknown-length note. Nothing was removed.

Method: documentation only; no commands were run.
