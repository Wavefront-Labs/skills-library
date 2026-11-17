---
id: computing-software.systems-network-administration.windows-server.active-directory-based-activation
name: active-directory-based-activation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-activation, active-directory-based-activation, adba, activation-object, vamt, csvlk, volume-activation, gvlk]
level: practitioner
status: docs-checked
description: "Activate domain-joined Windows and Office with AD-based activation: create the activation object with the CSVLK, how clients activate, and coexistence with KMS."
sources:
  - https://learn.microsoft.com/en-us/windows/deployment/volume-activation/activate-using-active-directory-based-activation-client
  - https://learn.microsoft.com/en-us/windows/deployment/volume-activation/active-directory-based-activation-overview
  - https://learn.microsoft.com/en-us/windows-server/get-started/activation-slmgr-vbs-options
  - https://learn.microsoft.com/en-us/windows-server/get-started/kms-activation-planning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active Directory-based activation (ADBA)

**What:** the KMS host key (CSVLK) is submitted to Microsoft and stored as an **activation object** in AD DS.
Domain-joined machines with a GVLK activate by receiving it from a domain controller. No KMS host, no RPC (it uses
LDAP), and it works with RODCs. It works within a single forest only: each forest needs its own object.

## Requirements
- Forest schema updated with adprep.exe from a supported server OS (VAMT route: domain schema level Windows Server
  2012 R2 or later); older DCs can still activate clients afterwards.
- Clients: a supported Windows OS with a GVLK installed.
- Domain Admin and Enterprise Admin membership, because setup changes forest-wide settings.
- For Office CSVLKs, install the matching Office Volume License Pack on the server running the role first.

## Create the activation object
Volume Activation Tools (on any server with the role tools):
```powershell
Install-WindowsFeature VolumeActivation -IncludeManagementTools
vmw.exe      # Volume Activation Tools > Active Directory-Based Activation > enter CSVLK > name it > Activate online/phone
```
Or `slmgr /ad-activation-online <CSVLK> "<object name>"` (needs read/write access to the activation object
container in the forest root domain; local admin is not required). Phone mode: `/ad-activation-get-IID <CSVLK>`
then `/ad-activation-apply-cid <CSVLK> <CID> [name]`. Repeat for Office CSVLKs.

## How clients behave
- After the Licensing service starts the client contacts AD DS, receives the activation object and activates; it
  then stays activated up to 180 days since last domain contact and by default retries every 7 days. The client
  compares the object with the edition defined by its GVLK.
- If the object cannot be retrieved, the client uses KMS activation.
- Workgroup machines and older volume-licensed OSes and applications still need a KMS host or MAK.
- If the computer leaves the domain and the Software Protection service or computer restarts, it becomes Not
  Activated and tries KMS.

## Manage
```cmd
slmgr /ao-list                  list activation objects
slmgr /del-ao <object DN>       remove one
slmgr /dlv                      on a client: shows whether KMS was used
```

## Verify
- [ ] A new domain-joined server with a GVLK shows Activated after sign-in (`slmgr /dlv`); if KMS also exists, test with KMS disabled.
- [ ] `slmgr /ao-list` shows objects for current Windows Server and Office versions.

## Checked

2026-10-27. Documentation release: Microsoft Learn Activate using Active Directory-based activation (updated 2025-05-14), ADBA overview (2025-06-10), slmgr options page. Confirmed: single-forest scope, LDAP not RPC, RODC support, adprep and schema level, Enterprise Admin requirement, vmw.exe route, Office VL pack, 180-day and 7-day behaviour, fallback to KMS, all /ad-activation-*, /ao-list and /del-ao options. Removed the activation-object container path, the 'ADBA first' claim and the quoted /dlv output as unconfirmed.

Method: documentation only; no commands were run.
