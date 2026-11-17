---
id: computing-software.cybersecurity-defensive.network-defence.network-detection-and-response
name: network-detection-and-response
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-security-monitoring, ndr, network-detection-and-response, zeek, suricata, east-west-visibility, encrypted-traffic-analysis, darktrace, vectra, corelight]
level: practitioner
status: draft
description: "Deploy and tune network detection and response: sensor placement for east-west visibility, Zeek-based metadata, detection categories, and integration with EDR and SIEM."
sources: ["CompTIA CySA+ CS0-003 objective 1.3 (network-related indicators)", "Gartner Market Guide for NDR (category definition)", "Zeek documentation (logs reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network detection and response (NDR)

**Goal:** detect attacker activity in network traffic, especially lateral movement and C2 on
hosts without EDR (IoT, OT, appliances, unmanaged), and respond fast.

## What NDR provides
- Metadata from all traffic (Zeek-style conn, dns, http, ssl, smb, kerberos, rdp logs).
- Detections: behavioural/ML (anomalous admin protocol use, beaconing, data staging),
  signatures (Suricata), and threat intel matching.
- Response: block via firewall/NAC integration, host isolation through EDR, or packet capture on demand.
Products: commercial (Vectra, Darktrace, ExtraHop, Corelight, Cisco Secure Network Analytics)
or open source (Zeek + Suricata + Security Onion/Malcolm).

## Placement
1. Internet edge (inside NAT so internal IPs are visible).
2. Data centre / server zone core for east-west.
3. Cloud: VPC traffic mirroring or virtual taps for critical subnets.
4. OT boundary (Purdue level 3/3.5), passive only.
Coverage map: list segments and whether NDR sees intra-segment traffic (switch-local traffic between two hosts on the same VLAN is often missed).

## Tuning
- First 2-4 weeks learning period for behavioural engines; tag known scanners, backup servers, admin jump hosts.
- Triage the noisiest detection types and suppress by host role, not globally.
- Feed asset context (critical servers, admin hosts) so alerts are prioritised.

## Integration
- Send detections and metadata to the SIEM; correlate with EDR process data (which process made the connection).
- Response actions automated only for high-confidence cases, with approval for critical assets.

## Gotchas
- Encrypted traffic limits payload detection; rely on metadata (JA4, certificate, timing, sizes).
- Packet drops at sensors under load create blind spots: monitor sensor health.
- Licensing by throughput tempts teams to exclude traffic; decide exclusions consciously.

## Verify
- [ ] Coverage map shows each critical segment observed.
- [ ] Purple-team test (simulated lateral movement over SMB/WinRM in a lab segment) detected.
