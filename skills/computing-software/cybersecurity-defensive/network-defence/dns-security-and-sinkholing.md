---
id: computing-software.cybersecurity-defensive.network-defence.dns-security-and-sinkholing
name: dns-security-and-sinkholing
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [dns, dns-sinkhole, dns-firewall, rpz, dga-detection, dns-tunneling, c2-over-dns, doh, dot, dns-filtering, passive-dns, nxdomain, split-horizon]
level: advanced
status: draft
description: "Use DNS as a defensive control point: sinkholing/RPZ for known-bad domains, detecting DGA and DNS-tunnelling C2, and the DoH/DoT blind spot it creates for your own visibility."
sources: ["ISC/BIND Response Policy Zones (RPZ) documentation (public)", "SANS whitepapers on DNS-based detection (public course material)", "RFC 8484 - DNS over HTTPS"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DNS security and sinkholing — a cheap, high-leverage control point

**Goal:** use the fact that almost everything resolves a domain before it connects
to block known-bad destinations cheaply, detect the C2 and exfiltration techniques
that abuse DNS itself, and understand how encrypted DNS quietly removes this
visibility unless you plan for it.

## 1. Sinkhole / DNS firewall with RPZ
Point internal DNS resolvers at threat-intel-fed blocklists (commercial feed,
open-source lists, or your own IOC list from the companion attack-mapping skill)
using Response Policy Zones (RPZ) on BIND/Unbound, or the equivalent "DNS
security" feature on cloud/managed DNS (Cisco Umbrella, cloud provider DNS
firewall). A query for a known-bad domain gets answered with a sinkhole IP (a
host you control that logs the connection attempt) instead of the real answer —
this both blocks the connection (malware can't reach its real C2) and tells you
exactly which internal host tried to resolve it, which is often the fastest
detection signal you have for a compromised endpoint, well before EDR or network
IDS catches the follow-on behaviour. Log every sinkhole hit to the SIEM as a
high-confidence alert — a legitimate host has no reason to query a known-malicious
domain.

## 2. Detecting DGA (domain generation algorithm) traffic
Malware families that generate algorithmic domains to evade static blocklists
leave statistical fingerprints: high NXDOMAIN rate from a single host (trying many
generated domains, most of which aren't registered), high entropy/randomness in
queried domain names, and query volume/pattern anomalies (many distinct
short-lived subdomains). Baseline normal NXDOMAIN rate per host/user and alert on
outliers rather than trying to pattern-match every DGA algorithm individually —
the volume/entropy signal generalises better than any single family's naming
convention.

## 3. Detecting DNS tunnelling and exfiltration over DNS
DNS tunnelling (C2 or data exfiltration encoded in TXT/CNAME/A record queries and
responses) shows up as abnormally long domain labels, unusually high query rate
to a single domain/subdomain, abnormal record types for the host's normal
behaviour (e.g. endpoint workstations rarely need TXT record lookups at volume),
and request/response size patterns inconsistent with normal resolution. Tools
exist (dnscat2 detection signatures, Zeek's dns.log analysis) but the core
technique is the same baseline-and-flag-outlier approach as DGA detection.

## 4. The DoH/DoT blind spot
DNS-over-HTTPS and DNS-over-TLS encrypt the query, and DoH in particular can run
over standard HTTPS (port 443) to a public resolver, bypassing your internal
resolver (and therefore your RPZ/sinkhole/logging) entirely if an application or
browser is configured to use its own built-in DoH resolver. This is a real,
widely-documented visibility gap: a compromised host can use DoH to reach a C2
domain your DNS firewall would otherwise have blocked, and your DNS logs show
nothing. Mitigations: block known public DoH resolver endpoints at the firewall
for anything other than an approved corporate DoH/DoT resolver, and/or enforce
browser/OS policy to use the internal resolver (Group Policy/MDM settings exist
for major browsers) — but treat this as an arms race, not a solved problem; new
DoH endpoints appear faster than blocklists update.

## Gotchas
- Sinkholing a domain that's also used for other legitimate purposes (shared
  hosting, CDN, a compromised-then-cleaned domain) causes collateral blocking —
  verify a feed entry's scope before adding it, and expire stale entries.
- Split-horizon DNS (internal vs external views) means a sinkhole/RPZ applied only
  to the external view won't affect internal resolution paths that bypass it.
- High NXDOMAIN rate also happens from normal causes (typos, browser
  pre-resolution/speculative connections, ad-blocker side effects) — tune
  thresholds against your own baseline, not a generic number from a blog post.
- Logging DNS queries at full fidelity (every query, every host) is a large,
  valuable, but high-volume data source — plan retention and indexing cost before
  turning it on everywhere (see data-onboarding-and-cim-mapping for the Splunk side).

## Verify
- [ ] RPZ/sinkhole hits generate a high-confidence SIEM alert with the querying
      host identified.
- [ ] NXDOMAIN rate and query entropy are baselined per host/segment, not
      compared to a generic published threshold.
- [ ] A policy exists for DoH/DoT (block unapproved resolvers or enforce the
      internal resolver) and its known gaps are documented.
- [ ] DNS log retention/volume was sized deliberately, not left at a default.

Related: computing-software.cybersecurity-defensive.network-defence.firewall-and-egress-policy,
computing-software.cybersecurity-defensive.threat-intelligence.attack-mapping-and-ioc-handling,
computing-software.cybersecurity-defensive.security-operations.threat-hunting-methodology
