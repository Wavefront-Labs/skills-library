---
id: computing-software.systems-network-administration.cisco-networking.store-and-forward-vs-cut-through-switching
name: store-and-forward-vs-cut-through-switching
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, switching, cut-through, store-and-forward, fragment-free, switching-latency, crc-errors, nexus, catalyst]
level: practitioner
status: draft
description: "Choose and reason about store-and-forward vs cut-through switching: latency, CRC error propagation, speed mismatches and how Catalyst and Nexus behave."
sources:
  - https://www.cisco.com/c/en/us/products/collateral/switches/nexus-5020-switch/white_paper_c11-465436.html
  - https://www.cisco.com/c/en/us/support/docs/switches/nexus-9000-series-switches/216239-nexus-9000-cloud-scale-asic-crc-identifi.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Store-and-forward vs cut-through switching

## The modes
| Mode | Forwards after | Latency | Bad frames |
|---|---|---|---|
| Store-and-forward | whole frame received, FCS checked | serialisation of full frame + lookup | dropped at ingress |
| Cut-through | destination MAC/headers read | constant, low (sub-us on DC ASICs) | forwarded; FCS stomped at egress |
| Fragment-free | first 64 bytes (legacy, collision era) | between | runts dropped |

Catalyst campus switches (2960/3850/9000) are store-and-forward. Nexus 3000/5000/9000 and
many DC ASICs default to cut-through where speeds allow.

## When cut-through actually happens
- Only when ingress speed >= egress speed and the egress queue is empty. Slow-to-fast
  (10G in, 40G out) or a congested egress falls back to store-and-forward.
- So "cut-through latency" only appears on uncongested, same-speed or fast-to-slow paths.

## CRC error propagation (the operational gotcha)
A frame with a bad FCS is already partly transmitted when detected, so the switch "stomps" the
FCS on egress. Every downstream port then counts a CRC error, and the real source is upstream.
On Nexus 9000:
```
show interface counters errors
show interface Eth1/1 | include CRC|Stomped
```
Find the port with **input CRC but zero stomped CRC**: that is the origin (dirty fibre, bad optic).
Stomped-only ports are just relaying the damage.

## Choosing
- Latency-critical DC/HFT fabrics: cut-through, with good optics and monitoring.
- Campus/edge: store-and-forward is fine; latency is dominated by queuing, not mode.

## Verify
- [ ] Know which mode each platform in a CRC-error path runs before blaming the reporting port.
