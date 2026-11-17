---
id: computing-software.cybersecurity-defensive.network-defence.dns-query-logging
name: dns-query-logging
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [dns-security, dns-query-logging, dns-analytics, route53-resolver-query-logs, windows-dns-analytical-log, zeek-dns, passive-dns]
level: practitioner
status: draft
description: "Collect DNS query logs from Windows DNS, BIND, Unbound, cloud resolvers and network sensors with client attribution, ship them to the SIEM and use them for hunting."
sources: ["Microsoft Learn - DNS logging and diagnostics (analytical log)", "Amazon Route 53 Resolver query logging documentation", "NSA and CISA - Selecting a Protective DNS Service and DNS logging guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DNS query logging

**Goal:** every internal DNS query is logged with the real client IP and stored searchable, for detection (C2, DGA, tunnelling) and investigations.

## Where to log
Log at the resolver that sees the **original client** - logging at a forwarder behind the resolver shows only the resolver's IP.

- **Windows DNS Server (2016+):** enable Analytical log: Event Viewer > Applications and Services Logs > Microsoft > Windows > DNS-Server > Analytical (show hidden logs) > Enable, or `wevtutil sl Microsoft-Windows-DNSServer/Analytical /e:true /rt:true /ms:<bytes>`. Event 256 = query received, 257 = response. Collect via ETW-capable agent (AMA DNS connector, Splunk Stream/UF, Elastic). Avoid legacy debug logging (`dns.log`) on busy servers.
- **BIND:** `logging { channel q { file "/var/log/named/queries.log" versions 10 size 100m; print-time yes; }; category queries { q; }; };` and `rndc querylog on`; or dnstap for high volume.
- **Unbound:** `log-queries: yes` / `log-replies: yes`, or dnstap.
- **Cloud:** Route 53 Resolver query logging to CloudWatch/S3/Firehose per VPC; Azure DNS Security Policy / DNS analytics via AMA; GCP Cloud DNS logging policy.
- **Network sensors:** Zeek `dns.log`, Suricata `eve.json` dns events capture all on-wire DNS including rogue resolvers.
- **Endpoints:** Sysmon Event ID 22 (DNSEvent) gives process attribution; DoH from browsers bypasses resolver logs unless controlled.

## Fields
timestamp, client IP (and resolved hostname/user via DHCP and EDR joins), query name, type, response code, answers, resolver.

## Use
- New/rare domains, newly registered domains, high-entropy labels (DGA), long TXT/NULL queries and high query volume to one domain (tunnelling), NXDOMAIN spikes.
- Retroactive IOC search during incidents.

## Volume
DNS is high volume; filter known-good internal zones at ingest or summarise, but keep full logs for external names at least 90 days.

## Verify
- [ ] `nslookup test-$(random).example.com` from a workstation appears in the SIEM with the workstation's IP within minutes.
- [ ] Coverage list shows every resolver and cloud VPC logging.
