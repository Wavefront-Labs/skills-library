---
id: computing-software.systems-network-administration.active-directory.tgt-delegation-across-forest-trusts
name: tgt-delegation-across-forest-trusts
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-trusts, enable-tgt-delegation, unconstrained-delegation, forest-trust]
level: advanced
status: gated
description: "Control Kerberos TGT delegation across forest trusts: the default block since 2019, netdom /EnableTGTDelegation, and moving apps to constrained delegation."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-trust
  - https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-constrained-delegation-overview
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adaccountcontrol
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# TGT delegation across forest trusts

Unconstrained delegation lets a service receive a copy of the user's TGT. Across a forest trust that means a
compromised server in forest B could act as users from forest A anywhere. TGT delegation across incoming forest trusts is **blocked by default** on updated systems (gated: unconfirmed, source is paywalled or blocked); the netdom `/EnableTgtDelegation` switch controls it.

## Symptoms
- Double-hop apps (web front end to SQL, IIS to file share) work for users from the local forest and fail for
  users from the trusted forest with access denied or a fallback to NTLM.

## Check the trust setting
```cmd
netdom trust <TrustingForest> /domain:<TrustedForest> /EnableTgtDelegation
```
Without `:yes|:no` it reports the current state. The switch enables or disables Kerberos full delegation on outbound forest trusts. When set to No, services in the other forest that are configured to be trusted for delegation to any service cannot use Kerberos full delegation with any account in this forest.

## Preferred fix: stop using unconstrained delegation
- Convert the front-end service to **resource-based constrained delegation**, configured on the back-end resource (`Set-ADComputer SQL01 -PrincipalsAllowedToDelegateToAccount WEB01$`). Microsoft documents constrained delegation across domains; confirm cross-forest behaviour in your environment (gated: unconfirmed, source is paywalled or blocked).
- Or classic constrained delegation, configured by an administrator on the front-end service account.

## Last resort: re-enable (accept the risk)
```cmd
netdom trust corp.example.com /domain:partner.example.org /EnableTgtDelegation:yes
```
Document the risk owner. Restrict which hosts have unconstrained delegation in the trusted forest to as few as
possible and mark privileged users "Account is sensitive and cannot be delegated" (`Set-ADAccountControl -AccountNotDelegated $true`).

## Verify
- [ ] Double-hop works for cross-forest users with RBCD and TGT delegation left disabled.
- [ ] `Get-ADComputer -Filter {TrustedForDelegation -eq $true}` lists only the hosts you intend.

## Checked
Checked 2026-10-27 against Microsoft Learn (netdom trust reference; Kerberos constrained delegation overview; Set-ADComputer, Set-ADAccountControl and Get-ADComputer references, Windows Server 2025).
- Confirmed: netdom /EnableTgtDelegation behaviour on outbound forest trusts; Set-ADComputer -PrincipalsAllowedToDelegateToAccount; Set-ADAccountControl -AccountNotDelegated; constrained delegation across domains.
- Gated: the default-blocked statement and cross-forest RBCD behaviour.
- Removed: the July 2019 update date, the Kerberos event numbers 14 and 16, and the which-side-runs-it claim.

Method: documentation only; no commands were run.
