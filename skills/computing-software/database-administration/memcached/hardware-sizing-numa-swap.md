---
id: computing-software.database-administration.memcached.hardware-sizing-numa-swap
name: hardware-sizing-numa-swap
category: computing-software
field: database-administration
product: memcached
tags: [hardware, numa, swap, ram, network]
level: practitioner
status: docs-checked
description: "Size hardware for memcached: light CPU, RAM-bound, no swap, uniform node size, NUMA binding with numactl, and network needs."
sources:
  - https://docs.memcached.org/serverguide/hardware/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Supported: 32-bit and 64-bit x86 and ARM; many operating systems (Linux, BSDs, various unix); no official support for Windows.
- CPU: typically light; multithreaded, defaulting to 4 worker threads; most installations only need a single memcached thread.
- RAM: the more the better, but do not take memory away from other services that might benefit. Roughly the same memory per server means you can add and remove servers without caring about a server's particular weight.
- Swap: assign physical memory with a few percent extra; do not over-allocate and expect swap to save you, performance will be very poor. Monitor swap use. Often a good idea to run hosts with very little swap or none: better to let an active service die than turn into a tarpit.
- High speed RAM is unlikely to give measurable benefits.
- NUMA: okay under normal loads; there is a measurable drop under benchmarking when running across multiple NUMA nodes. If extremely sensitive, run one instance per NUMA node and bind the instances via numactl or similar.
- Network: depends on average item size, so keep items small. Most deployments have low requirements (< 10mbps per instance).

Layouts: spare memory on webservers spreads the loss (but adds maintenance, multi-get fan-out to every server, and a risk of swap or killing memcached if the app leaks memory); running on database hosts is "not a great idea"; dedicated hosts (64G+) mean fewer machines but more pain when one dies.

## Checked

2026-11-04. Confirmed against the Hardware and Instances page. Removed: the closing Verify line (`free -m`, `numactl --hardware`), which the page does not give.

Method: documentation only; no commands were run.
