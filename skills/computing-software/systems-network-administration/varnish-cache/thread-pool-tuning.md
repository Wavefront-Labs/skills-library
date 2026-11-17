---
id: computing-software.systems-network-administration.varnish-cache.thread-pool-tuning
name: thread-pool-tuning
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [thread-pools, thread-pool-min, thread-pool-stack, threads-limited]
level: advanced
status: docs-checked
description: "Tune Varnish worker threads: thread_pools, thread_pool_min/max, stack size, and the counters sess_queued, sess_dropped and threads_limited that signal trouble."
sources:
  - https://www.varnish.org/docs/reference/varnishd/
  - https://www.varnish.org/docs/tutorials/varnish-monitoring/
  - https://www.varnish.org/docs/users-guide/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# thread pool tuning

Defaults and guidance from the varnishd reference:

- `thread_pools` 2 (1-32, experimental, delayed): more pools decrease lock contention, and each pool has a thread accepting new connections, so very high new-connection rates on many-core systems may need more. More than one pool per CPU is most likely detrimental. It can be increased on the fly; decreases need a restart unless the `drop_pools` experimental flag is set.
- `thread_pool_min` 100 per pool (minimum 5, strongly recommended at least 10): raising it may help ramp up faster from low load or after threads expired.
- `thread_pool_max` 5000 per pool: do not set higher than needed, as excess threads soak up RAM and CPU.
- `thread_pool_reserve` 0 = auto-tune to 5% of `thread_pool_min`, effective value at least 5; keeps vital tasks runnable under high load.
- `thread_queue_limit` 20 requests per pool (experimental): above it sessions are dropped instead of queued.
- `thread_pool_timeout` 300 s: threads above `thread_pool_min` idle this long are destroyed.
- `thread_pool_add_delay` 0: raise to a few milliseconds if `threads_failed` grows too much. If thread creation fails, check that `thread_pool_max` is not too high; raising `thread_pool_timeout` and `thread_pool_min` reduces destroy-and-recreate churn.
- `thread_pool_stack` 80k per thread.

Worst-case stack memory is on the order of `thread_pools x thread_pool_max x thread_pool_stack`, so keep stacks as small as safe.

Stack overflow: it usually shows as a segfault near the stack pointer. Varnish adds a note to the panic message (`THIS PROBABLY IS A STACK OVERFLOW - check thread_pool_stack parameter`). The troubleshooting guide says to add 128k to the current `thread_pool_stack` and restart; if crashes stop it is most likely not a bug. The varnishd manual recommends increasing in 150%-200% steps until overflows cease. Stack use is driven by GZIP (un)compression, ESI, regular expression matches, VMODs and VCL sub nesting depth.

Counters in `varnishstat` (monitoring tutorial):
- `sess_queued`: sessions queued because no thread was immediately available; consider increasing `thread_pool_min`.
- `sess_dropped`: sessions dropped because the maximum thread queue length was hit; consider increasing `thread_queue_limit`.
- `threads_limited`: times more threads were needed but the pool limit was reached.
- `threads`: total threads in use.

Verify: `varnishstat -1 -f 'MAIN.*'` prints the counters above once (`-1` prints to stdout, `-f GLOB` filters by name).

## Checked
2026-11-08. Read in full: the varnishd manual and parameter list, the Varnish monitoring tutorial and the troubleshooting page. Confirmed: defaults and guidance above. Changed: the verify command uses the filter form shown in the tutorial instead of a multi-`-f` form that is not documented there; added the manual's 150-200% stack guidance.
Method: documentation only; no commands were run.
