---
id: computing-software.database-administration.scylladb.kb-unresponsive-nodes-swap
name: kb-unresponsive-nodes-swap
category: computing-software
field: database-administration
product: scylladb
tags: [swap, reserve-memory, unresponsive, memory-pressure, scylla-server]
level: practitioner
status: docs-checked
description: "Diagnose ScyllaDB nodes that look down and block SSH: swap thrashing or no swap, the default 93 percent memory pre-allocation, --reserve-memory, and swap setup."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/unresponsive-nodes.rst", "https://github.com/scylladb/scylladb/blob/master/docs/kb/set-up-swap.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unresponsive nodes and swap

Symptom: ScyllaDB nodes show as down, new SSH sessions cannot be established and existing ones are slow. That usually means a node-level problem, most commonly swap:
- With swap configured, the kernel may swap out ScyllaDB memory and later access becomes very slow.
- With no swap, the kernel may loop trying to free pages it cannot, becoming a CPU hog that stalls ScyllaDB and other processes.

Resolution:
1. A healthy system should not swap. ScyllaDB pre-allocates 93% of memory by default and never exceeds it, leaving 7% for the OS and other tasks. Move non-essential processes to other machines; if they are essential and the 7% is not enough, raise the reservation.
2. Having swap enabled and unused beats needing swap and not having it: configure swap for production.

Raise the reservation by adding `--reserve-memory 10G` (example) to the scylla command line in `/etc/sysconfig/scylla-server` (RHEL) or `/etc/default/scylla-server` (Debian).

Swap setup: `scylla_setup` runs `scylla_swap_setup`, or run it directly (`--swap-directory`, `--swap-size` in GB). Manual file method, size = the lower of total_mem/3 and 16 GB (18 GB RAM gives 6 GB, 240 GB gives 16 GB):

```
sudo fallocate -l 6G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
sudo swapon --show
```

## Checked

2026-11-04: symptoms, the 93 percent default pre-allocation, the reservation file paths, scylla_swap_setup options and the swap file procedure and sizing rule confirmed against the ScyllaDB unresponsive-nodes and set-up-swap knowledge-base pages.

Method: documentation only; no commands were run.
