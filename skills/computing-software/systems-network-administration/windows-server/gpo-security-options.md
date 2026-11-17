---
id: computing-software.systems-network-administration.windows-server.gpo-security-options
name: gpo-security-options
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, gp-advanced-settings, security-options, ldap-signing, smb-signing, ntlm, group-policy]
level: practitioner
status: gated
description: "Configure the Security Options node in Group Policy: LDAP signing and channel binding, SMB signing, NTLM levels, anonymous restrictions and UAC, with safe rollout order."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/security-options
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/enable-ldap-signing-in-windows-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPO Security Options

Path: Computer Configuration > Policies > Windows Settings > Security Settings > Local Policies > **Security
Options**. These are registry values under `HKLM\SYSTEM\CurrentControlSet\Control\Lsa`, `...\LanmanServer`,
etc. (see each setting's Learn page for the exact registry location).

## High-value settings
| Setting | Direction (gated: unconfirmed, source is paywalled or blocked) | Notes |
|---|---|---|
| Domain controller: LDAP server signing requirements | Require signing | check event 2889 first (Learn: logged when a client makes an unsigned LDAP bind) |
| Domain controller: LDAP server channel binding token requirements | Always (after audit) | for LDAPS |
| Network security: LDAP client signing requirements | per standard | |
| Microsoft network server/client: Digitally sign communications (always) | Enabled | |
| Network security: LAN Manager authentication level | NTLMv2 only, refuse LM and NTLM | confirm the option text on the setting's page |
| Network security: Do not store LAN Manager hash value | Enabled | |
| Network access: Do not allow anonymous enumeration of SAM accounts and shares | Enabled | |
| Network security: Restrict NTLM: ... | audit first | see restrict-ntlm |
| Interactive logon: Machine inactivity limit | per standard | |
| Accounts: Rename administrator account | per standard | LAPS handles password |
| User Account Control: Admin Approval Mode for the built-in Administrator | Enabled | |

## Rollout
1. Audit: enable LDAP interface events (`16 LDAP Interface Events` = 2) on DCs and collect 2889; NTLM audit
   policies; SMB signing is low risk on modern clients.
2. Pilot GPO on a test OU, then DC OU, then servers, then workstations.
3. Baselines: start from a vendor or Microsoft baseline and compare, rather than hand-picking.

## Gotchas
- Some options need a reboot or service restart; test each on a pilot machine.
- Security settings are generally not reverted when the GPO stops applying (see group-policy-registry-tattooing).

## Verify
- [ ] `gpresult /h` shows the winning GPO; `secedit /export /cfg c.inf` on a target shows the values.

## Checked
2026-10-28. Confirmed on the Learn Security Options and LDAP-signing pages: the setting names listed (LDAP signing, channel
binding, LAN Manager authentication level, anonymous SAM enumeration, digital signing, machine inactivity limit), event
2889 for unsigned binds and the `16 LDAP Interface Events` diagnostic set to 2. Removed as unconfirmed: the 16-hour
refresh interval, 900 s value, specific target values and defaults per release, per-option reboot behaviour, and
named baseline tooling.
Method: documentation only; no commands were run.
