---
id: computing-software.systems-network-administration.cisco-networking.sflow-vs-netflow
name: sflow-vs-netflow
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, sflow-agent, sflow, netflow, ipfix, packet-sampling, flow-telemetry, nexus, catalyst, monitoring]
level: practitioner
status: draft
description: "Compare sFlow and NetFlow/IPFIX: packet sampling vs flow cache, what each can measure, where Cisco platforms support sFlow, and configuring an sFlow agent on Nexus."
sources:
  - https://sflow.org/sflow_version_5.txt
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/system-management/b-cisco-nexus-9000-series-nx-os-system-management-configuration-guide-93x/b-cisco-nexus-9000-series-nx-os-system-management-configuration-guide-93x_chapter_011000.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sFlow vs NetFlow

## Model
| | sFlow (v5) | NetFlow v9 / IPFIX |
|---|---|---|
| Mechanism | random 1-in-N packet sampling, exports packet headers (first ~128 bytes) + interface counters immediately | builds flow records in a cache, exports on timeout |
| State on device | none (stateless) | flow cache (memory) |
| Accuracy | statistical; good for top talkers at high speed | exact per flow (unsampled) or sampled |
| L2 visibility | yes (raw headers: MAC, VLAN, any protocol) | depends on record fields |
| Latency to collector | seconds | active timeout (often 60 s+) |
| Standard | sflow.org (RFC 3176 v4) | RFC 3954 / RFC 7011 |

## Where Cisco supports sFlow
Nexus 3000/9000 (NX-OS) support sFlow; Catalyst IOS XE platforms use Flexible NetFlow
(and some support sampled NetFlow). Mixed estates often run both and normalise at the collector.

## Nexus sFlow agent
```
feature sflow
sflow sampling-rate 4096
sflow max-sampled-size 128
sflow counter-poll-interval 20
sflow collector-ip 10.0.0.71 vrf management
sflow collector-port 6343
sflow agent-ip 10.255.0.21
sflow data-source interface ethernet 1/1-48
show sflow
show sflow statistics
```
Sampling rate guidance: 1:1000 at 1G, 1:4096 at 10G, 1:8192+ at 40/100G. Lower N = more accuracy and CPU.

## Choosing
- Billing, security forensics, per-flow exact counts: NetFlow/IPFIX unsampled where affordable.
- High-speed DC fabrics, DDoS detection, L2 visibility: sFlow.
- Collectors (nfdump/nfsen, ntopng, Kentik, ElastiFlow) mostly accept both; scale sFlow samples by N.

## Verify
- [ ] Collector traffic estimate within a few percent of SNMP counters after scaling by sampling rate.
