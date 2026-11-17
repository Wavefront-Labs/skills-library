---
id: computing-software.systems-network-administration.active-directory.virtual-dc-cloning
name: virtual-dc-cloning
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, virtualized-domain-controller, dc-cloning, new-addccloneconfigfile, get-addccloningexcludedapplicationlist, cloneable-domain-controllers, hyper-v, rapid-dc-deployment]
level: advanced
status: docs-checked
description: "Clone a virtual DC safely: Cloneable Domain Controllers group, app allow list, New-ADDCCloneConfigFile, export/import with a new ID, and checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/virtual-dc/virtualized-domain-controller-deployment-and-configuration
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-addccloneconfigfile
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-addccloningexcludedapplicationlist
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Clone a virtual domain controller

**Goal:** stamp out a new DC from an existing virtual DC in minutes instead of promoting.
Relies on VM-GenerationID, so the hypervisor must support it.

## Requirements
- Source DC: Windows Server 2012+ guest on a hypervisor that supports VM-GenerationID.
- The PDC emulator FSMO role must be hosted on a Windows Server 2012+ DC and be online
  and reachable (over RPC) when cloning starts. Microsoft's guide says writable DCs, RODCs,
  global catalogs and FSMO holders all support cloning.

## Steps
1. Authorise the source: add the source DC's computer account to the
   **Cloneable Domain Controllers** group.
2. Check installed apps/services that are not on the default allow list:
```powershell
Get-ADDCCloningExcludedApplicationList
Get-ADDCCloningExcludedApplicationList -GenerateXml -Path <DSA_WORKING_DIR> -Force   # writes CustomDCCloneAllowList.xml
```
Uninstalling an incompatible program or service is the recommended fix; any one left off
both allow lists prevents cloning. Only add software you know survives a machine identity
change to `CustomDCCloneAllowList.xml`.
3. Create the clone config on the source:
```powershell
New-ADDCCloneConfigFile -CloneComputerName DC05 -SiteName LON `
  -Static -IPv4Address 10.0.0.25 -IPv4SubnetMask 255.255.255.0 -IPv4DefaultGateway 10.0.0.1 `
  -IPv4DNSResolver 10.0.0.10,10.0.0.11
```
Without `-Path` this writes `DCCloneConfig.xml` to the DSA working directory (default
`%systemroot%\ntds`); `-Path` picks another folder and `-Offline` skips the online tests.
`-Static` is required when you give the static IPv4 arguments.
4. Shut down the source, then **export** and **import as copy with new ID**:
```powershell
Export-VM -Name DC04 -Path <EXPORT_DRIVE>:\Export
Import-VM -Path '<EXPORT_DRIVE>:\Export\DC04\Virtual Machines\<GUID>.vmcx' -Copy -GenerateNewId -VirtualMachinePath <EXPORT_DRIVE>:\VMs\DC05 -VhdDestinationPath <EXPORT_DRIVE>:\VMs\DC05
```
5. Optionally restart the source DC, and make sure the PDC emulator is online. Start the clone:
   it detects the new generation ID, looks for `DCCloneConfig.xml` and promotes itself under
   the name in that file.

## Failure modes
- Clone boots into Directory Services Repair Mode: read `%systemroot%\debug\dcpromo.log`
  and the Directory Service event log; typical causes are an incompatible program or service,
  a duplicate or invalid name or IP in the XML, no DHCP when no IP is given, the PDC emulator
  not reachable over RPC, or the DC not being in Cloneable Domain Controllers.

## Verify
- [ ] `Get-ADDomainController DC05` shows a new DC in the right site.
- [ ] Replication from and to the clone is healthy and the source DC is still healthy.

## Checked

Documentation: Microsoft Learn virtualized domain controller deployment guide and the
Get-ADDCCloningExcludedApplicationList / New-ADDCCloneConfigFile / Import-VM cmdlet references
(Windows Server 2025 module docs), from the public GitHub sources, MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: PDC emulator must be online and on 2012+; FSMO holders can be cloned (the earlier
"not an FSMO holder" and "PDC cannot be cloned" statements were wrong and removed);
`-GenerateXml -Path -Force` and the CustomDCCloneAllowList.xml name; New-ADDCCloneConfigFile
parameters, default location and `-Static` requirement; Import-VM `-Copy -GenerateNewId
-VirtualMachinePath -VhdDestinationPath`. Removed unconfirmed steps (Rename-VM, group clean-up).

Method: documentation only; no commands were run.
