---
id: computing-software.systems-network-administration.windows-server.azure-vm-activation-azure-kms
name: azure-vm-activation-azure-kms
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-activation, azure-kms, kms, activation-errors, azure-virtual-network]
level: practitioner
status: docs-checked
description: "Fix Windows activation on Azure VMs: Azure KMS endpoints azkms.core.windows.net and kms.core.windows.net, forced tunnelling routes and the right setup key."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/troubleshoot-activation-problems
  - https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/custom-routes-enable-kms-activation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Activation of Azure VMs against Azure KMS

Marketplace Windows images activate against Microsoft's Azure KMS automatically. Failures almost always come from
network routing or a changed product key.

## Check
```cmd
slmgr /dlv
```
In Azure public cloud regions the KMS endpoint is `azkms.core.windows.net:1688`. Other clouds: China
`kms.core.chinacloudapi.cn:1688` or `azkms.core.chinacloudapi.cn:1688`; Germany `kms.core.cloudapi.de:1688`;
US Government `kms.core.usgovcloudapi.net:1688`. Use the endpoint for the VM's cloud.

## Fix steps
1. Set the KMS host explicitly:
```cmd
slmgr /skms azkms.core.windows.net:1688
slmgr /ato
```
2. Test connectivity:
```powershell
Test-NetConnection azkms.core.windows.net -Port 1688
```
3. **Forced tunnelling** (all Internet-bound traffic sent on-premises) breaks it, because the activation request
   must come from an Azure public IP address. Add a custom route with next hop Internet for the KMS IPs. Azure
   Global: `azkms.core.windows.net` is 20.118.99.224 and 40.83.235.53 (add both); `kms.core.windows.net` now
   resolves to 20.118.99.224 (since 2023-03-01 the old 23.102.135.246 is unused). Other clouds have different
   IPs; take them from the forced-tunnelling article.
4. Wrong key (MAK/retail entered by someone, or a custom image from on-premises): install the GVLK for the edition
   (`slmgr /ipk <GVLK>` from Microsoft's KMS client keys list), then `/ato`.

## Errors
| Error | Meaning |
|---|---|
| 0xC004F074 | No KMS could be contacted (routing/firewall/DNS) |
| 0xC004F06C | request timestamp invalid; client clock too different from the KMS host |
| 0xC004FD01 | Windows is not running on a supported Hyper-V virtualization platform |
| 0xC004FD02 | Windows is not activated on the host machine |

## Gotchas
- Microsoft also publishes a separate troubleshooting-tools article for Azure VM Windows activation; use it for
  cases not covered here.

## Verify
- [ ] `slmgr /dli` shows Licensed.

## Checked

2026-10-27. Documentation release: Microsoft Learn Azure VM activation troubleshooting and forced-tunneling articles (current). Confirmed regional KMS endpoints, the two Azure Global IPs, the kms.core.windows.net change on 2023-03-01, why forced tunnelling fails, and error codes 0xC004F074, 0xC004F06C, 0xC004FD01 and 0xC004FD02. Removed 0xC004F035, the Azure Hybrid Benefit licence-type note, the 168.63.129.16 DNS note and the channel string as unconfirmed.

Method: documentation only; no commands were run.
