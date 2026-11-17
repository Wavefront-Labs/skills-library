---
id: computing-software.cybersecurity-defensive.system-hardening.fortigate-hardening
name: fortigate-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [fortigate-hardening, fortinet, fortios, firewall-hardening, ssl-vpn, network-device-hardening]
level: practitioner
status: draft
description: "Harden FortiGate firewalls: admin access on trusted interfaces only, trusted hosts, MFA, admin ports, SSL VPN exposure, firmware patching, logging and config backups."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening", "https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/", "https://www.fortiguard.com/psirt", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FortiGate hardening

FortiOS edge devices have had a steady stream of actively exploited vulnerabilities (SSL VPN, management
interface). Hardening is mainly: reduce exposed management and VPN surface, and patch fast.

## Administrative access
```
config system interface
    edit "wan1"
        set allowaccess ping          # no https, ssh, http, fgfm on internet-facing interfaces
    next
    edit "mgmt"
        set allowaccess https ssh
    next
end
config system admin
    edit "netadmin"
        set trusthost1 10.0.10.0 255.255.255.0     # trusted hosts per admin
        set two-factor fortitoken                  # or email / RADIUS / SAML MFA
        set accprofile "super_admin"
    next
end
config system global
    set admin-sport 8443
    set admin-ssh-port 2222
    set admintimeout 10
    set admin-lockout-threshold 3
    set admin-lockout-duration 900
    set strong-crypto enable
    set admin-https-redirect enable
    set gui-firmware-upgrade-warning enable
end
```
- Rename or remove the default `admin` account after creating named accounts; use RBAC profiles
  (read-only for NOC).
- Prefer SSO (SAML to the IdP) or RADIUS/TACACS+ for admin auth with MFA; keep one local break-glass account.
- Local-in policies can further restrict which sources reach management services on any interface.
- Disable unused features: `set admin-telnet disable`, HTTP access, FortiGuard push if not needed, and
  `fgfm` on internet interfaces unless FortiManager requires it.

## VPN exposure
- If using SSL VPN: Fortinet has been moving customers off SSL VPN tunnel mode toward IPsec/ZTNA in recent
  FortiOS releases; check the release notes for your version. Restrict by geography or source where possible,
  require MFA (SAML), disable web mode if unused, and keep firmware current.
- IPsec: IKEv2, strong proposals (AES-GCM, DH groups 19/20/21), certificate authentication where possible.

## Patch and monitor
- Subscribe to FortiGuard PSIRT advisories; treat CISA KEV-listed FortiOS bugs as emergency changes.
- After a critical advisory, follow Fortinet's indicators of compromise guidance (unexpected admin accounts,
  files, config changes); the symlink persistence issue in 2025 showed that patching alone may not remove
  attacker access.
- Logs to FortiAnalyzer or SIEM: admin logins, config changes (`event` logs), VPN logins; alert on admin
  logins from new sources.

## Config hygiene
Encrypted config backups (`set private-data-encryption enable` for stored secrets), backups off-device,
config diffs reviewed, no "any-any" policies, logging enabled on all policies.

## Verify
External scan of WAN IPs shows no admin HTTPS/SSH; admin login from an untrusted host fails; firmware is on a
version with no known exploited vulnerabilities; config change alerts reach the SOC.
