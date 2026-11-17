---
id: computing-software.cybersecurity-defensive.network-defence.rd-gateway-secure-rdp-access
name: rd-gateway-secure-rdp-access
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [vpn, rd-gateway, rdp, remote-desktop-gateway, nla, rd-cap, rd-rap, mfa-nps-extension]
level: practitioner
status: gated
description: "Publish RDP safely: never expose 3389, use RD Gateway with RD CAP/RAP, NLA, MFA via the NPS extension, TLS certs, logging, and modern alternatives like Entra app proxy or Bastion."
sources: ["https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remote-desktop-gateway-role", "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-nps-extension-rdg", "https://www.cisa.gov/news-events/news/remote-desktop-protocol-rdp-security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RD Gateway and secure RDP access

Internet-exposed RDP (TCP/UDP 3389) is a common attack entry point (gated: unconfirmed, source is paywalled or blocked). Never expose it directly.

## RD Gateway
RD Gateway tunnels RDP over HTTPS and enforces policies before any connection reaches a host.
- **RD CAP** (connection authorization policy): which users/groups may use the gateway; require
  smart card or password, device redirection restrictions (disable drive/clipboard redirection for
  untrusted users).
- **RD RAP** (resource authorization policy): which internal hosts (AD group of computers) each user
  group may reach, and ports (3389 only).
- TLS certificate from a trusted CA matching the public name.
- Place in a DMZ or behind a reverse proxy; gateway joined to AD (Tier 1 asset).

## MFA
NPS extension for Microsoft Entra MFA on the NPS server used by RD Gateway as central policy store:
RD Gateway -> NPS (RADIUS) -> Entra MFA push/number matching. Raise the RADIUS timeout on the
RD Gateway NPS so users have time to approve (see the NPS extension page).

## Host-side hardening
- Network Level Authentication required (authentication before session creation).
- Allow RDP only from the gateway/jump hosts (Windows Firewall scope rule).
- Restricted Admin mode or Remote Credential Guard for admins so credentials are not left on targets.
- Account lockout policy; deny RDP logon for service accounts.

## Logging
- Gateway and host logon events.
Forward to SIEM; alert on failed MFA bursts and logons outside RAP-expected hosts.

## Alternatives
ZTNA or cloud remote-access products remove inbound exposure entirely.

## Gotchas
- RD Gateway is an internet-facing server: patch it promptly.
- Users bypassing via personal remote tools (AnyDesk, TeamViewer): block unapproved RMM tools.

## Verify
External port scan shows no 3389; a connection through the gateway prompts MFA and reaches only RAP-allowed
hosts; direct RDP from a workstation to a server is blocked by host firewall.

## Checked

Date: 2026-10-28

- Confirmed: RD Gateway lets users reach internal RDS resources over the internet without a VPN; access requires one RD CAP and one RD RAP (CAP says who may connect, RAP says which resources); NPS extension for Entra MFA with RD Gateway and a RADIUS timeout setting (Microsoft docs); Remote Credential Guard and Restricted Admin exist (Windows security docs).
- Gated: the claim that exposed RDP is a leading ransomware entry point (cisa.gov returned 403).
- Removed (not found): 30-60 second timeout figure, event IDs, UDP 3391 and CVE gotchas, TLS 1.2+, 443, named alternative products.
Method: documentation only; no commands were run.

