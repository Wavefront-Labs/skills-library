---
id: computing-software.cybersecurity-defensive.security-architecture.out-of-band-management-network
name: out-of-band-management-network
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [network-segmentation, management-network, out-of-band-management, oob, bmc-ipmi, console-servers, network-architecture]
level: advanced
status: draft
description: "Build an out-of-band management network: isolate BMCs, switch and firewall management, console servers, independent access paths and monitoring for admin interfaces."
sources: ["https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-061a", "https://www.nsa.gov/Portals/75/documents/what-we-do/cybersecurity/professional-resources/csi-network-infrastructure-security-guide.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Out-of-band management network

**Goal:** management interfaces (BMC/iLO/iDRAC/IPMI, switch/router/firewall management,
hypervisor management, storage controllers, console servers) live on a separate network
that users and attackers on production networks cannot reach, and that still works when
production is down.

## Why
Management planes give total control (reflash firmware, reconfigure firewalls, mount
virtual media). They are frequently unpatched and use weak default auth; BMC
vulnerabilities and exposed management interfaces are regular entries in CISA advisories.

## Design
- **Dedicated management network:** separate VLANs/VRF at minimum; physically separate
  switches for high-assurance environments. No routing from user or server networks.
- **Access path:** admins reach it only via a management bastion/jump host (MFA, PAM) or a
  dedicated management VPN, from PAWs.
- **Independent connectivity (true OOB):** console servers (Opengear, Lantronix) with serial
  connections to network devices and cellular/independent WAN backup, so you can recover when
  the production network or firewall is broken or compromised.
- Device configuration: bind management services to the management interface only
  (`ip ssh source-interface`, management VRF; disable management on data interfaces);
  restrict with ACLs to management subnets.
- Disable unused management protocols: Telnet, HTTP, SNMPv1/2c (use SNMPv3), IPMI over LAN
  where not needed; change default BMC credentials; integrate with central AAA (TACACS+/RADIUS).

## Monitoring
Log all management access (AAA accounting, BMC logs where supported) to the SIEM; alert on
logins from outside expected bastion IPs, firmware updates outside change windows, and new
devices appearing on management VLANs.

## Gotchas
- Management NICs left connected to production VLANs during builds.
- Hypervisor management (vCenter/ESXi) reachable from server VLANs was central in many
  ransomware cases; treat as tier 0.
- OOB cellular gateways become an internet-facing backdoor if not hardened (MFA, no default
  credentials, allowlisted sources).

## Verify
From user and server networks, scans of management subnets find nothing reachable; a
tabletop or test where production core is "down" confirms admins can still reach devices
via OOB.
