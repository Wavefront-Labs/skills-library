---
id: computing-software.cybersecurity-defensive.security-architecture.sase-sse-architecture
name: sase-sse-architecture
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [zero-trust, sase, sse, ztna, secure-web-gateway, casb, fwaas, network-architecture]
level: advanced
status: draft
description: "Design a SASE/SSE architecture: ZTNA replacing VPN, SWG and CASB for internet and SaaS, FWaaS, traffic steering, identity integration and phased migration."
sources: ["https://www.cisa.gov/zero-trust-maturity-model", "https://csrc.nist.gov/pubs/sp/800/207/final", "https://www.gartner.com/en/information-technology/glossary/secure-access-service-edge-sase"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SASE and SSE architecture

**Goal:** apply consistent security to users wherever they work, with access to private
apps and the internet brokered by cloud security services instead of backhauling to a
data-centre VPN and firewall stack.

## Components
- **SSE (Security Service Edge):** cloud-delivered security:
  - **ZTNA:** per-application access to private apps, identity and device posture checked per
    session, apps not exposed to the internet (connectors dial out).
  - **SWG:** URL filtering, TLS inspection, malware scanning, DNS security for internet traffic.
  - **CASB:** SaaS visibility (shadow IT), inline controls (block uploads to personal storage),
    API-based scanning of sanctioned SaaS.
  - **DLP** across the above; **FWaaS** for non-web traffic; **RBI** for risky sites.
- **SASE** = SSE + SD-WAN networking (branch connectivity, path selection), ideally converged.

## Design decisions
1. **Identity:** integrate with the IdP (SAML/OIDC, SCIM for groups); policies by group and
   device posture.
2. **Traffic steering:** endpoint agent (best coverage, posture), PAC/proxy, GRE/IPsec tunnels
   from branches, DNS-based for unmanaged. Decide what bypasses (e.g. Teams media, banking
   sites from TLS inspection) and document why.
3. **TLS inspection:** required for meaningful SWG/DLP; deploy the inspection CA via MDM;
   exempt privacy-sensitive categories (health, finance) per legal guidance and certificate-pinned apps.
4. **Private app access:** connectors near apps (data centre, VPCs); segment by app,
   not network.
5. **Logging:** stream SSE logs to the SIEM; they replace firewall/proxy logs for remote users.
6. **Resilience:** fail-open vs fail-closed per traffic type; multiple PoPs; break-glass access path.

## Migration path
Start with SWG for remote users, then ZTNA for a few web apps with a pilot group, expand to
non-web apps, retire VPN for most users, then branch SD-WAN integration. Keep VPN for
exceptions during transition.

## Gotchas
- Lifting VPN rules ("all users to 10.0.0.0/8") into ZTNA defeats the point; define
  per-app policies from actual usage.
- Single vendor vs best-of-breed: integration and one policy plane matter more than
  feature checklists.
- Latency to PoPs and local regulations (data residency for inspected traffic) vary by region.

## Verify
Remote user test matrix: allowed app reachable, other private IPs not reachable, malicious URL
blocked, upload to unsanctioned storage blocked, all events visible in the SIEM.
