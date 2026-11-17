---
id: computing-software.collaboration-platform-administration.matrix-synapse.ram-cpu-and-file-handle-tuning
name: ram-cpu-and-file-handle-tuning
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, performance, ram, synapse-cache-factor, jemalloc, file-descriptors, presence, limits-conf, cpu]
level: advanced
status: docs-checked
description: "Tame a slow or memory-hungry Synapse: SYNAPSE_CACHE_FACTOR, libjemalloc via LD_PRELOAD, the presence CPU workaround, and open file handle limits."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/admin_faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
First make sure you run the latest Synapse with Python 3 and a PostgreSQL database. Synapse is RAM hungry by design: it caches recent room data in memory to speed up common requests.

**Cache factor.** The `SYNAPSE_CACHE_FACTOR` environment variable defaults to 0.5. Lower it to cut RAM in constrained environments, raise it if performance degrades. Beware the trap: on machines with slow disks a low factor causes slow requests to back up, and the backlog itself explodes memory use. In that case reduce nothing; increase the factor drastically, with 2.0 a good starting value.

**jemalloc.** Preloading libjemalloc can noticeably cut overall memory use and especially improves giving RAM back to the OS. Put the library in `LD_PRELOAD` when launching Synapse. On Debian install `libjemalloc2` and add to `/etc/default/matrix-synapse`:

```
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2
```

You may also need `PYTHONMALLOC=malloc` so jemalloc can compute memory usage accurately, because Python's own small-object allocator interferes. The docs say the big gain was seen on Python 2.7 and the benefit on Python 3 is unclear.

**High CPU and presence.** A known bug with presence tracking can generate a flood of outgoing federation requests. If metrics show far more outgoing federation requests than user activity explains, disable presence in the config as a workaround.

**File handles.** Running out of file descriptors makes Synapse live-lock at 100% CPU and/or stop accepting TCP connections. Busy rooms with hundreds of servers cause the first message from your server to open connections to all of them at once, which can exhaust descriptors especially if DNS is slow. Raise the maximum open files to at least 4096 (default 1024 or 256), typically in `/etc/security/limits.conf`. Handles can also leak when inbound requests hang; match `Received request` against `Processed request` lines and look for ones taking more than a few seconds.

## Checked

Method: docs-checked 2026-11-09 against docs/usage/administration/admin_faq.md (Synapse develop branch, raw markdown, read in full).
