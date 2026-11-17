---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.dns-forensic-analysis
name: dns-forensic-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [dns-forensics, dns, protocol-forensics, pcap, zeek, passive-dns, dfir]
level: practitioner
status: verified
description: "Analyse DNS in packet captures and logs for investigations: query/response fields, NXDOMAIN storms, DGA and fast-flux patterns, TTLs, tunnelling indicators and attribution."
sources: ["https://www.wireshark.org/docs/dfref/d/dns.html", "https://docs.zeek.org/en/master/logs/dns.html", "https://datatracker.ietf.org/doc/html/rfc1035"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS forensic analysis

**Goal:** use DNS evidence to find infected hosts, C2 domains, and the timing of malicious
activity, even when payload traffic is encrypted.

## Wireshark filters
```text
dns                                  all DNS
dns.flags.response == 0              queries only
dns.flags.rcode == 3                 NXDOMAIN responses
dns.qry.name contains "example"      domain filter
dns.qry.type == 16                   TXT (tunnelling, staging)
dns.resp.ttl < 60                    low TTLs (fast flux, C2)
dns.qry.name.len > 50                long names (encoding)
```
Statistics -> DNS gives rcode, query types and counts.

## tshark summary
```bash
tshark -r cap.pcap -Y "dns.flags.response==0" -T fields -e frame.time_epoch -e ip.src -e dns.qry.name -e dns.qry.type > q.tsv
cut -f3 q.tsv | sort | uniq -c | sort -rn | head -50
```

## Patterns
- **DGA**: many NXDOMAIN for random-looking names from one host; high entropy labels.
- **Fast flux**: many A records, short TTLs, changing over time.
- **Tunnelling**: long, high-entropy subdomains, TXT/NULL/CNAME types, high query volume to one
  domain (see the DNS tunnelling skill).
- **Newly registered / rare domains**: compare against top lists and first-seen data.
- **Resolver bypass**: hosts querying external resolvers directly (port 53 to non-corporate
  IPs) or DoH endpoints.

## Attribution
Internal resolver logs only show the resolver as source for forwarded queries; get client
IPs from the internal DNS server logs (Windows DNS analytic log, BIND query log) or Zeek on
the inside. Map IPs to hosts via DHCP.

## Pivot
Passive DNS (historical resolutions), WHOIS, certificate transparency for discovered domains.

## Verify
Each suspicious domain has: first and last query time, querying hosts, resolved IPs, and
corresponding connection evidence (or a note that none followed).

## Checked
Run on Wireshark 4.4.1 against synthetic captures (A and TXT queries, answered, unanswered and NXDOMAIN lookups, 52 to 77
character names): every filter in the Wireshark block parsed and matched the intended packets (`dns.resp.ttl < 60` also
matches a TTL of 0), `dns.qry.name.len` exists, the tshark summary pipeline produced the per-name counts, and Statistics >
DNS is in the User's Guide statistics chapter. Windows DNS analytic events are described on Microsoft Learn and BIND's
query log in its Administrator Reference Manual. Pattern descriptions (DGA, fast flux) are heuristics, not detections.
