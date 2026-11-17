---
id: computing-software.cybersecurity-defensive.network-defence.guest-wifi-isolation
name: guest-wifi-isolation
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [wireless-security, guest-wifi-isolation, client-isolation, captive-portal, owe, enhanced-open, guest-vlan, internet-only-access]
level: practitioner
status: draft
description: "Build guest Wi-Fi that gives internet only: separate VLAN/VRF, client isolation, firewall rules, OWE or portal, bandwidth limits and logging for accountability."
sources: ["CompTIA Security+ SY0-701 objectives 3.2 and 4.1 (segmentation, wireless)", "Wi-Fi Alliance Wi-Fi CERTIFIED Enhanced Open (OWE)", "NIST SP 800-153"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Guest Wi-Fi isolation

**Goal:** visitors and personal devices get internet access with no path to corporate
systems or to each other.

## Design
- **Separate SSID** mapped to a guest VLAN or, better, a separate VRF or tunnelled to a DMZ/anchor
  controller so guest traffic never enters the internal routing table.
- **Firewall policy** on the guest segment: allow DNS (to a filtering resolver), HTTP/HTTPS and
  needed ports outbound to internet; deny RFC1918 and all internal ranges explicitly; deny access to AP and controller management.
- **Client isolation** (peer-to-peer blocking) on the SSID so guests cannot attack each other.
- **Encryption**: OWE (Wi-Fi Enhanced Open) gives encryption without a password; or WPA3-Personal
  (SAE) with a rotating passphrase; captive portal for terms acceptance and registration.
- **Rate limits** per client and per SSID.
- **DNS filtering** for malware and abuse categories.

## Accountability
Captive portal sponsor or SMS registration, and logs of MAC, IP, time, user (where legally
required) in case of abuse reports.

## Personal devices of staff
Put BYOD on guest or a separate BYOD SSID with internet and only explicitly published apps (via
ZTNA/reverse proxy), not the corporate network.

## Gotchas
- Guest VLAN routed by the core switch with ACLs is easy to break with one ACL change; VRF or tunnelling is more robust.
- Allowing guests to reach internal DNS leaks internal names; use a public/filtering resolver.
- Printers or displays for guests require specific exceptions; scope them to the single device and port.

## Verify
- [ ] From a guest client: internal IP ranges and management interfaces unreachable (scan test), internet works.
- [ ] Two guest clients cannot reach each other.
