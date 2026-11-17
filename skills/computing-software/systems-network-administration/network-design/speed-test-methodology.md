---
id: computing-software.systems-network-administration.network-design.speed-test-methodology
name: speed-test-methodology
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-performance, speed-test, throughput-testing, iperf3, isp-performance]
level: practitioner
status: docs-checked
description: "Run speed tests that mean something: wired vs Wi-Fi, single vs multi-stream, choosing servers, testing at the edge vs end host, latency under load, and repeatable records."
sources:
  - https://www.measurementlab.net/tests/ndt/
  - https://iperf.fr/iperf-doc.php
  - https://www.waveform.com/tools/bufferbloat
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Speed test methodology

## Avoid misleading results
- Test **wired**, from a capable machine (gigabit+ NIC, not throttled CPU, no VPN), or you measure
  Wi-Fi/host limits.
- Test at the **edge** (directly behind the ISP handoff/firewall) and at the user location to split
  ISP vs internal problems.
- Pause other traffic or record utilisation during the test.
- Browser tests depend on browser and CPU; use CLI tools for repeatability.

## Tools
| Tool | Notes |
|---|---|
| Ookla Speedtest (`speedtest` CLI) | vendor tool; cross-check against a second tool |
| M-Lab NDT7 | single stream measurement of bulk transport capacity (per M-Lab); shows what one flow achieves |
| Cloudflare speed.cloudflare.com, fast.com | browser based; cross-check with a CLI tool |
| iperf3 to your own server | controlled endpoint across WAN/VPN: `iperf3 -c host -P 8 -t 30` and `-R` |
| Waveform bufferbloat test | latency under load |

## Interpreting
- Multi-stream close to plan but single-stream low -> latency x window (BDP) or per-flow shaping,
  not lack of bandwidth.
- Download fine, upload poor -> asymmetric plan or upstream congestion (cable evenings).
- Latency rising sharply under load -> bufferbloat; enable SQM or QoS shaping.
- Results vary by time of day -> ISP contention.
- Firewall with IPS/TLS inspection can cap throughput; test with inspection bypassed for comparison.

## Record
Date/time, location, wired/wireless, tool and server, download/upload/latency/jitter, latency
under load. Take several runs at different times; ISPs want this when you open a ticket.

## Verify
- [ ] Edge wired tests stay close to the contracted speed across a day; user-location gaps explained by measured internal limits.

## Checked

- Date: 2026-10-28
- Confirmed: M-Lab NDT is a single-stream measurement; iperf3 options -P/--parallel (default 1), -R/--reverse and -t/--time exist as used in the example command.
- Removed: Ookla and Cloudflare tool behaviour notes, Google search usage claim, flent, 90 % threshold, fq_codel.
Method: documentation only; no commands were run.
