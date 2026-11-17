---
id: computing-software.systems-network-administration.active-directory.demote-dc-and-metadata-cleanup
name: demote-dc-and-metadata-cleanup
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-ds, uninstall-addsdomaincontroller, dc-demotion, metadata-cleanup, domain-controller-deployment, forceremoval, ntdsutil, dead-dc, fsmo, dns-cleanup]
level: practitioner
status: docs-checked
description: "Retire a DC: graceful demotion with Uninstall-ADDSDomainController, or forced removal of a dead DC with metadata cleanup, FSMO and DNS tidy-up."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/uninstall-addsdomaincontroller
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/ad-ds-metadata-cleanup
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/demoting-domain-controllers-and-domains--level-200-
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Demote a DC, or clean up after a dead one

## A. Graceful demotion (the DC is alive and replicating)
1. Move any FSMO roles off it (`netdom query fsmo`).
2. Make sure it is not the only GC, DNS server or DHCP server in a site, and update anything
   pointing at its IP: DHCP option 006, static DNS client settings, LDAP-bound apps, RADIUS,
   network devices, time clients.
3. Demote:
```powershell
Uninstall-ADDSDomainController -Credential (Get-Credential) `
  -LocalAdministratorPassword (Read-Host -AsSecureString 'new local admin pw')
```
`-LocalAdministratorPassword` must be non-empty (you are prompted if omitted). The last DC in a domain needs
`-LastDomainControllerInDomain`; it also exposes `-RemoveApplicationPartitions`, `-IgnoreLastDnsServerForZone` and
`-RemoveDnsDelegation` for removing the domain's DNS data. Do not remove other AD DS-related roles (DNS, GPMC, RSAT)
if you will promote it again soon.
4. After reboot, remove the AD DS role. The server object remains under *Sites\<site>\Servers*: delete it only if it
   has no NTDS Settings child (a child object means another application uses it).

## B. Dead DC (will never come back)
Never power on the old DC again after this. Metadata cleanup runs on a surviving DC and needs Domain Admins or
equivalent:
- **Active Directory Users and Computers** (2008+ RSAT): Domain Controllers OU > delete the computer object > tick
  "This Domain Controller is permanently offline...". This performs metadata cleanup and tries to move any FSMO roles.
- **Or** Sites and Services: delete the NTDS Settings object under the server first, tick the same box, then delete the
  server.
- **Or** ntdsutil, connected to a replication partner of the removed DC:
```cmd
ntdsutil
metadata cleanup
connections
connect to server <PARTNER_DC_FQDN>
quit
remove selected server <REMOVED_DC_NAME>
quit
quit
```
"Access is denied" usually means the computer or NTDS Settings object is protected from accidental deletion; clear that
check box on the Object tab and retry.

Then:
1. After a forced removal, seize any FSMO roles it held from another DC (the demotion wizard warns you to do this
   immediately).
2. DNS: remove the DC's stale records (its A record and its SRV records under `_msdcs` in the domain zone, and any NS
   records) so clients are not sent to it.
3. If it was a DNS forwarder target or conditional forwarder elsewhere, update those.

## Gotchas
- A demotion that fails because it cannot reach a replication partner: use `-ForceRemoval` only when the DC truly
  cannot contact any DC in the domain topology, then run metadata cleanup from another DC.

## Verify
- [ ] `repadmin /replsummary` shows no failures to the removed DC (it should not appear).
- [ ] `dcdiag /e /q` clean; `nslookup -type=srv _ldap._tcp.dc._msdcs.<domain>` lacks the old DC.
- [ ] FSMO holders all online (`netdom query fsmo`).

## Checked

Date: 2026-10-27. Documentation: Uninstall-ADDSDomainController (Windows Server 2025 module page), "Clean up AD DS
server metadata" (updated 2025-05), "Demoting domain controllers and domains" (MicrosoftDocs/windowsserverdocs and
windows-powershell-docs, main branch).
Confirmed: parameter names and meanings (`-LocalAdministratorPassword`, `-LastDomainControllerInDomain`, `-ForceRemoval`,
`-RemoveApplicationPartitions`, `-IgnoreLastDnsServerForZone`, `-RemoveDnsDelegation`), the three metadata cleanup
methods and the ntdsutil sequence, the access-denied cause, seizing FSMO after forced removal, deleting the server
object only when it has no NTDS Settings child.
Removed unconfirmed claims: `-DemoteOperationMasterRole:$false`, the CNAME/_sites/_tcp/_udp record list, the DFSR
topology query, "reset computer password" and the unreplicated-changes warning.

Method: documentation only; no commands were run.
