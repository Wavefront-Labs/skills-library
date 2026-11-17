---
id: computing-software.cybersecurity-defensive.system-hardening.pan-os-hardening
name: pan-os-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [pan-os-hardening, palo-alto, management-interface, globalprotect, firewall-hardening, network-device-hardening]
level: practitioner
status: draft
description: "Harden Palo Alto PAN-OS management: dedicated management network, permitted IPs, admin roles and MFA, disabling management on data interfaces, GlobalProtect, and patching."
sources: ["https://docs.paloaltonetworks.com/best-practices/10-2/administrative-access-best-practices", "https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin", "https://security.paloaltonetworks.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PAN-OS management hardening

Palo Alto's own advisories (for example the 2024 management interface and GlobalProtect vulnerabilities) stress
that exposed management interfaces are the main risk. Their administrative access best practices are the
baseline.

## Management interface
- Connect the MGT port to a dedicated out-of-band management network, never internet-reachable.
- **Permitted IP addresses** on the management interface (Device > Setup > Interfaces > Management): only
  jump hosts/PAWs and Panorama.
- Services on MGT: HTTPS, SSH, and only needed others (SNMP, User-ID, HTTP OCSP); disable HTTP and Telnet.
- **Interface management profiles** on data-plane interfaces: do not attach profiles allowing HTTPS/SSH to
  untrusted zones; if management must traverse a data interface, restrict with permitted IPs and use a
  separate zone.
- Captive portal / GlobalProtect portals are separate from device management; keep them on dedicated
  interfaces/addresses.

## Administrators
- Named admin accounts with **role-based admin profiles** (custom roles with least privilege; superuser only for
  a few).
- Authentication profile with SAML or RADIUS/TACACS+ and **MFA**; local break-glass account with long
  password stored in a vault.
- Password complexity and lockout (Device > Setup > Management > Minimum Password Complexity), idle timeout,
  `failed attempts` and lockout time in the authentication profile.
- Rename/disable the default `admin` account after setup.

## Platform settings
- Enable **FIPS-CC mode** where required (resets device; plan ahead).
- SSL/TLS service profile for management with TLS 1.2+.
- Login banner; NTP with authentication; certificate for management from internal CA.
- Configuration logs and system logs to Panorama/SIEM; alert on admin logins and commits.
- Commit/config audit: require descriptions on commits; Panorama templates enforce settings across devices.

## GlobalProtect and exposed services
Keep GlobalProtect portal/gateway patched urgently, enable threat prevention on the GlobalProtect interface
traffic where applicable, use certificate + MFA authentication, and monitor for advisory IoCs.

## Patching
Track PAN-OS preferred releases, subscribe to security advisories, apply hotfixes for critical issues quickly,
and use threat prevention signatures released for specific CVEs as interim protection when available.

## Verify
External scan shows no management services; `show admins` and the admin role list match the access register;
login from a non-permitted IP fails; software version has no open critical advisories.
