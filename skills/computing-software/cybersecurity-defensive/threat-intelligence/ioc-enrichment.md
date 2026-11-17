---
id: computing-software.cybersecurity-defensive.threat-intelligence.ioc-enrichment
name: ioc-enrichment
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [iocs, ioc-enrichment, virustotal, passive-dns, whois, threat-intel-platform, context-scoring]
level: practitioner
status: draft
description: "Enrich IOCs before acting: passive DNS, WHOIS, certificate, sandbox and reputation lookups, internal sightings, scoring confidence and avoiding tipping off adversaries."
sources: ["MISP documentation - Enrichment modules", "VirusTotal API v3 documentation", "FIRST CTI SIG - IOC handling guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IOC enrichment

**Goal:** each indicator has enough context to decide whether to block, hunt, monitor or discard.

## Enrichment by type
- **IP:** ASN and owner (`whois`, Team Cymru), geolocation, hosting vs residential, passive DNS (domains seen on it), open ports (Shodan/Censys), reputation (AbuseIPDB, GreyNoise to identify mass scanners/benign crawlers), shared hosting/CDN (blocking a Cloudflare IP blocks thousands of sites).
- **Domain:** registration date (newly registered = suspicious), registrar, WHOIS/RDAP, name servers, passive DNS history, certificate transparency (crt.sh), URL scanning (urlscan.io), lookalike of your brands.
- **URL:** scan in a sandbox or urlscan (mind visibility settings - public scans can tip off actors and leak tokens in URLs).
- **File hash:** VirusTotal detections and first-seen date, sandbox reports (behaviour, contacted hosts), signer, prevalence, YARA matches.
- **Email:** sender infrastructure, SPF/DKIM/DMARC results, campaign clustering.

## Internal context (most important)
Sightings in your own logs: SIEM lookups across DNS, proxy, EDR, email over the indicator's lifetime. An indicator never seen internally is lower priority for hunting; one seen on a critical host escalates.

## Scoring
Record source, source reliability, confidence, first/last seen, kill-chain phase, related actor/campaign, TLP. Lower confidence for shared infrastructure, old indicators, and single-source items.

## Automation
TIP enrichment modules (MISP modules, OpenCTI connectors) or SOAR playbooks; cache results; respect API quotas.

## OPSEC
- Do not resolve or browse adversary domains from corporate IPs; use sandboxes/attribution-managed infrastructure.
- Uploading a private sample to public VirusTotal makes it visible to subscribers (including adversaries); check hash first, upload only if allowed.

## Verify
- [ ] Enrichment records stored with the indicator in the TIP.
- [ ] Block decisions reference enrichment (e.g. not CDN shared, low false positive risk).
