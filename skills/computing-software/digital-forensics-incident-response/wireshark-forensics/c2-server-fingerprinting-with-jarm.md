---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.c2-server-fingerprinting-with-jarm
name: c2-server-fingerprinting-with-jarm
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [jarm, tls-server-fingerprinting, c2-infrastructure, threat-intelligence, dfir]
level: practitioner
status: draft
description: "Fingerprint suspected C2 servers with JARM: how the active TLS fingerprint works, running it safely, pivoting in Shodan/Censys, known framework hashes and false-positive limits."
sources: ["https://github.com/salesforce/jarm", "https://engineering.salesforce.com/easily-identify-malicious-servers-on-the-internet-with-jarm-e095edac525a/", "https://help.shodan.io/the-basics/search-query-fundamentals", "https://search.censys.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# C2 server fingerprinting with JARM

JARM (Salesforce, 2020) is an active TLS server fingerprint: it sends 10 crafted ClientHellos and hashes how the server responds (chosen version, cipher, extensions). Servers built on the same TLS stack and configuration give the same 62-character hash, so C2 frameworks with default settings cluster together.

## Running it
```bash
python3 jarm.py 203.0.113.50 -p 443
python3 jarm.py -i suspected_ips.txt -o jarm_results.csv
```
- JARM connects to the server: run from infrastructure that does not reveal your organisation (a research VPS or vendor platform), and only against servers you have reason to investigate. Interaction can tip off an attacker monitoring their server.
- Passive alternative: search existing scan data. Shodan exposes `ssl.jarm:<hash>`, Censys indexes JARM in host records; no packets from you.

## Pivoting
1. Get the hash for a confirmed C2 IP from the incident.
2. Search Shodan/Censys for the same hash, then narrow with other attributes: certificate subject/issuer, HTTP response headers and body hash, open ports, hosting ASN.
3. Candidate siblings go to threat-intel review and, if confirmed, into blocklists and retro-hunts (proxy/DNS logs for contact with them).

## Known hashes
Published lists exist for default Cobalt Strike, Metasploit, Sliver, Mythic, Covenant and others; defaults change with framework and Java/Go versions, and operators change TLS settings, so treat lists as leads.

## Limits
- The same JARM is shared by every server on a given stack and config (many legitimate nginx or Go servers share hashes); a JARM match alone is weak.
- CDNs and load balancers front many origins; JARM reflects the edge, not the C2 behind it.
- JA4S/JA4X (FoxIO) add passive server and certificate fingerprints from your own captures; combine them.

## Gotchas
- Record when the fingerprint was taken; servers change.
- Do not scan networks or IPs where you lack a legitimate investigative reason; follow your organisation's rules for active interaction.

## Verify
Infrastructure attributed via JARM is corroborated by at least one more independent attribute (certificate, HTTP fingerprint, or observed traffic from your environment).
