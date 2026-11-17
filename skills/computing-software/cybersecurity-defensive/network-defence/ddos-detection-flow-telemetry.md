---
id: computing-software.cybersecurity-defensive.network-defence.ddos-detection-flow-telemetry
name: ddos-detection-flow-telemetry
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ddos-detection, netflow, sflow, ipfix, fastnetmon, traffic-baselining, ddos-mitigation]
level: practitioner
status: draft
description: "Detect DDoS with flow telemetry: NetFlow/sFlow/IPFIX export, per-destination thresholds, FastNetMon or Kentik-style detection, automated mitigation triggers and alert tuning."
sources: ["https://fastnetmon.com/docs-fnm-advanced/", "https://datatracker.ietf.org/doc/html/rfc7011", "https://sflow.org/developers/specifications.php", "https://www.cisa.gov/sites/default/files/publications/understanding-and-responding-to-ddos-attacks_508c.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DDoS detection with flow telemetry

## Export
- Edge routers export sampled sFlow (1:1000-1:4096 typical at high speed) or NetFlow v9/IPFIX with short active timeouts (60 s) to the detector. Sampling is fine for volumetric detection.
- Include interface counters (SNMP/streaming telemetry) to see link saturation.

## Detection logic
- Per-destination-host thresholds: packets/s, bits/s, flows/s, overall and per protocol (UDP, TCP SYN, ICMP, fragments).
- Baselines per host group (web servers vs mail vs VPN) - static thresholds from observed peaks x safety factor, or learned baselines.
- Signature hints: UDP from source ports 53/123/1900/11211/389 (reflection), SYN without ACK ratio, many small packets.

## FastNetMon (open source / Advanced) example
```
# /etc/fastnetmon.conf (community edition)
networks_list_path = /etc/networks_list      # your prefixes
sflow = on
sflow_port = 6343
threshold_pps = 200000
threshold_mbps = 1000
threshold_flows = 3500
enable_ban = on
notify_script_path = /usr/local/bin/notify_about_attack.sh
gobgp = on                                     # announce RTBH/FlowSpec automatically
```
Automated actions: BGP blackhole (RTBH) or FlowSpec, or API call to the scrubbing provider to divert.

## Operations
- Alert routing to NOC + SOC with target, vector, magnitude; dashboards for top talkers.
- Tune: legitimate bursts (backups, patch days, marketing events) - suppress windows or higher thresholds for those hosts.
- Review each auto-mitigation for collateral damage.

## Gotchas
- L7 (HTTP) floods are low volume and invisible to flow thresholds; detect at CDN/WAF/load balancer.
- Flow exporters overloaded during attacks drop records; size collectors.

## Verify
- [ ] Simulated flood (lab or authorised test) triggers detection within the target time (e.g. < 1 min).
- [ ] Auto-mitigation path tested end to end.
