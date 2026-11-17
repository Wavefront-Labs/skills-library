---
id: computing-software.systems-network-administration.active-directory.external-and-shortcut-trusts
name: external-and-shortcut-trusts
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-trusts, external-trust, shortcut-trust, realm-trust, non-transitive, kerberos-referral, trust-types, mit-kerberos]
level: practitioner
status: gated
description: "Choose and build the right trust type: external (single domain, non-transitive, NTLM-friendly), shortcut (speed up referrals in big forests), realm (MIT Kerberos)."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc775736(v=ws.10)
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-trust
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External, shortcut and realm trusts

## Trust types at a glance
| Type | Transitive | Use |
|---|---|---|
| Parent-child / tree-root | yes, two-way | created automatically inside a forest |
| Forest | yes | one-way or two-way; share resources between whole forests |
| External | no | one-way or two-way; access to a Windows NT 4.0 domain or a domain in a separate forest not joined by a forest trust |
| Shortcut | yes | one-way or two-way; improves logon times between two domains in the same forest |
| Realm | transitive or non-transitive | one-way or two-way; with a non-Windows Kerberos realm |

## External trust
```cmd
netdom trust res.ad.example.com /domain:partner.example /twoway /add ^
  /usero:RES\admin /passwordo:* /userd:PARTNER\admin /passwordd:*
```
- SID filtering (quarantine) is on by default for external trusts (gated: unconfirmed, source is paywalled or blocked). Check or set it with `netdom trust ... /quarantine`.
- Prefer a forest trust where both sides are AD and you need access to more than one domain.

## Shortcut trust
When users in `emea.ad.example.com` constantly use resources in `apac.ad.example.com`,
Kerberos walks up to the root and back down. A shortcut trust cuts that to one hop:
```cmd
netdom trust emea.ad.example.com /domain:apac.ad.example.com /twoway /add /usero:... /userd:...
```
Benefit: fewer referrals, less dependency on forest-root DCs across the WAN.

## Realm trust
For a non-Windows Kerberos realm, create the trust with `netdom trust <domain> /domain:<REALM> /add /realm /passwordt:*`; `/passwordt` (the trust password) is required, and `/transitive:yes` makes a realm trust transitive. Configure the matching trust principal on the non-Windows KDC using that platform's documentation.

## Verify
- [ ] `Get-ADTrust -Filter *` lists the trust.
- [ ] `netdom trust ... /verify` succeeds.

## Checked
Checked 2026-10-27 against Microsoft Learn (Trust types, Windows Server 2003 documentation; netdom trust reference).
- Confirmed: trust types, transitivity and direction table; netdom /add /twoway /realm /passwordt /transitive /quarantine syntax.
- Wrong in the earlier text: the external-trust netdom example had the /usero and /userd accounts swapped.
- Gated: SID filtering being on by default for external trusts (the netdom page lists `/quarantine` default as No).
- Removed: the NTLM fallback claim, MIT-side principal steps and altSecurityIdentities mapping, Get-ADTrust property names and the klist referral check.

Method: documentation only; no commands were run.
