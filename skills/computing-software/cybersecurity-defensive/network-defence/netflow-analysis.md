---
id: computing-software.cybersecurity-defensive.network-defence.netflow-analysis
name: netflow-analysis
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-security-monitoring, netflow-analysis, ipfix, sflow, flow-logs, nfdump, silk, traffic-baselining, data-exfiltration-detection]
level: practitioner
status: draft
description: "Collect and analyse NetFlow/IPFIX/sFlow to baseline traffic, find scanning, lateral movement and exfiltration, and size flow collection."
sources: ["CIS Control 13.6 (collect network traffic flow logs)", "RFC 7011 IPFIX protocol", "nfdump documentation", "CERT NetSA SiLK documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NetFlow / IPFIX analysis

**Goal:** see who talked to whom, how much and when, across the whole network, cheaply enough
to keep months of history.

## Collection
- Export from routers, firewalls, core switches (NetFlow v9/IPFIX; sFlow is sampled).
- Collector: nfdump/nfcapd, SiLK, ElastiFlow, or the SIEM/NDR's collector.
```
nfcapd -w -D -l /var/flows -p 2055 -S 1        # collect, rotate files every 5 minutes
```
- Prefer unsampled flow at internet edges and between security zones; sampling (1:1000) hides small exfiltration and beacons.
- Flow active timeout (e.g. 60 s) so long connections are reported during, not only after.

## Queries (nfdump)
Top talkers outbound by bytes:
```
nfdump -R /var/flows -s srcip/bytes -n 20 'src net 10.0.0.0/8 and not dst net 10.0.0.0/8'
```
Internal host scanning (SYN-only flows, many destinations):
```
nfdump -R /var/flows -q -o "fmt:%sa %da" 'proto tcp and flags S and not flags A and dst port in [445 3389 22]' \
  | sort -u | awk '{print $1}' | uniq -c | sort -rn | head
```
Sources contacting hundreds of distinct hosts on 445/3389/22 within minutes are scanning or worming.
Lateral movement: workstation-to-workstation SMB/RDP/WinRM (usually rare by design).
Exfiltration: large outbound byte counts to rare destinations, especially at odd hours; asymmetric flows (bytes out much greater than bytes in).

## Baseline
Build per-subnet baselines (normal peers, ports, volumes by hour). Alerts on deviations are
better than static thresholds.

## Gotchas
- Flows have no payload or domain names: enrich with DNS logs and proxy logs.
- NAT hides internal hosts at the edge: collect inside NAT too, or join with NAT logs.
- Asymmetric routing produces half flows; collect from both paths.
- Storage: roughly 50-100 bytes per flow record; estimate flows/sec x retention before buying disk.

## Verify
- [ ] A test transfer of 1 GB to an external host appears with correct bytes and endpoints.
- [ ] Flow sources report continuously (alert on exporter silence).
