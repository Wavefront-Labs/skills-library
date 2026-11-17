---
id: computing-software.cybersecurity-defensive.network-defence.ddos-response-runbook
name: ddos-response-runbook
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ddos-mitigation, ddos-response-runbook, incident-response, traffic-analysis, provider-escalation, extortion-ddos, ransom-ddos]
level: practitioner
status: draft
description: "Prepare and run a DDoS response: detection signals, classification, provider escalation, mitigation actions, communications, ransom-DDoS handling and after-action review."
sources: ["CISA/FBI/MS-ISAC Understanding and Responding to DDoS Attacks (2024)", "NIST SP 800-61r3", "CompTIA Security+ SY0-701 objective 2.4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DDoS response runbook

**Goal:** when a DDoS hits, the team recognises it quickly, engages the right provider, applies
prepared mitigations and communicates, instead of improvising.

## Before (preparation)
- Inventory internet-facing services, their providers (CDN, cloud, ISP, DNS) and protection level.
- Provider contacts, account IDs and escalation procedures in an offline copy.
- Baselines for traffic (bps, pps, requests/sec) per service; monitoring and alerts on deviations.
- Pre-approved actions: enable "under attack" mode, geo-block, tighten rate limits, swing BGP to scrubbing.

## During
1. **Detect and confirm**: traffic graphs, error rates, provider alerts. Distinguish from a
   legitimate spike (marketing campaign, outage-driven retries) and from infrastructure failure.
2. **Classify**: volumetric (bps), protocol (pps, SYN/UDP), application layer (requests to specific URLs).
   Capture samples: top source IPs/ASNs, user agents, URLs, packet types.
3. **Engage**: open a priority case with the provider (and ISP for volumetric attacks on own links).
4. **Mitigate** by type:
   - Volumetric: provider scrubbing / BGP diversion, upstream blackholing of targeted IP only as last resort (it completes the DoS for that IP).
   - Protocol: SYN proxy, zone protection, ACLs for reflection protocols (UDP 123, 1900, 11211, 389).
   - Application: WAF rules on request signature, rate limits, JS challenge/CAPTCHA, cache more aggressively, temporarily disable expensive features.
5. **Watch for distraction**: DDoS can cover intrusion attempts; keep monitoring other alerts.
6. **Communicate**: status page, customer support scripts, executives.

## Ransom DDoS
Extortion emails threatening attacks: do not pay; notify providers and law enforcement; verify
protections on the named targets; many threats are never carried out.

## After
Timeline, peak volumes, what worked, time to mitigate, gaps (unprotected service, missing
contact), and update the runbook.

## Gotchas
- Mitigations left on after the attack (geo-blocks, CAPTCHAs) silently hurt customers; schedule their removal.
- Attack traffic often targets DNS or the VPN, not the website.

## Verify
- [ ] Tabletop of a DDoS scenario run within the last year.
- [ ] Provider escalation numbers tested.
