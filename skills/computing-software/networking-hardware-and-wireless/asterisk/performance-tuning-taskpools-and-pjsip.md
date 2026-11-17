---
id: computing-software.networking-hardware-and-wireless.asterisk.performance-tuning-taskpools-and-pjsip
name: performance-tuning-taskpools-and-pjsip
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, performance, taskpool, pjsip, timer-t1, timer-b, endpoint-identifier-order, sorcery-cache, tuning]
level: advanced
status: docs-checked
description: "Tune busy PJSIP systems: taskpool settings in pjsip.conf and stasis.conf, timer_t1 and timer_b, endpoint_identifier_order, and sorcery memory caches for realtime objects."
sources:
  - https://docs.asterisk.org/Deployment/Performance-Tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# performance tuning: taskpools and PJSIP
Poor performance is not always Asterisk's fault: load, SIP traffic mix, realtime configuration, clock speed and CPU all matter.

**Taskpool** replaced the deprecated Threadpool in 20.17.0, 22.7.0 and 23.1.0. PJSIP taskpool arrived a minor version later (20.18.0, 22.8.0, 23.2.0). Idle dynamic threads are removed after a delay; if that happens often, raise the sizes.
- `[system]` in `pjsip.conf`: `taskpool_minimum_size` (4), `taskpool_initial_size` (4), `taskpool_auto_increment` (1), `taskpool_idle_timeout` (60), `taskpool_max_size` (50, 0 = no maximum).
- `[taskpool]` in `stasis.conf`: `minimum_size`, `initial_size`, `idle_timeout_sec`, `max_size`.
Disable unused AMI, CDR and CEL modules, which can be taxing.

**Protocol timers** (`[system]`): `timer_t1` default 500 ms, minimum 100; the page says 100 is probably safe unless RTT exceeds 100 ms (250 for outlier mobile clients). `timer_b` defaults to 32 s; 6400 is fine for most installations and saves memory.

**Identification**: `endpoint_identifier_order` (default `ip,username,anonymous`) in `[global]`; put `username` first for many registering phones.

**Database storage** is slowest. Add caches in `sorcery.conf`, for example `endpoint/cache=memory_cache,maximum_objects=3000,expire_on_reload=yes,object_lifetime_maximum=900`. Flush caches or single objects with the sorcery memory cache CLI commands or the equivalent AMI commands after changing the database.

## Checked
2026-11-09: read the cited Performance Tuning page in full and confirmed the Taskpool version gates, the pjsip.conf and stasis.conf taskpool options and defaults, timer_t1 and timer_b guidance, endpoint_identifier_order and the sorcery.conf cache example. Reworded the cache flushing sentence to the page's wording (it names the commands only generally).

Method: documentation only; no commands were run.
