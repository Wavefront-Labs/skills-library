---
id: computing-software.systems-network-administration.cisco-networking.ios-high-cpu-troubleshooting
name: ios-high-cpu-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, high-cpu, show-processes-cpu, interrupt-cpu, punt, epc, troubleshooting]
level: practitioner
status: draft
description: "Diagnose high CPU on IOS and IOS XE: process vs interrupt load, top processes, platform-level CPU on XE, punted traffic, and capturing what is hitting the CPU."
sources:
  - https://www.cisco.com/c/en/us/support/docs/routers/4000-series-integrated-services-routers/212409-troubleshoot-high-cpu-on-isr4000.html
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/215890-troubleshoot-high-cpu-usage-in-catalyst.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# High CPU troubleshooting

## 1. Process or interrupt?
```
show processes cpu sorted | exclude 0.00
!  CPU utilization for five seconds: 85%/40%; one minute: 80%; five minutes: 78%
```
In `85%/40%`, the second number is interrupt-level (packets switched in software). High interrupt
= traffic punted to or process-switched by the CPU. High total with low interrupt = a process.
```
show processes cpu history          ! 72-hour graph; correlate with events
```

## 2. IOS XE: which layer?
IOS XE runs IOSd as one Linux process among others. Check the platform view first:
```
show processes cpu platform sorted | exclude 0%
show platform software status control-processor brief
```
- `linux_iosd-imag` high: look inside IOSd with `show processes cpu sorted`.
- `fed main event` (Catalyst) or `ucode_pkt_PPE0` (ISR/ASR data plane): forwarding plane/punt load.
- `smand`, `pubd`, `ndbmand`: telemetry/programmability load.

## 3. Common culprits by process
| Process | Typical cause |
|---|---|
| IP Input | process-switched traffic: ACL logging, IP options, TTL-expired floods, fragments, CEF disabled |
| ARP Input | ARP storms, scanning of a large connected subnet, ARP for directly connected default route |
| SNMP ENGINE | NMS polling heavy tables (full routing table, ARP/MAC tables) too often |
| BGP Router / BGP Scanner | convergence, large table churn |
| Spanning Tree / HL3U | topology changes, MAC flushes |
| SSH Process / Exec | big show outputs, automation hammering the box |
| Crypto IKMP | IKE negotiation storms |

## 4. See what is punted (Catalyst 9k)
```
show platform software fed switch active punt cpuq brief
show platform software fed switch active punt cause summary
show platform hardware fed switch active qos queue stats internal cpu policer
monitor capture CPU control-plane in match any buffer size 10 limit pps 1000
monitor capture CPU start / stop
show monitor capture CPU buffer brief
```
The CPU capture shows the actual packets (e.g. TTL=1 traffic, broadcast storm, routing protocol
floods). Fix the source or tighten CoPP.

## Gotchas
- Short spikes from `show tech`, `write memory` or SNMP walks are normal; chase sustained load.
- Debugs themselves raise CPU; prefer captures and counters.

## Verify
- [ ] Five-minute CPU back to baseline and the offending process/punt cause no longer at the top.
