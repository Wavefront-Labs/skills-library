---
id: computing-software.cybersecurity-defensive.system-hardening.bmc-idrac-ilo-hardening
name: bmc-idrac-ilo-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [firmware-security, bmc-hardening, idrac, ilo, ipmi, redfish, out-of-band-management, default-credentials]
level: practitioner
status: draft
description: "Harden server BMCs (iDRAC, iLO, XClarity, IPMI): isolated management network, disable IPMI over LAN, change defaults, directory auth with MFA, firmware updates, logging."
sources: ["https://www.cisa.gov/news-events/alerts/2013/07/26/risks-using-intelligent-platform-management-interface-ipmi", "https://media.defense.gov/2023/Jun/14/2003241405/-1/-1/0/CSI_HARDEN_BMCS.PDF", "https://www.dell.com/support/manuals/en-us/idrac9-lifecycle-controller-v6.x-series/idrac9_6.xx_ug/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BMC hardening (iDRAC, iLO, IPMI)

Baseboard management controllers have full control over the server (power, console, virtual media,
firmware) independent of the OS. A compromised BMC survives OS reinstalls and is invisible to EDR.
NSA/CISA guidance: treat BMCs as high-value targets.

## Network
- Dedicated out-of-band management VLAN, reachable only from admin jump hosts; never internet-exposed
  (Shodan lists thousands of exposed iLO/iDRAC interfaces).
- Do not use "shared LOM" mode that puts the BMC on the production NIC.
- Block BMC outbound traffic except NTP, syslog, update servers you control.

## Protocols
- **Disable IPMI over LAN** (UDP 623): IPMI 2.0 RAKP leaks password hashes to unauthenticated requests
  (offline cracking) and "cipher 0" allows auth bypass on some implementations.
- Use Redfish/HTTPS; TLS 1.2+, replace self-signed certs with your PKI.
- Disable unused services: SNMPv1/v2c, Telnet, SSH if unneeded, virtual media if unneeded.

## Accounts
- Change factory defaults (iDRAC `root/calvin`, iLO unique sticker password, Supermicro `ADMIN/ADMIN` on old
  units); remove or disable unused local accounts.
- Directory integration (LDAP/AD) with role groups, plus local break-glass in a vault.
- MFA where supported (iDRAC 9 RSA SecurID/email OTP; iLO 6 with directory and two-factor options), or
  enforce via jump host access.
- Session timeouts and lockout on failed logins.

## Firmware
- Track BMC firmware versions in inventory; patch regularly (iLO and iDRAC have had critical RCEs,
  e.g. iLO4 CVE-2017-12542 auth bypass).
- Enable firmware signature verification / Secure Boot of the BMC (iLO silicon root of trust,
  iDRAC signed firmware) and run vendor integrity checks.

## Logging
Send BMC logs (Lifecycle Controller log, iLO Integrated Management Log, security events) to the SIEM via
syslog; alert on logins, user changes, firmware updates and virtual media mounts outside maintenance windows.

## Gotchas
- Decommissioned servers keep BMC configs (credentials, directory bind accounts); wipe them.
- Host OS can reach the BMC via host interface (Redfish over USB NIC, IPMI KCS); OS admins can reset BMC
  credentials from the host in many platforms (e.g. `ipmitool user set password`).

## Verify
External scan shows no 623/443 BMC exposure, `ipmitool -I lanplus -H <bmc> ...` fails (IPMI over LAN off),
firmware versions are current in the inventory, and a test BMC login appears in the SIEM.
