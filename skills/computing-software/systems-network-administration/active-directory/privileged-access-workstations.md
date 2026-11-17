---
id: computing-software.systems-network-administration.active-directory.privileged-access-workstations
name: privileged-access-workstations
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, privileged-access, ad-tiering, paw, privileged-access-workstation, jump-server, tier-0, deny-logon, clean-source]
level: advanced
status: docs-checked
description: "Build and enforce privileged access workstations for AD admins: clean-source principle, hardening baseline, tiered deny-logon GPOs, and admin account separation."
sources:
  - https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-devices
  - https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/implementing-least-privilege-administrative-models
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Privileged access workstations (PAWs)

**Clean source principle:** a system that controls another must be at least as trusted. If
a Domain Admin types credentials on a laptop that browses the web, the laptop's attacker owns
the domain. A PAW is a dedicated, hardened device used only for admin work.

## Account separation
Each admin has: a daily account (email, web), and per-tier admin accounts
(for example `adm0-jsmith` for Tier 0, `adm1-jsmith` for servers). Admin accounts have no mailbox, are
in Protected Users, marked *Account is sensitive and cannot be delegated*, and (Tier 0) in an authentication policy silo.

## PAW build
- Dedicated hardware (or the PAW is the host and daily use is a VM on it, never the reverse).
- Microsoft's device guidance lists for the privileged profile: TPM 2.0, UEFI Secure Boot, BitLocker, HVCI,
  Credential Guard, application control (AppLocker), applications installed only by the management system, and
  removal of local admin rights.
- **No general internet browsing or email**: the privileged profile uses a deny-by-default URL list. Opening a few
  well-known administrative portals is different from browsing arbitrary websites.
- Managed from Tier 0 (separate OU, separate GPOs, own management scope).
- Tier 0 PAWs are members of the Tier 0 silo.

## Enforce tier boundaries with user rights (GPO)
- In GPOs linked to the OUs of **lower-tier servers and workstations**, add the Tier 0 groups (Domain Admins,
  Enterprise Admins, your Tier 0 admin group) to the user rights *Deny access to this computer from the network*,
  *Deny log on as a batch job*, *Deny log on as a service*, *Deny log on locally* and *Deny log on through Remote
  Desktop Services* (the rights Microsoft lists for the Enterprise Admins group).
- On workstations: deny Tier 1 admin groups similarly.
- DCs: only Tier 0 can log on.

## Jump servers
If PAWs per admin are not feasible, a hardened jump server per tier can reduce risk, but
the device used to reach it must still be clean; a jump server reached from a normal laptop
protects much less.

## Verify
- [ ] A Domain Admin logon attempt to a member server is denied by policy.
- [ ] PAW cannot reach arbitrary internet sites.
- [ ] Admin accounts have no mailboxes and are in Protected Users.

## Checked
2026-10-27, against the Learn pages "Securing devices as part of the privileged access story" (privileged-access-devices, updated 2024-01) and "Enterprise access model", plus windowsserverdocs "Implementing Least-Privilege Administrative Models" and the Protected Users and Appendix pages. Confirmed: clean-source reasoning; PAW as the highest security configuration that blocks email and web browsing; device controls (TPM 2.0, Secure Boot, BitLocker, HVCI, Credential Guard, AppLocker, no local admin, apps installed only by the management system, deny-by-default URLs); the five deny user rights for Enterprise Admins on member servers and workstations; Protected Users and sensitive-account flags. Removed as unconfirmed: Defender ASR rules, WDAC, and named Intune/ConfigMgr scoping.

Method: documentation only; no commands were run.
