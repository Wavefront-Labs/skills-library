---
id: computing-software.cybersecurity-defensive.identity-access-management.kerberos-delegation-hardening
name: kerberos-delegation-hardening
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [sso, kerberos-delegation, unconstrained-delegation, machine-account-quota, constrained-delegation, rbcd, protocol-transition, active-directory, s4u]
level: advanced
status: gated
description: "Find and fix risky Kerberos delegation in AD: unconstrained, constrained (with/without protocol transition) and RBCD, how each is abused, and replacing them safely."
sources: ["https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-constrained-delegation-overview", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/how-to-configure-protected-accounts", "https://adsecurity.org/?p=1667"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kerberos delegation hardening

Delegation lets a service act as a user to another service. Misconfigured, it lets an attacker who
controls one server impersonate anyone, including domain admins.

## Inventory (gated: unconfirmed, source is paywalled or blocked)
```powershell
# Unconstrained (excluding DCs, which always have it)
Get-ADComputer -Filter {TrustedForDelegation -eq $true -and PrimaryGroupID -ne 516} -Properties TrustedForDelegation
Get-ADUser -Filter {TrustedForDelegation -eq $true}
# Constrained, and whether protocol transition (any auth protocol) is allowed
Get-ADObject -Filter {msDS-AllowedToDelegateTo -like "*"} -Properties msDS-AllowedToDelegateTo,userAccountControl |
  Select Name, msDS-AllowedToDelegateTo, @{n='ProtocolTransition';e={($_.userAccountControl -band 0x1000000) -ne 0}}
# Resource-based constrained delegation
Get-ADComputer -Filter * -Properties msDS-AllowedToActOnBehalfOfOtherIdentity | ? {$_.'msDS-AllowedToActOnBehalfOfOtherIdentity'}
```

## Risks
- **Unconstrained**: any user authenticating to the host leaves a forwardable TGT in its memory.
  With coercion (PrinterBug/PetitPotam) an attacker makes a DC authenticate and steals the DC's TGT
  -> DCSync. Remove it from everything except DCs.
- **Constrained with protocol transition** (the trusted-to-authenticate-for-delegation flag): the service can get
  tickets for any user to the listed SPNs without that user authenticating. Compromise of that
  account = impersonate admins to those services.
- **RBCD**: whoever can write `msDS-AllowedToActOnBehalfOfOtherIdentity` on a computer (often the
  account that joined it, via `ms-DS-MachineAccountQuota` defaults) can configure delegation to it
  and take over the host.

## Fix
1. Replace unconstrained with constrained (Kerberos only) or RBCD to specific services.
2. Avoid protocol transition unless needed (web front ends doing non-Kerberos auth); restrict SPN list.
3. Protect privileged accounts: "Account is sensitive and cannot be delegated" on all admins, and
   add them to Protected Users (blocks delegation and RC4).
4. Set `ms-DS-MachineAccountQuota` to 0 and audit write permissions on computer objects.
5. Disable the Print Spooler on DCs and servers that do not print; apply EFS RPC mitigations.

## Monitor
- 5136 changes to `msDS-AllowedToDelegateTo`, `msDS-AllowedToActOnBehalfOfOtherIdentity`,
  `userAccountControl` delegation flags.
- 4769 with S4U2Self/S4U2Proxy for privileged users.

## Gotchas
- Some apps (SQL Reporting, IIS with Kerberos to back ends) rely on delegation; test with app owners.
- Changing delegation requires the service to get new tickets (`klist purge`, restart).

## Verify
Re-run the inventory: no non-DC unconstrained delegation, protocol transition only on documented
accounts, all Tier 0 accounts flagged sensitive or in Protected Users.

## Checked

2026-10-28. Confirmed against the constrained delegation overview, the protected accounts page and the adsecurity.org unconstrained delegation article: unconstrained delegation risk, protocol transition and the trusted-to-authenticate bit, 'Account is sensitive and cannot be delegated', Protected Users blocking delegation and RC4. Gated: the AD attribute names, flag value and event ids in the inventory and monitor sections. Removed: service-name retargeting claim, Transited Services detail.

Method: documentation only; no commands were run.
