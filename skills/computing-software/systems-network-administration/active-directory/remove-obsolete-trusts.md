---
id: computing-software.systems-network-administration.active-directory.remove-obsolete-trusts
name: remove-obsolete-trusts
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-trusts, remove-trust, netdom-trust, conditional-forwarder]
level: practitioner
status: gated
description: "Decommission a trust safely: find who still uses it, disable selectively, remove both sides with Remove-ADTrust or netdom, and clean up DNS forwarders."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-trust
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adtrust
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/remove-dnsserverzone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing obsolete trusts

Old trusts to divested companies or migrated domains are attack paths. Remove them, but find the dependencies first.

## 1. Inventory
```powershell
Get-ADTrust -Filter *
```

## 2. Find usage
- Foreign security principals from the partner in your groups (the ForeignSecurityPrincipals container holds them; search it and resolve each SID while the trust still exists) (gated: unconfirmed, source is paywalled or blocked).
- Authentication across the trust: on your DCs, security events **4768/4769** where the account domain is the
  partner; on the partner, the same for your domain. Two to four weeks of data.
- SID history from the partner domain on migrated users (must be gone before removal if anyone still relies on it).

## 3. Brown-out first
Turn on selective authentication (`netdom trust ... /selectiveauth:yes`, valid on outbound forest and external trusts) with no Allowed-to-Authenticate grants (gated: unconfirmed, source is paywalled or blocked), or set the trust to one direction, for a
week. Anything that breaks tells you who to talk to; reverse instantly if needed.

## 4. Remove
```cmd
netdom trust corp.example.com /domain:partner.example.org /remove /UserD:partner\admin /PasswordD:*
```
The ActiveDirectory PowerShell module has Get-ADTrust but no Remove-ADTrust; use netdom or Active Directory Domains and Trusts. Do not add `/force` to remove a trust: `/force` removes the trusted domain object and cross-reference object from the forest and can remove a child domain. `/oneside` restricts the operation to one side. Remove the trust on **both** sides.

## 5. Clean up
- Delete conditional forwarders / stub zones for the partner (`Remove-DnsServerZone partner.example.org`).
- Remove FSPs from groups; delete name suffix routing entries; remove firewall rules opened for the trust.

## Verify
- [ ] `Get-ADTrust -Filter *` no longer lists the partner on either side.
- [ ] No 4769 failures from apps in the following week.

## Checked
Checked 2026-10-27 against Microsoft Learn (netdom trust reference; Get-ADTrust, Remove-DnsServerZone and event 4768 and 4769 references, Windows Server 2025).
- Confirmed: netdom trust /remove, /oneside and /force semantics; Remove-DnsServerZone; events 4768 and 4769.
- Wrong in the earlier text: Remove-ADTrust does not exist in the ActiveDirectory module, and the netdom example used /force, which can remove a child domain; both are corrected.
- Gated: the ForeignSecurityPrincipals search and the selective-authentication brown-out effect.
- Removed: Get-ADTrust property names and the trust-account remark.

Method: documentation only; no commands were run.
