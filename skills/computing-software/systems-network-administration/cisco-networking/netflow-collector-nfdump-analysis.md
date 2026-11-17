---
id: computing-software.systems-network-administration.cisco-networking.netflow-collector-nfdump-analysis
name: netflow-collector-nfdump-analysis
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [netflow, nfdump, nfcapd, flow-collector, ipfix, top-talkers, traffic-analysis]
level: practitioner
status: draft
description: "Collect NetFlow/IPFIX with nfcapd and query it with nfdump: top talkers, filters, time windows, aggregation, and proving a collector is receiving data."
sources:
  - https://github.com/phaag/nfdump
  - https://github.com/phaag/nfdump/blob/master/man/nfdump.1
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NetFlow collector and nfdump analysis

nfdump is the classic open-source collector/CLI: `nfcapd` receives and writes 5-minute
files, `nfdump` queries them.

## Collect
```bash
mkdir -p /var/cache/nfdump/edge1
nfcapd -D -p 2055 -w /var/cache/nfdump/edge1 -S 1 -t 300   # -S 1: year/month/day subdirs
```
Multiple exporters: one nfcapd per port, or `-n name,ip,dir` per source (version dependent;
check `nfcapd -h`). Open UDP 2055 on the host firewall.

Proof of receipt: `tcpdump -ni eth0 udp port 2055 -c 5` and new files every 5 minutes.

## Query
```bash
# Top 10 source IPs by bytes over a window
nfdump -R /var/cache/nfdump/edge1 -t 2026/10/16.09:00:00-2026/10/16.10:00:00 -s srcip/bytes -n 10
# Top destination ports
nfdump -R /var/cache/nfdump/edge1 -s dstport/bytes -n 20
# All flows of one host to TCP 445
nfdump -R /var/cache/nfdump/edge1 'src host 10.1.1.50 and proto tcp and dst port 445'
# Aggregate by conversation, output as CSV
nfdump -R /var/cache/nfdump/edge1 -A srcip,dstip -o csv 'net 10.1.0.0/16' > conv.csv
```
Filter syntax is tcpdump-like (`src net`, `port`, `proto`, `bytes > 1000000`, `flags S`).

## Patterns
- Sudden bandwidth spike: `-s srcip/bytes` over the spike window names the host in seconds.
- Scanning: `-s srcip/flows` with `'flags S and not flags A'` shows sources making many SYN-only flows.
- Data exfil: flows with large outbound bytes to a single external address outside hours.
- Remember sampling: multiply if the exporter samples (nfdump scales if sampler info is sent).

## Front ends
NfSen/nfsen-ng, or export to Elastic/ClickHouse via goflow2/pmacct for dashboards.

## Verify
- [ ] New nfcapd files each interval; nfdump top-talkers match interface SNMP counters roughly.
