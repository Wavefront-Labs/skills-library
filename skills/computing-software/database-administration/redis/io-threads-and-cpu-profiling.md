---
id: computing-software.database-administration.redis.io-threads-and-cpu-profiling
name: io-threads-and-cpu-profiling
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, io-threads, redis-performance, cpu-profiling, perf, redis-latency]
level: practitioner
status: docs-checked
description: "Configure Redis I/O threads for network-bound workloads, measure whether they help, and profile CPU hot spots on the main thread with perf and flame graphs."
sources:
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/cpu-profiling/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# I/O threads and CPU profiling

**Goal:** know whether Redis is CPU-bound on command execution (single main thread) or on socket I/O (parallelisable), and act on evidence.

## I/O threads
```text
io-threads 4                  # example from redis.conf; 1 = main thread only
# io-threads-do-reads is in the 7.0 redis.conf (default no) and absent from the 8.2 one,
# where enabled I/O threads also handle reads and protocol parsing
```
- redis.conf: enable only if you actually have performance problems and Redis uses a large share of CPU time on socket I/O.
- Does not speed up slow commands (Lua, big `ZRANGE`): command execution stays on the main thread.
- redis.conf (8.2): use machines with at least 4 cores and leave one spare; 4 cores → 3 I/O threads, 8 cores → 7. The 7.0 file suggested 2-3 and 6 and said more than 8 is unlikely to help.

## Measure
```bash
redis-benchmark -h host -t set,get -n 2000000 -c 200 -P 1 --threads 4 -q
```
Compare ops/s and p99 with `io-threads 1` vs N, running the benchmark from another host; redis.conf says to run redis-benchmark with `--threads` matching the Redis thread count, otherwise you will not see the speedup. Watch per-thread CPU with `top -H -p $(pidof redis-server)`.

## CPU profiling the main thread
```bash
perf record -g --pid $(pidof redis-server) -F 999 -- sleep 60
perf report --no-children --sort comm,symbol
# flame graph
perf script | stackcollapse-perf.pl | flamegraph.pl > redis.svg
```
Stack traces need debug information: the Redis profiling guide builds with `make REDIS_CFLAGS="-g -fno-omit-frame-pointer"` and keeps `-O2`.

## Other CPU sinks
- `INFO commandstats` shows per-command statistics.
- TLS adds CPU overhead; I/O threading with TLS is supported from Redis 8.0.
- Active defrag and expiry cycles consume CPU (`hz`, `active-defrag-cycle-max`).

## Verify
After a change, `INFO cpu` (`used_cpu_sys_main_thread`, `used_cpu_user_main_thread`) and benchmark p99 improve under the same load.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from redis.conf 8.2 and 7.0: the THREADED I/O comments (at least 4 cores, leave one spare, 3 threads for 4 cores and 7 for 8 in 8.2; 2-3 and 6 in 7.0), io-threads-do-reads present in 7.0 and absent in 8.2, reads and parsing threaded when enabled, `--threads` advice for redis-benchmark; redis-benchmark usage (`--threads`, `-P`, `-c`, `-n`, `-t`, `-q`, `-h`); the CPU profiling guide (`perf record -g --pid ... -F 999 -- sleep 60`, perf script + stackcollapse-perf.pl + flamegraph.pl, `-g -fno-omit-frame-pointer`); INFO fields `used_cpu_sys_main_thread` and `used_cpu_user_main_thread`; TLS I/O threading since 8.0. Removed unconfirmed: the 100k ops/s guideline, restart requirement, thread names, typical hot symbols, usec_per_call.
Method: documentation only; no commands were run.
