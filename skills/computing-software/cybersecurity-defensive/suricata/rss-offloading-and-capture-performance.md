---
id: computing-software.cybersecurity-defensive.suricata.rss-offloading-and-capture-performance
name: rss-offloading-and-capture-performance
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [rss, nic-offloading, symmetric-hash, ethtool]
level: advanced
status: docs-checked
description: "Prepare NICs for IDS capture: RSS queue count and symmetric hashing, disabling LRO and GRO, checksum offload rules per capture method."
sources: ["https://docs.suricata.io/en/latest/performance/packet-capture.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RSS and offloading

Suricata performs best in workers mode; both directions of a flow must reach the same thread in order.

## RSS
Standard RSS is usually asymmetric, so directions can land in different queues and Suricata may see a SYN/ACK long after client data. Check queues with `ethtool -l`. Options: reduce to one queue (usual advice, for example `ethtool -L $DEV combined 1`), use symmetric hash, or a special random key. Some Intel drivers cannot yet enable symmetric mode, and wrong i40e changes can cause kernel panics.

## Offloading
Disable most NIC, driver and kernel acceleration. LRO and GRO break `dsize` and TCP state tracking. Checksum offload can stay on for AF_PACKET and PF_RING but must be off for PCAP, Netmap and others.

## By method
- AF_PACKET: one queue (or symmetric RSS with `cluster_qm`).
- PF_RING: one queue with `cluster_flow`.
- Netmap: one queue, or the `lb` tool or autofp.

## Checked

Method: docs-checked 2026-11-09 against https://docs.suricata.io/en/latest/performance/packet-capture.html (read in full).
