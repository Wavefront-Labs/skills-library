---
id: computing-software.cybersecurity-defensive.network-defence.secure-web-gateway-deployment
name: secure-web-gateway-deployment
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [web-filtering, secure-web-gateway, swg, explicit-proxy, pac-file, sse, zscaler, netskope, cloud-proxy, roaming-users]
level: practitioner
status: draft
description: "Deploy a secure web gateway for office and roaming users: forwarding methods (PAC, agent, GRE/IPsec), authentication, policy baseline, bypasses and logging."
sources: ["CompTIA Security+ SY0-701 objective 4.5 (web filter, agent-based, centralised proxy)", "CIS Control 9.3 (network-based URL filters)", "Gartner Security Service Edge definition"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure web gateway deployment

**Goal:** all user web traffic, on site or remote, passes through policy (malware, phishing,
category, DLP) with user identity attached to every log.

## Forwarding options
| Method | Use |
|---|---|
| Endpoint agent (Zscaler Client Connector, Netskope client, Defender for Endpoint web protection) | Roaming laptops; follows the user everywhere |
| PAC file / explicit proxy | Managed browsers on site; easy but bypassable by non-browser apps |
| GRE/IPsec tunnels from branch firewalls | Office traffic including unmanaged devices |
| Transparent/inline on-prem proxy | Legacy, single site |
Most estates combine an agent for laptops with tunnels for sites.

## Identity
SAML/SCIM integration with the IdP so logs show users and groups; policies by group.

## Policy baseline
1. Block: malware, phishing, newly registered/observed domains (or warn), command-and-control,
   anonymisers/proxies, P2P, high-risk categories per acceptable use policy.
2. Caution pages for uncategorised sites.
3. File type controls: block executable downloads from uncategorised sites; sandbox unknown files.
4. TLS inspection for most categories (see TLS inspection skill), bypass for privacy-sensitive categories (health, finance) and pinned apps.
5. DLP on uploads for sensitive data.

## Bypasses
Keep a reviewed list: update services that break with inspection, VoIP/video (direct for
performance), certificate-pinned apps. Each bypass is a blind spot; document owner and reason.

## Logging
Forward logs (user, URL, category, action, bytes, file hashes) to the SIEM; these are core
investigation data for phishing clicks and exfiltration.

## Gotchas
- Users with admin rights disable agents; enforce tamper protection and alert on agent offline.
- Fail-open vs fail-closed when the cloud proxy is unreachable: decide and document.
- Geo-location of egress IPs changes content and triggers "impossible travel" in SaaS logs.

## Verify
- [ ] Test URLs (malware/phishing test pages from the vendor) blocked on site and off site.
- [ ] Logs carry user identity for over 99% of requests.
