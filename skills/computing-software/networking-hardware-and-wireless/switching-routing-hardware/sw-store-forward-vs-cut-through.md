---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-store-forward-vs-cut-through
name: sw-store-forward-vs-cut-through
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [switch-cut-through, switch-buffers-oversubscription, switch-latency]
level: advanced
status: draft
description: "Understand switching modes, buffer depth and oversubscription ratios to pick switches for latency or burst-heavy workloads."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Switching modes, buffers, oversubscription

- Store-and-forward receives the whole frame, checks FCS, then forwards; cut-through begins forwarding after reading the header. Cut-through lowers latency but may forward corrupted frames; many data-centre switches support both.
- Shallow buffers suit uniform traffic; incast patterns (many senders to one receiver) need deeper buffers or ECN/QoS tuning.
- Oversubscription = total downstream capacity / uplink capacity. Access layers at 20:1 or higher are common for office networks; data-centre leaf layers typically aim for 3:1 or better, based on the workload.
- Check backplane and forwarding rate (Mpps) in datasheets; a switch can have line-rate ports but a lower non-blocking figure.

## Verify
- [ ] Interface drop counters (output queue drops) stay near zero at peak under realistic load.
