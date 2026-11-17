---
id: computing-software.systems-network-administration.network-design.cisco-secure-client-remote-access
name: cisco-secure-client-remote-access
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, access-management, anyconnect, secure-client, ssl-vpn, remote-access-vpn, dtls]
level: practitioner
status: docs-checked
description: "Deploy Cisco Secure Client (AnyConnect) remote access VPN on ASA/FTD: TLS/DTLS and IKEv2, group policies, split tunnelling, posture, MFA via SAML/RADIUS and troubleshooting."
sources:
  - https://www.cisco.com/c/en/us/support/security/anyconnect-secure-mobility-client-v4-x/series.html
  - https://www.cisco.com/c/en/us/td/docs/security/asa/asa920/configuration/vpn/asa-920-vpn-config/vpn-anyconnect.html
  - https://www.cisco.com/c/en/us/td/docs/security/secure-firewall/management-center/device-config/740/management-center-device-config-74/vpn-remote-access.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cisco Secure Client remote access

Cisco Secure Client (formerly AnyConnect) is the endpoint VPN client for ASA and Secure Firewall
(FTD) headends.

## Transport
- TLS to connect, with optional DTLS (Cisco: DTLS avoids latency and bandwidth problems of some SSL connections and improves real-time applications). Without DTLS the session uses TLS.
- Alternatively IPsec/IKEv2 (the client supports both SSL and IPsec/IKEv2).

## Headend objects
- **Connection profile (tunnel group)**: authentication (SAML 2.0, RADIUS with MFA,
  certificates), address pool, group alias/URL.
- **Group policy**: DNS servers, split tunnel lists, banner, idle/session timeouts, client profile
  settings.
- Address pools sized for peak concurrent users plus headroom; routed back to the headend.

## Split tunnelling
- Tunnel all (most secure, highest headend load), split include (only corporate subnets), or
  split exclude (everything except listed destinations).
- Split DNS for internal domains.

## Posture and modules
Endpoint posture checks and dynamic access policies are available; see the Cisco configuration guide for the modules your release supports.

## Troubleshooting
- Client: collect the diagnostics bundle and check whether the session uses DTLS or TLS.
- ASA: use the session-database show commands and webvpn debugging described in Cisco's guide.
- Common faults: certificate name mismatch/untrusted chain, DTLS blocked (falls back to TLS), MTU
  (see the guide's Adjust MTU Size section), overlapping home LAN subnets, pool exhaustion.

## Verify
- [ ] Test user connects with MFA, gets DTLS, reaches internal apps, split tunnel and DNS behave per policy; capacity report shows sessions vs licence and pool size.

## Checked

- Date: 2026-10-28
- Confirmed: ASA AnyConnect/Secure Client guide: TLS with optional DTLS, SSL and IPsec/IKEv2 connections, SAML 2.0 support, Adjust MTU Size and DPD/OMTU sections.
- Removed: port numbers, split-exclude dynamic domain feature, posture and Umbrella module claims, DART, specific ASA commands and the 1300-1400 MTU range (the Cisco client series page returned 404).
Method: documentation only; no commands were run.
