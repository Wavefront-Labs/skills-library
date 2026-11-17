---
id: computing-software.systems-network-administration.windows-server.adfs-farm-behavior-level-upgrade
name: adfs-farm-behavior-level-upgrade
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-fs, adfs-farm-behavior-level, fbl, adfs-upgrade, windows-server-2025]
level: advanced
status: docs-checked
description: "Upgrade an AD FS farm by adding newer servers, removing old ones and raising the farm behavior level with Invoke-AdfsFarmBehaviorLevelRaise, including WID and SQL farms."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/deployment/upgrading-to-ad-fs-in-windows-server
  - https://learn.microsoft.com/en-us/powershell/module/adfs/invoke-adfsfarmbehaviorlevelraise
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD FS farm behavior level upgrade

AD FS upgrades are rolling: join newer-OS servers to the existing farm, move roles, remove old servers, then raise
the **farm behavior level (FBL)** to unlock new features.

## FBL values
| FBL | OS |
|---|---|
| 1 | 2012 R2 |
| 3 | 2016 |
| 4 | 2019 and 2022 (check the docs for newer releases) |

Raising the FBL creates a new AD FS configuration database (AdfsConfiguration, V3, V4). A newer-OS server joined to a
lower-FBL farm runs in mixed mode at the farm's level and cannot use the new features; do not stay in mixed mode long.
```powershell
Get-AdfsFarmInformation | Select CurrentFarmBehavior,FarmNodes
```

## Procedure (WID farm)
1. Back up config (AD FS Rapid Restore Tool) and the token-signing/decryption certs if not auto-managed.
2. Add new servers: deploy the target OS, apply all updates, install the AD FS role and join the existing farm (`Add-AdfsFarmNode`).
3. Make a new server primary: on it `Set-AdfsSyncProperties -Role PrimaryComputer`, then on others
   `Set-AdfsSyncProperties -Role SecondaryComputer -PrimaryComputerName ADFS-NEW01`.
4. Move load balancer, DNS and network configuration to the new servers, verify, then uninstall the AD FS role from the old
   servers and remove stale entries with `Set-AdfsFarmInformation -RemoveNode "<old-server-FQDN>"`.
5. The AD schema must be at least level 85 for AD FS 2016+ and at least 88 for AD FS 2019+. Then, on one server:
```powershell
Test-AdfsFarmBehaviorLevelRaise
Invoke-AdfsFarmBehaviorLevelRaise
```
6. Upgrade WAP after the FBL raise: on each new WAP server run `Install-WebApplicationProxy` with the federation certificate
   thumbprint, check `Get-WebApplicationProxyConfiguration` (ConfigurationVersion), set `Set-WebApplicationProxyConfiguration -ConnectedServersName ...`
   to the new servers only, then `Set-WebApplicationProxyConfiguration -UpgradeConfigurationVersion` (skip if it already shows Windows Server 2016).

## Gotchas
- Back up the AD FS configuration and servers first; the procedure above is the documented WID-farm path.
- All remaining farm nodes must run the target OS before the raise.
- Service account: switching to gMSA is easiest during the upgrade.

## Verify
- [ ] `Get-AdfsFarmInformation` shows the new FBL; sign-in to a test RP works through WAP; old nodes gone from FarmNodes.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main (AD FS content, ms.date 2023-2024; AD FS in Windows Server 2016-2025).
Confirmed from upgrading-to-ad-fs-in-windows-server (WID farm): FBL table (1, 3, 4 with 2019 and 2022), new configuration database on raise,
mixed-mode caveat, schema levels 85 and 88, Set-AdfsSyncProperties roles, Set-AdfsFarmInformation -RemoveNode, Test- and Invoke-AdfsFarmBehaviorLevelRaise and the WAP upgrade steps.
Removed the nonexistent Remove-AdfsFarmNode, the adprep instruction, the WAP-compatibility claim, the SQL-farm paragraph and the one-way assertion, none of which the page states.
Method: documentation only; no commands were run.
