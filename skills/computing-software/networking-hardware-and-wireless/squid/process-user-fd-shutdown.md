---
id: computing-software.networking-hardware-and-wireless.squid.process-user-fd-shutdown
name: process-user-fd-shutdown
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, cache-effective-user, max-filedescriptors, shutdown-lifetime, process]
level: intro
status: docs-checked
description: "Set the run-as user, file descriptor cap and shutdown grace period with cache_effective_user, max_filedescriptors and shutdown_lifetime."
sources:
  - https://www.squid-cache.org/Doc/config/cache_effective_user/
  - https://www.squid-cache.org/Doc/config/max_filedescriptors/
  - https://www.squid-cache.org/Doc/config/shutdown_lifetime/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process user, descriptors, shutdown
- `cache_effective_user` (default `nobody`): when started as root, Squid switches real and effective user and group IDs to this account. See `cache_effective_group`.
- `max_filedescriptors`: default is the OS soft `ulimit`; set it below that or up to the hard limit. Removing the line restores the soft limit. A restart is needed, and some I/O types, such as Windows, may not support large values.
- `shutdown_lifetime` (default 30 seconds): on SIGTERM or SIGHUP Squid enters shutdown pending; clients still active after this time get a timeout message.

## Checked

2026-11-04. Read the cache_effective_user, max_filedescriptors and shutdown_lifetime directive pages and confirmed the defaults and behaviours listed. Nothing was removed.

Method: documentation only; no commands were run.
