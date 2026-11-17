---
id: computing-software.cloud-infrastructure-engineering.calico.monitoring-kube-controllers-ipam-metrics
name: monitoring-kube-controllers-ipam-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [prometheus, metrics, kube-controllers, ipam, ipam-allocations, ippool, garbage-collection, port-9094]
level: practitioner
status: docs-checked
description: "Read the calico-kube-controllers IPAM metrics (allocations in use, borrowed, GC candidates, blocks, pool size) and their node and ippool labels on port 9094 to watch address use."
sources:
  - https://docs.tigera.io/calico/latest/reference/kube-controllers/prometheus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
kube-controllers reports Prometheus metrics by default on **port 9094**. Change or disable that through KubeControllersConfiguration. List all metrics with their help text:

```bash
curl -s http://localhost:9094/metrics | head
```

Calico-specific IPAM metrics:

| Metric | Labels | Meaning |
|---|---|---|
| `ipam_allocations_in_use` | ippool, node | Allocations currently used by a workload or interface |
| `ipam_allocations_borrowed` | ippool, node | In use but borrowed from a block with affinity to another node |
| `ipam_allocations_gc_candidates` | ippool, node | Marked by garbage collection as potential leaks; returns to zero normally |
| `ipam_allocations_gc_reclamations` | ippool, node | Counter of allocations reclaimed by GC |
| `ipam_blocks` | ippool, node | Number of IPAM blocks |
| `ipam_ippool_size` | ippool | Addresses in the pool CIDR |

Older per-node variants (`ipam_blocks_per_node`, `ipam_allocations_per_node`, `ipam_allocations_borrowed_per_node`) exist; the page says to prefer the labelled ones for new integrations.

**Labels.** `node` is the node where the allocation was made (for blocks, the node with affinity). `ippool` is the pool the block occupies, or `no_ippool` if no pool matches.

Practical reading: compare `ipam_allocations_in_use` with `ipam_ippool_size` to see pool pressure, and watch `ipam_allocations_gc_candidates` for leaks. Standard Go runtime metrics (`go_goroutines`, `go_memstats_*`) are also exported.

## Checked

2026-11-08. The Monitoring kube-controllers with Prometheus page was read in full. Port, metric names, labels and the curl check were confirmed on the Monitoring kube-controllers with Prometheus page. The pool-pressure reading is a suggested use, not page text.

Method: documentation only; no commands were run.
