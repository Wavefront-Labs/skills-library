---
id: computing-software.systems-network-administration.windows-server.mpio-for-iscsi
name: mpio-for-iscsi
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iscsi, mpio, multipath-io, msdsm, load-balance-policy, round-robin, mpclaim, storage-paths]
level: practitioner
status: docs-checked
description: "Configure Multipath I/O for iSCSI: install MPIO, claim iSCSI devices with MSDSM, choose load-balance policy, connect multiple paths and verify failover."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/mpio/enable-msdsmautomaticclaim
  - https://learn.microsoft.com/en-us/powershell/module/mpio/set-msdsmglobaldefaultloadbalancepolicy
  - https://learn.microsoft.com/en-us/powershell/module/mpio/set-mpiosetting
  - https://learn.microsoft.com/en-us/windows-server/administration/server-core/server-core-roles-and-services
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# MPIO for iSCSI

## Install and claim
```powershell
Install-WindowsFeature Multipath-IO
Enable-MSDSMAutomaticClaim -BusType iSCSI     # BusType accepts iSCSI or SAS; run once per bus type
Restart-Computer
```
- Enable claiming and set the default policy before connecting sessions: MSDSM applies the default load balance policy only to devices it claims after you set it, and unclaimed paths show as separate disks.
- Vendor DSMs (Dell, NetApp, Pure) may replace MSDSM; follow the array's guide and do not
  mix.

## Policy
```powershell
Set-MSDSMGlobalDefaultLoadBalancePolicy -Policy RR      # Round Robin
Get-MSDSMGlobalDefaultLoadBalancePolicy
```
| Policy | Code |
|---|---|
| Clear the default | None |
| Fail Over Only | FOO |
| Round Robin | RR |
| Least Queue Depth | LQD |
| Least Blocks | LB |
Per-disk policy is changed with the `mpclaim` utility, which is not covered in the current Microsoft Learn reference. Use the array vendor's recommended policy.

## Connect each path
One `Connect-IscsiTarget ... -IsMultipathEnabled $true -IsPersistent $true` per
initiator-NIC/target-portal pair, on separate subnets.

## Timers
```powershell
Get-MPIOSetting
Set-MPIOSetting -NewPathRecoveryInterval 20 -NewPDORemovePeriod 30 -CustomPathRecovery Enabled
```
Settings covered by Set-MPIOSetting: path verification state and period, PDORemovePeriod, retry count and interval, custom path recovery time and disk timeout. `-NewPathRecoveryInterval` only applies when `-CustomPathRecovery Enabled` is set. A restart may be requested after changes.

## Verify
- [ ] The MPIO tooling (MPIO properties dialog or `mpclaim`) shows all expected paths per disk.
- [ ] Pull one storage NIC: IO continues and the path returns when reconnected.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Enable-MSDSMAutomaticClaim -BusType accepts SAS or iSCSI, run once per type; Set-MSDSMGlobalDefaultLoadBalancePolicy -Policy accepts None, FOO, RR, LQD and LB, and applies only to devices claimed after it is set; Set-MPIOSetting parameters and defaults for CustomPathRecovery; Multipath-IO is the feature name in the Server Core role table.
- Wrong claim fixed: the policy table listed RRWS (Round Robin with Subset), which the cmdlet does not accept; Least Blocks (LB) was missing.
- Removed unconfirmed details: vendor DSM examples, mpclaim syntax, event ids 16/17, the reboot-after-feature-install note, and per-policy array guidance.

Method: documentation only; no commands were run.
