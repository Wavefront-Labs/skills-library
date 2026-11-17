---
id: computing-software.systems-network-administration.active-directory.replication-metadata-showobjmeta
name: replication-metadata-showobjmeta
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-replication, replication-metadata, repadmin, showobjmeta, get-adreplicationattributemetadata]
level: advanced
status: docs-checked
description: "Read AD replication metadata to find which DC and when an attribute changed: repadmin /showobjmeta, Get-ADReplicationAttributeMetadata and version numbers."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742104(v=ws.11)
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adreplicationattributemetadata
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replication metadata with repadmin /showobjmeta

Every replicated attribute carries metadata: originating DC (invocation ID), originating time, originating
USN, local USN and a **version** number. It answers "who changed this, where and when" without auditing.

## Read it
```cmd
repadmin /showobjmeta DC01 "CN=jsmith,OU=Users,DC=ad,DC=example,DC=com"
```
The output shows, per attribute, the version number, the originating and local USNs, the originating server and the time stamp. You can name the object by DN, GUID (`"<GUID=...>"`) or SID (`"<SID=...>"`).
```powershell
Get-ADReplicationAttributeMetadata -Object "CN=Domain Admins,CN=Users,DC=ad,DC=example,DC=com" -Server DC01 -ShowAllLinkedValues |
  Sort-Object LastOriginatingChangeTime | Format-List *
```
For linked attributes such as `member`, add `/linked` to repadmin (documented as valid when the forest functional level is
Windows Server 2003) or `-ShowAllLinkedValues` to the cmdlet. Add `-IncludeDeletedObjects` for deleted objects.

## Uses
- Who added someone to Domain Admins: originating DC and time; then check that DC's Security log (4728/4732/4756)
  at that time for the account.
- Compare versions across DCs: a DC with a lower version for the same attribute has not replicated it.

## Gotchas
- Compare the same object on several DCs by passing a DC list to repadmin; a DC showing an older version has not yet received the change.

## Verify
- [ ] The originating DC and time match a Security log event for the change.

## Checked
2026-10-27, against the repadmin /showobjmeta page (Learn previous-versions, Windows Server 2012 R2), the Get-ADReplicationAttributeMetadata cmdlet page, and the Appendix L events table (windowsserverdocs). Confirmed: /showobjmeta syntax with DSA_LIST, DN/GUID/SID object references and the /linked switch; what the metadata contains; the cmdlet's -Object, -Server, -ShowAllLinkedValues and -IncludeDeletedObjects parameters and the LastOriginatingChangeTime property; security events 4728, 4732 and 4756 (member added to a global, local or universal group). Removed as unconfirmed: the conflict-winner rule, the pwdLastSet remark, the 100,000-per-day version bump, the LastOriginatingDeleteTime and other property names, and the clock-skew remark.

Method: documentation only; no commands were run.
