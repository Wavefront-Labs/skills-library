---
id: computing-software.cybersecurity-defensive.network-defence.remote-access-vpn-hardening
name: remote-access-vpn-hardening
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [vpn, remote-access-vpn, ssl-vpn, vpn-appliance-hardening, mfa, certificate-authentication, split-tunnelling, posture-check, vpn-logging]
level: practitioner
status: draft
description: "Harden remote access VPNs: patch and expose minimally, certificate plus phishing-resistant MFA, posture checks, split-tunnel decisions and log monitoring."
sources: ["NSA/CISA Selecting and Hardening Remote Access VPN Solutions (2021)", "CISA Known Exploited Vulnerabilities catalogue (VPN appliances)", "CompTIA Security+ SY0-701 objective 3.2"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote access VPN hardening

**Goal:** remote access that is not the easiest way into your network, given that VPN
appliances are among the most exploited internet-facing systems.

## Platform
- Choose products with a record of fast patches and standards-based protocols (IKEv2/IPsec or
  well-maintained TLS VPNs); check the CISA KEV catalogue history for the vendor.
- Consider ZTNA for application-level access instead of network-level VPN where possible.

## Hardening checklist (NSA/CISA)
1. **Patch within days** for VPN CVEs, hours for KEV-listed ones; subscribe to vendor PSIRT.
2. Reduce attack surface: disable unused features (web portals, clientless access, legacy
   protocols), management interface not reachable from the internet.
3. **Authentication**: device certificate (managed devices only) plus phishing-resistant MFA
   (FIDO2 via SAML to the IdP) - not SMS or push without number matching.
4. **Posture checks**: managed device, EDR running, OS patched, disk encrypted before granting access.
5. **Authorisation**: user groups map to limited network access (not "VPN = full LAN").
6. Strong crypto only (TLS 1.2+ with AEAD ciphers, IKEv2 strong proposals).
7. Lockout/rate limiting on authentication; geo restrictions if workforce locations are known.

## Split tunnelling
- Full tunnel: all traffic through corporate controls; more bandwidth, simpler security.
- Split tunnel: SaaS/internet direct; needs endpoint web protection (SWG agent/DNS filtering) to compensate.
Decide explicitly and document compensating controls.

## Monitoring
- Forward VPN logs (auth success/failure, session start/end, assigned IP, client version) to the SIEM.
- Alerts: logins from new countries or impossible travel, many failures (spraying), sessions from hosting/VPS providers, concurrent sessions for one user.
- Run vendor integrity check tools after major CVEs; check for webshells and modified files on the appliance.

## Gotchas
- Local VPN accounts that bypass the IdP and MFA (admin, test, service): remove or restrict.
- Appliances are often outside EDR coverage; exploitation shows only in appliance logs, which attackers wipe.
- Session timeouts too long allow stolen session cookies to persist; enforce re-auth.

## Verify
- [ ] External scan shows only the VPN service port; management not exposed.
- [ ] Test login without MFA or from an unmanaged device is refused.
