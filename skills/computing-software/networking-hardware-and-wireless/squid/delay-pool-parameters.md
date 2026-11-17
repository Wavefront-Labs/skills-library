---
id: computing-software.networking-hardware-and-wireless.squid.delay-pool-parameters
name: delay-pool-parameters
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, delay-parameters, restore-maximum, bytes-per-second, delay-pools]
level: advanced
status: docs-checked
description: "Set per-class speed limits with delay_parameters using restore/maximum byte rates."
sources:
  - https://www.squid-cache.org/Doc/config/delay_parameters/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# delay_parameters
Needs `--enable-delay-pools`; no default. Each limit is `restore/maximum` in bytes per second; `none` means unlimited.

- Class 1: `delay_parameters pool aggregate`
- Class 2: `delay_parameters pool aggregate individual`
- Class 3: `delay_parameters pool aggregate network individual`
- Class 4: `delay_parameters pool aggregate network individual user`
- Class 5: `delay_parameters pool tagrate`

Examples from the page:
```
delay_parameters 1 none 8000/8000
delay_parameters 2 32000/32000 8000/8000 600/8000
delay_parameters 4 32000/32000 8000/8000 600/64000 16000/16000
```
The first limits each host in a class 2 pool to 64 Kbit/s.

## Checked

2026-11-04. Read the delay_parameters directive page and confirmed the per-class syntax, restore/maximum in bytes per second, none for no limit and the three examples. Nothing was removed.

Method: documentation only; no commands were run.
