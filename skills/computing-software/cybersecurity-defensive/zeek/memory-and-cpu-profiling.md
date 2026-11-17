---
id: computing-software.cybersecurity-defensive.zeek.memory-and-cpu-profiling
name: memory-and-cpu-profiling
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, troubleshooting, jemalloc, perf-flamegraph, state-growth]
level: advanced
status: docs-checked
description: "Diagnose Zeek memory growth with jemalloc profiling (MALLOC_CONF, jeprof) and high CPU with perf record and flame graphs, including frame-pointer build advice."
sources: ["https://docs.zeek.org/en/current/advanced/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# memory and cpu profiling

**Memory growth** may be a leak in the C++ core or script state growth, such as a global table never expired, or containers attached to long-lived connections.

jemalloc must be built with profiling. Build Zeek with `--enable-jemalloc` (optionally `--with-jemalloc=/usr/local/`), or use `LD_PRELOAD`. Verify:

```
MALLOC_CONF="stats_print:true" zeek -e 'event zeek_init() {}' 2>&1 | grep 'config.prof'
```

It must report `config.prof: true`. LD_PRELOAD and MALLOC_CONF do not work with a setuid or setcap zeek binary. Dump profiles about every 256MB of allocation:

```
MALLOC_CONF="prof:true,prof_prefix:jeprof.out,prof_final:true,lg_prof_interval:28" zeek -C -i eth0
jeprof $(which zeek) jeprof.out.*
jeprof $(which zeek) --svg jeprof.out.<pid>.* > out.svg
```

Under ZeekControl, the zeek-jemalloc plugin sets the environment; `.heap` files appear in a worker's spool directory.

**CPU**: a worker near one full core is either overloaded by packets or has a performance problem. Use perf:

```
perf record -g -p <pid>
perf script | /path/to/FlameGraph/stackcollapse-perf.pl | /path/to/FlameGraph/flamegraph.pl > out.svg
```

For pinned workers use `perf record -g -C <cpu>`. For best results build Zeek and libraries with `-fno-omit-frame-pointer` (and `--build-type=RelWithDebugInfo`), weighing a possible performance cost. FlameScope helps when processes freeze.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
