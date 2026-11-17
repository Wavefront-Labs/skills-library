---
id: computing-software.cybersecurity-defensive.system-hardening.default-credentials-removal
name: default-credentials-removal
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [least-functionality, default-credentials, vendor-default-passwords, device-onboarding, credential-scanning, cis-control-4]
level: practitioner
status: draft
description: "Find and eliminate vendor default credentials on devices, appliances and applications: onboarding checklist, authenticated scanning for defaults, and unique passwords in a vault."
sources: ["CIS Controls v8 - Safeguard 4.7 Manage Default Accounts", "CISA Secure by Design - Eliminating default passwords", "NIST SP 800-53 Rev 5 IA-5 Authenticator Management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Default credentials removal

**Goal:** no device or application in the estate accepts a vendor default or shared factory password.

## Where defaults hide
Network gear (admin/admin, cisco/cisco), printers and MFPs, IP cameras and NVRs, BMCs (iLO/iDRAC/IPMI ship unique passwords now, older units do not), UPS/PDU cards, storage arrays, hypervisor appliances, databases (`sa`, `postgres` without password), app servers (Tomcat manager), CMS installers, IoT/OT devices, cloud marketplace images with documented default users.

## Onboarding checklist (every new device/app)
1. Change or disable every default account before connecting it to production networks.
2. Generate a unique random credential per device; store in the password vault (CyberArk, Vault, 1Password, Bitwarden) with owner and device id.
3. Disable unused accounts and default SNMP communities (`public`/`private`).
4. Integrate with central auth (RADIUS/TACACS+/LDAP/SSO) where supported, keeping one break-glass local account.

## Discovery of existing defaults
- Vulnerability scanner default-credential checks (Nessus "Default Unix Accounts" family, plugin families for web/admin consoles); authorise this scanning since it attempts logins.
- Nmap NSE: `http-default-accounts`, `snmp-brute` with vendor lists, `ipmi-brute`.
- Nuclei `default-logins` templates for web consoles.
- Watch account lockout policies when testing.

## Response when found
Change immediately, check logs for prior logins from unexpected sources, and treat as a potential compromise if the device was internet-exposed.

## Gotchas
- Factory reset restores defaults; include re-hardening in RMA/reset procedures.
- Shared "standard" password across all switches is effectively a default once one leaks.

## Verify
- [ ] Default-credential scan of all segments returns no successful logins.
- [ ] Vault contains an entry for every managed device in the asset inventory.
