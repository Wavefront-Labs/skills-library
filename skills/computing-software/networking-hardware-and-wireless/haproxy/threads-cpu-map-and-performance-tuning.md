---
id: computing-software.networking-hardware-and-wireless.haproxy.threads-cpu-map-and-performance-tuning
name: threads-cpu-map-and-performance-tuning
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, nbthread, cpu-map, thread-groups, performance-tuning, tune-bufsize]
level: practitioner
status: docs-checked
description: "Tune HAProxy with nbthread, cpu-map, thread-groups, tune.bufsize and the SSL session cache, and read Idle_pct to see whether CPU is the limit."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# threads cpu map and performance tuning
```
global
    nbthread 8
    cpu-map auto:1/1-8 0-7
    tune.ssl.cachesize 200000
```
- `nbthread <number>`: on platforms with CPU affinity the default is the number of CPUs the process is bound to at startup (so `taskset` or `cpuset` from the caller adjusts it); otherwise it defaults to 1. The default appears in `haproxy -vv`. Values are capped by `thread-hard-limit`, which wins over a higher `nbthread` and warns; `nbthread` above the CPUs available gives a warning and bad performance.
- `thread-groups <number>` splits threads into independent groups (default 1) to reduce contention at the cost of configuration effort, and is the only way to use more than 64 threads (64 per group; the maximum group count is set at compile time, default 16). `thread-group <group> [<thread-range>...]` assigns threads to a group explicitly.
- `cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...]` pins threads to CPUs. Without thread groups a thread range needs the `1/` prefix, and `1` equals `1/all`. A range accepts `all`, `odd`, `even` or `number[-[number]]`. With `auto:` both sets must have the same size and HAProxy binds threads to CPUs in order, for example `cpu-map auto:1/1-4 0-3`. A later `cpu-map` replaces earlier ones where they overlap.
- Management guide advice for network-bound loads: interrupts and HAProxy compete when on the same CPU. Pin HAProxy (with `taskset` or `cpu-map`) and the interrupts under `/proc/irq` to different cores that share the same L3 cache, spread multi-queue NIC interrupts over a few such cores, and stop `irqbalance`. Unloading a stateful firewall or conntrack can show whether it is a bottleneck.
- `tune.bufsize` (default 16384 bytes): the manual strongly recommends not changing it. Larger values increase memory use, so lower global `maxconn` by the same factor; HTTP/2 requires at least 16384. An HTTP request larger than `tune.bufsize - tune.maxrewrite` gets a 400 and a response larger than `tune.bufsize` gets a 502.
- `tune.ssl.cachesize` sets the SSL session cache size in blocks (about 200 bytes each; default 20000; 0 disables the cache). When full, the most idle entries are purged; larger caches reduce CPU-intensive handshakes. All entries are preallocated at startup.
- `tune.ssl.default-dh-param` caps the DH parameter size for DHE (1024 or more; higher costs more CPU). Without it, or a DH file, and with no DH parameters in the PEM file, DHE ciphers are unavailable for that frontend.
- Measure with `show info`: `Idle_pct` is the share of time spent waiting in poll() against processing. Near 100 means a very low load; near 0 means constant activity. A low idle with low load suggests expensive rules, and a high idle with slow responses means HAProxy is just waiting on data. Other fields include `Tasks`, `Run_queue`, `CurrConns` and `CumReq`. `show activity` reports developer-oriented per-thread counters whose fields are deliberately undocumented.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual (`nbthread`, `thread-groups`, `thread-group`, `thread-hard-limit`, `cpu-map`, `tune.bufsize`, `tune.ssl.cachesize`, `tune.ssl.default-dh-param`) and management guide (idle ratio and CPU pinning text, `show info` field names, `show activity`). Removed: the `nbproc` removal claim, kernel sysctl values, `LimitNOFILE` sizing, ephemeral-port exhaustion, `ssl-default-bind-options no-tls-tickets`, ECDSA and `tune.ssl.ocsp-update` advice, `show pools` memory comparison, and the `wrk`/`h2load` load-test verification. Read as sections of both documents only.
Method: documentation only; no commands were run.
