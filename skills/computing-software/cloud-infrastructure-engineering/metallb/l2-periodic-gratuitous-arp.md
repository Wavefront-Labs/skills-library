---
id: computing-software.cloud-infrastructure-engineering.metallb.l2-periodic-gratuitous-arp
name: l2-periodic-gratuitous-arp
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, gratuitous-arp, fdb-aging, gratuitous-arp-interval, layer2, speaker, helm]
level: advanced
status: docs-checked
description: "Fix periodic L2 packet loss caused by switch FDB aging by making the MetalLB speaker re-send gratuitous ARP/NDP at a fixed interval, and how to pick the interval."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/layer2.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Periodic gratuitous ARP/NDP

Default: gratuitous ARP/NDP is sent only on failover. MetalLB still replies to ARP requests and NDP Neighbor Solicitations for announced VIPs.

Symptom: in some environments, such as switches that age FDB entries faster than upstream gateways age their ARP cache, service IPs see periodic packet loss with no leadership change, because nothing refreshes the switch forwarding table between failovers.

Fix: make the speaker re-emit gratuitous ARP/NDP for every announced IP on a fixed interval:
- speaker flag `--gratuitous-arp-interval`, or
- Helm value `speaker.gratuitousARPInterval`.

The value is in seconds. `0` (default) keeps failover-only behaviour.

Gotchas:
- The interval is speaker-wide: it applies to every L2-announced IP on the node.
- Very short intervals on speakers announcing many IPs over many interfaces create noticeable broadcast traffic and slow the speaker's handling of service updates.
- Rule of thumb from the docs: pick the largest interval that is still shorter than the switch's FDB aging time.

## Checked
2026-11-04. Confirmed against the MetalLB "layer 2 mode" page, "Periodic gratuitous announcements": flag, Helm value, seconds, default 0, speaker-wide scope, broadcast and slowdown warning, rule of thumb. Removed a generic verify line.
Method: documentation only; no commands were run.
