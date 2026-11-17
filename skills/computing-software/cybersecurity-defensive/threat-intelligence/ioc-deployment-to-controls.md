---
id: computing-software.cybersecurity-defensive.threat-intelligence.ioc-deployment-to-controls
name: ioc-deployment-to-controls
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [iocs, ioc-deployment, blocklists, edr-indicators, dns-rpz, firewall-edl, stix-taxii, expiry]
level: advanced
status: draft
description: "Deploy vetted IOCs to security controls: choose block versus detect, push via TAXII, EDLs, RPZ and EDR APIs, set expiry, and test for false positives before wide blocking."
sources: ["OASIS STIX 2.1 and TAXII 2.1 specifications", "Palo Alto Networks - External Dynamic Lists documentation", "Microsoft Defender for Endpoint - Manage indicators"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deploying IOCs to controls

**Goal:** high-confidence indicators reach the right controls automatically, with expiry, and without blocking business traffic.

## Decide action per indicator
| Confidence / context | Action |
|---|---|
| High confidence, low collateral (unique malicious domain, malware hash) | Block + alert |
| Medium confidence or shared infra | Alert/monitor only, hunt retroactively |
| Low confidence, old | Retro-hunt only, do not deploy |

## Delivery paths
- **DNS:** RPZ zone fed from TIP (`malicious.example CNAME .` for NXDOMAIN, or to sinkhole) on BIND/Infoblox/Unbound; protective DNS services with custom block lists.
- **Firewall/proxy:** External Dynamic Lists (Palo Alto EDL URL/IP/domain lists served over HTTPS), FortiGate threat feeds, Zscaler/Netskope custom categories.
- **EDR:** Defender for Endpoint indicators API (`POST /api/indicators` with `action: Block|Audit|Warn`, `expirationTime`), CrowdStrike IOC Management API, SentinelOne blacklist.
- **Email gateway:** Tenant Allow/Block List (`New-TenantAllowBlockListItems`), sender/URL blocks.
- **SIEM:** threat intel lookups/ThreatIntelligenceIndicator tables matched against logs (retro and real-time).
- **Transport:** TIP -> TAXII 2.1 collections -> consumers; or SOAR jobs.

## Safety
- Allow-list check before deployment: your own domains, CDNs, major SaaS, cloud provider ranges, top-1M sites (Tranco), RFC1918.
- Stage: audit mode for 24 h on EDR/DNS, check hit volume; a sudden spike of hits on a new indicator often means a false positive.
- Every deployed indicator carries `valid_until`/expiry (e.g. IPs 30 days, domains 90 days, hashes long-lived) and source reference.

## Feedback
Hits create alerts with the indicator's context; record true/false positive to feed source scoring.

## Verify
- [ ] Test indicator (benign test domain) blocked on all intended controls within the SLA.
- [ ] No deployed indicators without expiry.
- [ ] Allow-list guard rejects a test attempt to block a protected domain.
