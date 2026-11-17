---
id: computing-software.systems-network-administration.cisco-networking.ios-xe-packet-trace
name: ios-xe-packet-trace
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, packet-trace, qfp, debug-platform-condition, drop-reason, asr1000, isr4000, catalyst-8000]
level: practitioner
status: draft
description: "Follow packets through the IOS XE data plane with packet-trace: conditions, per-packet feature paths, drop reasons and FIA trace on ISR/ASR/Catalyst 8000."
sources:
  - https://www.cisco.com/c/en/us/support/docs/content-networking/adaptive-session-redundancy-asr/117858-technote-asr-00.html
  - https://www.cisco.com/c/en/us/td/docs/routers/asr1000/configuration/guide/chassis/asr1000_cfg_packet_trace.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IOS XE packet-trace

## When
"Is the router dropping it, and why?" on IOS XE routers (ASR 1000, ISR 4000, Catalyst 8000,
CSR/C8000V). Packet-trace shows each packet's path through QFP features (ACL, NAT, IPsec, ZBFW)
and the final disposition (FWD/DROP) with a reason.

## Steps
```
debug platform condition ipv4 10.1.1.10/32 both          ! condition: match traffic
debug platform condition start
debug platform packet-trace packet 128 fia-trace         ! keep 128 packets, record feature path
! generate the traffic
show platform packet-trace summary
show platform packet-trace packet 0                       ! per-packet detail
show platform packet-trace statistics
debug platform condition stop
clear platform condition all
```
Conditions can also be ingress interface (`debug platform condition interface Gi0/0/0 ingress`)
or match ACL (`debug platform condition ipv4 access-list TRACE-ACL both`).

## Reading output
```
Pkt   Input        Output       State  Reason
0     Gi0/0/1      Gi0/0/0      FWD
1     Gi0/0/1      Gi0/0/0      DROP   402 (Ipv4Acl)
```
Detail shows each feature: `IPV4_INPUT_ACL`, `IPV4_NAT_INPUT_FIA`, `IPV4_OUTPUT_IPSEC_...` with results.
Drop reasons: `Ipv4Acl`, `Ipv4NoRoute`, `NatIn2out`, `IpsecInput`, `UnconfiguredIpv4Fia`, `TailDrop`.

Global drop counters without conditions:
```
show platform hardware qfp active statistics drop clear   ! reset
show platform hardware qfp active statistics drop
```

## Gotchas
- Always use a condition; unconditional trace on a busy router costs performance.
- Packet-trace sees data-plane forwarding; locally-sourced or punted control-plane traffic paths differ.
- Copy-packet option (`copy packet input size 256`) records bytes for decode.
- Catalyst 9000 switches use a different tool (`show platform software fed ... punt`, FED packet capture);
  packet-trace is for QFP-based routers.

## Verify
- [ ] Clean up: `show platform conditions` empty after troubleshooting.
