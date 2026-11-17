---
id: computing-software.cybersecurity-defensive.endpoint-security.edr-custom-indicator-blocking
name: edr-custom-indicator-blocking
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [edr, custom-ioc-blocking, defender-indicators, crowdstrike-ioc, file-hash-block, certificate-indicators, allow-block-list]
level: practitioner
status: draft
description: "Create, scope and expire custom EDR indicators for hashes, IPs, URLs and certificates in Defender for Endpoint and CrowdStrike, choosing audit, warn or block and avoiding self-inflicted outages."
sources: ["Microsoft Learn - Create indicators in Microsoft Defender for Endpoint", "CrowdStrike Falcon documentation - IOC management", "Microsoft Learn - Network protection (required for IP/URL indicators)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EDR custom indicator blocking

**Goal:** quickly block or alert on known-bad files and destinations across endpoints during an incident, with scoping and expiry.

## Defender for Endpoint
Settings > Endpoints > Indicators (or API `POST https://api.securitycenter.microsoft.com/api/indicators`):
```json
{"indicatorValue":"<sha256>","indicatorType":"FileSha256","action":"BlockAndRemediate",
 "title":"IR-2026-114 loader","description":"Loader from phishing campaign","severity":"High",
 "expirationTime":"2026-12-31T00:00:00Z","rbacGroupNames":["Workstations"],"generateAlert":true}
```
- Types: FileSha1/FileSha256/FileMd5, IpAddress, DomainName, Url, CertificateThumbprint.
- Actions: Allow, Audit, Warn (URL/IP), Block, BlockAndRemediate.
- IP/URL indicators require **network protection** in block mode (and for non-Edge browsers rely on it); Edge uses SmartScreen.
- Certificate indicators block everything signed by that cert (useful for stolen code-signing certs) - check for legitimate use first.
- Limit 15,000 indicators per tenant; scope by device groups.

## CrowdStrike Falcon
IOC Management: hashes (SHA256/MD5) with action `prevent`/`detect`/`allow`, domains/IPs `detect` (network blocking via Firewall Management or Falcon's DNS-based features); platform scoping, host groups, expiration. API: `POST /iocs/entities/indicators/v1`.

## Safety
- Never block hashes of OS or common signed binaries; check prevalence in advanced hunting first (`DeviceFileEvents | where SHA256 == "<hash>" | summarize dcount(DeviceId)`).
- Start with Audit/Detect for IPs and domains that may be shared infrastructure.
- Always set expiry and a reference to the incident/ticket; review expiring indicators.
- Allow indicators override detections - restrict who can create them and audit.

## Verify
- [ ] Test hash (e.g. EICAR variant or custom benign test binary) blocked on a pilot device.
- [ ] Indicator list has no entries without expiry or ticket reference.
