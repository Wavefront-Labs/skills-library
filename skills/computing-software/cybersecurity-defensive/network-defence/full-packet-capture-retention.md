---
id: computing-software.cybersecurity-defensive.network-defence.full-packet-capture-retention
name: full-packet-capture-retention
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-security-monitoring, full-packet-capture, arkime, pcap-retention, rolling-buffer, security-onion, packet-broker, capture-storage-sizing]
level: advanced
status: draft
description: "Deploy full packet capture (Arkime, Security Onion) at chokepoints: sizing storage for days of retention, filtering encrypted bulk, and retrieving sessions for investigations."
sources: ["CIS Control 13 (network monitoring and defense)", "Arkime documentation (arkime.com)", "Security Onion documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Full packet capture retention

**Goal:** when an alert fires, you can retrieve the actual packets of the session from the last
days, which proves what happened beyond what logs show.

## Architecture
- Sensors at chokepoints (internet edge inside the firewall, data centre core, between zones)
  fed by TAPs or packet brokers; packet brokers deduplicate, slice and load-balance.
- **Arkime** (formerly Moloch) indexes session metadata in OpenSearch/Elasticsearch and stores
  pcap on sensor disks; analysts search sessions and download pcap. **Security Onion** bundles
  capture (Stenographer/Suricata pcap), Zeek, Suricata and Elastic.

## Sizing
```
storage_bytes = average_link_utilisation_bits_per_sec / 8 x seconds_of_retention
```
Example: 2 Gbps average over 7 days = 2e9/8 x 604,800 = ~151 TB. Reduce by:
- Truncating or dropping bulk encrypted traffic after the handshake (Arkime `packet-drop`/`maxPacketsInQueue`
  rules, or Security Onion BPF) - keeps metadata, cuts 60-80% of volume.
- Excluding known-heavy trusted flows (backups, video streaming CDNs) by BPF.
- Accepting shorter retention for pcap (days) and longer for metadata (weeks/months).

## Operations
- Monitor packet drops on capture NICs and sensor disk free; a full disk silently stops capture.
- Time sync (PTP/NTP) on sensors to correlate with logs.
- Access control and audit for pcap retrieval (it contains everything, including credentials).

## Using it
Pivot from an alert (IP, port, time) to Arkime sessions, review SPI data (HTTP headers, DNS,
TLS SNI/JA4), download pcap for Wireshark. For TLS, packets give metadata and sizes unless
inspected upstream.

## Gotchas
- More encryption (TLS 1.3, QUIC, ECH) reduces payload value; metadata extraction (Zeek, JA4) becomes the main return.
- Legal and privacy review: full capture includes employee personal data.
- Capturing only at the edge misses lateral movement; prioritise internal chokepoints too.

## Verify
- [ ] Retention actually achieved (oldest pcap timestamp) matches the target.
- [ ] Sensor drop rate under 0.1% during peak.
