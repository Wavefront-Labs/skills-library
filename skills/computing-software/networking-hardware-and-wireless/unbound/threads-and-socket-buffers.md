---
id: computing-software.networking-hardware-and-wireless.unbound.threads-and-socket-buffers
name: threads-and-socket-buffers
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, num-threads, so-reuseport, so-rcvbuf, outgoing-range, performance-tuning]
level: advanced
status: draft
description: "Scale Unbound on busy servers: num-threads, so-reuseport, outgoing-range, num-queries-per-thread and UDP socket buffer sizes with their OS limits."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/performance.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# threads and socket buffers
The guide says most installations need no tuning; these are for large resolvers.

- `num-threads`: set to the number of CPU cores.
- `so-reuseport: yes`: on Linux noticeably improves UDP performance; `unbound-control status` shows whether it is active.
- `outgoing-range`: as high as possible. Without libevent the guide suggests about 950 with 1 core, 450 with 2, 200 with 4 (formula 1024/cores minus 50).
- `num-queries-per-thread`: about half of `outgoing-range`.
- `so-rcvbuf`: 4m or 8m on busy servers to reduce drops during spikes. Linux caps it, so raise `net.core.rmem_max`; Unbound needs root to bypass the cap.
- `so-sndbuf`: typically 4m to 8m; raise `net.core.wmem_max` if needed.

Check for overruns with `netstat -su` (`RcvbufErrors` and `SndbufErrors`). BSD uses `kern.ipc.maxsockbuf`; Solaris uses `ndd`.

Watch `requestlist.overwritten` and `requestlist.exceeded` counters for queries replaced or dropped.
