---
id: computing-software.systems-network-administration.network-design.microburst-detection
name: microburst-detection
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-performance, microburst, output-drops, buffers, incast, telemetry, sub-second-monitoring]
level: practitioner
status: docs-checked
description: "Find microbursts that drop packets on links that look idle in 5-minute graphs: sub-second counters, buffer telemetry, incast patterns, and fixes via buffers, QoS or speed."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/nexus-9000-series-switches/218121-understand-microburst-detection-on-nexu.html
  - https://www.arista.com/en/um-eos/eos-latency-analyzer-lanz
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microburst detection

A lightly loaded link can still drop packets: for a few milliseconds many
senders transmit at once and the egress buffer overflows. 5-minute (or even 1-minute) averages
hide it completely.

## Symptoms
- Output drops increasing on a port with low average utilisation.
- TCP retransmissions and application latency spikes at regular moments (backups, map-reduce
  shuffles, storage replication, market data opens).
- Typical topology: many-to-one (incast), speed change (10G/25G into 1G), or uplink oversubscription.

## Measure at the right resolution
1. Counters: poll output drops and bytes every second (streaming telemetry or a script that polls interface counters); look for drop increments coinciding with spikes.
2. Platform features:
   - Arista: LANZ (latency analyzer) monitors output queue lengths per interface and reports congestion events (system log messages, streamed data).
   - Other platforms: look for per-queue drop counters and microburst or buffer monitoring in the vendor documentation.
3. Packet capture with precise timestamps at the egress (TAP + capture appliance) and an IO graph at
   1 ms intervals.

## Fixes (in order of cost)
- Increase buffer share for the port/queue (platform-specific queue and buffer settings).
- QoS: separate bursty bulk traffic into its own queue so latency-sensitive flows are not dropped.
- Spread load: ECMP, more uplinks, move bursty servers across leaves.
- Application tuning: stagger jobs, limit parallelism, enable pacing.
- Speed up the bottleneck link (1G to 10G, 10G to 25G).

## Verify
- [ ] Sub-second monitoring shows drop increments disappear during the bursty workload after the fix.

## Checked

- Date: 2026-10-28
- Confirmed: Arista LANZ guide: LANZ monitors output queue lengths per interface, supports early detection of microbursts and reports congestion events as log messages and streamed data.
- Removed: Nexus and Catalyst commands and settings (Cisco Nexus page returned 404), the 10G/15 % example, Linux fq qdisc.
Method: documentation only; no commands were run.
