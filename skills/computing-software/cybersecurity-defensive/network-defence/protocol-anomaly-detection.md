---
id: computing-software.cybersecurity-defensive.network-defence.protocol-anomaly-detection
name: protocol-anomaly-detection
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [protocol-anomaly-detection, zeek-weird-log, suricata-anomaly, dns-tunneling-detection, protocol-misuse, network-security-monitoring]
level: advanced
status: docs-checked
description: "Detect protocol anomalies: Zeek weird.log and protocol analysers, Suricata anomaly events, non-standard ports, DNS/HTTP/TLS misuse and tunnelling, and baselining to cut noise."
sources: ["https://docs.zeek.org/en/master/logs/weird-and-notice.html", "https://docs.suricata.io/en/latest/output/eve/eve-json-format.html", "https://d3fend.mitre.org/technique/d3f:ProtocolMetadataAnomalyDetection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protocol anomaly detection

Signatures catch known bad; protocol anomaly detection catches traffic that does not behave like the
protocol it claims to be (tunnels, C2 on standard ports, evasion).

## Sources
- **Zeek** `weird.log` (malformed/unexpected protocol events) and `notice.log`; dynamic protocol detection identifies the real protocol regardless of port (`conn.log` `service` field).
- **Suricata** `anomaly` EVE events (decoder, stream, applayer anomalies) and `app_proto` vs destination port.

## Detections
| Anomaly | Logic |
|---|---|
| Protocol on wrong port | `service` = ssh/http/tls on a port not normally used for it, or port 443 with `service` empty/non-TLS |
| DNS tunnelling | Long query names, high entropy labels, many unique subdomains per domain, TXT/NULL heavy, high query volume to one domain |
| HTTP misuse | Rare user agents, POST-heavy to one host with regular timing, missing Host header, HTTP/1.0 from modern clients |
| TLS anomalies | Self-signed/expired certs to external hosts, SNI absent, JA4 rare in the estate, certificate CN mismatching SNI |
| ICMP tunnelling | ICMP echo payloads large or non-standard and high volume |
| SMB/RPC anomalies | SMBv1 use, named-pipe access to unusual pipes from workstations |

## Baselining
Weird events are noisy at first (broken middleboxes, odd devices). Baseline per segment for a period you choose,
suppress known-benign `weird` names per source, alert on new ones.

## Gotchas
- QUIC/HTTP3 on UDP 443 is normal now; do not flag it as anomaly by default.
- CDNs and SaaS produce many long DNS names (e.g. telemetry); allow-list by registrable domain.

## Verify
- [ ] A test DNS tunnel (lab, e.g. iodine in an isolated range) triggers the detection.
- [ ] Weird/anomaly suppressions documented.

## Checked

2026-10-28. Confirmed against: Zeek documentation (weird.log and notice.log); Suricata EVE JSON format (anomaly events); MITRE D3FEND Protocol Metadata Anomaly Detection.

Removed as unconfirmed: numeric DNS-name threshold, two-week baseline, SIEM pseudo-query using orig_bytes.

Method: documentation only; no commands were run.
