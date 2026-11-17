---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.flow-analysis-with-silk
name: flow-analysis-with-silk
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [silk, netflow, ipfix, flow-analysis, network-forensics, dfir]
level: advanced
status: draft
description: "Investigate network flow records with CERT NetSA SiLK: rwfilter selections, rwcut, rwstats top-N, rwcount time series, IP sets and converting pcaps or IPFIX for analysis."
sources: ["https://tools.netsa.cert.org/silk/", "https://tools.netsa.cert.org/silk/analysis-handbook.pdf", "https://tools.netsa.cert.org/silk/rwfilter.html", "https://tools.netsa.cert.org/silk/rwstats.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flow analysis with SiLK

SiLK (System for Internet-Level Knowledge, CERT NetSA) stores NetFlow/IPFIX as compact binary records and provides fast command-line tools. It suits months of flow data where packet capture does not exist.

## Getting data in
- Live collection: `rwflowpack` from NetFlow v5/v9/IPFIX exporters (often fed by YAF or routers).
- From pcaps: `yaf --in cap.pcap --out cap.yaf` then `rwipfix2silk cap.yaf --silk-output=cap.rw`, or `rwp2yaf2silk --in=cap.pcap --out=cap.rw`.
- Repository queries use `--start-date/--end-date --type=in,out` with the configured sensor layout.

## Core tools
```bash
# all flows from a host to TCP 443 in a window
rwfilter --start-date=2026/10/01 --end-date=2026/10/05 --type=all \
  --saddress=10.1.2.3 --proto=6 --dport=443 --pass=stdout | rwcut --fields=sip,dip,dport,bytes,packets,stime,duration
# top destinations by bytes from that host
rwfilter ... --saddress=10.1.2.3 --pass=stdout | rwstats --fields=dip --values=bytes --count=20
# traffic over time in 5-minute bins
rwfilter ... --daddress=203.0.113.50 --pass=stdout | rwcount --bin-size=300
# IP sets: hosts that talked to the C2
rwfilter ... --daddress=203.0.113.50 --pass=stdout | rwset --sip-file=talked_to_c2.set
rwsetcat talked_to_c2.set
```
Other tools: `rwsort`, `rwuniq` (custom aggregations), `rwsetbuild` (IOC lists to sets for `--dipset` filtering), `rwappend`, `rwfileinfo` (provenance of a file).

## Investigation patterns
- **Scoping C2**: build a set of known C2 IPs (`rwsetbuild`), filter `--dipset` over the whole retention period to find every internal host that contacted them and when it started.
- **Exfiltration**: `rwstats --fields=sip,dip --values=bytes` on outbound flows; asymmetry (out >> in) to rare destinations.
- **Beaconing**: `rwcut` start times for a host-destination pair, then examine intervals (`awk` difference of successive `stime`).
- **Lateral movement**: internal-to-internal flows on 445, 3389, 5985, 135 from unexpected sources.

## Gotchas
- Flows are sampled on many routers (1:N); byte counts are estimates. Check exporter sampling settings before quoting volumes.
- Long connections are split into multiple records by active timeouts; aggregate before measuring duration.
- Time is flow start/end at the exporter; clock and timeout settings affect precision.

## Verify
Key figures (first contact time, bytes out) are reproduced with a second query or cross-checked against firewall or proxy logs, and sampling rates are stated.
