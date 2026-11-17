---
id: computing-software.systems-network-administration.active-directory.entra-id-login-for-windows-server-vms
name: entra-id-login-for-windows-server-vms
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, domain-join, entra-id-join, aadloginforwindows, virtual-machine-administrator-login, virtual-machine-user-login, azure-rbac, rdp, conditional-access, dsregcmd]
level: practitioner
status: docs-checked
description: "Sign in to Windows Server Azure VMs with Entra ID: AADLoginForWindows extension, VM login RBAC roles, RDP from Entra-joined clients, and dsregcmd checks."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-windows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra ID sign-in for Windows Server VMs

**Goal:** Entra-join an Azure VM (no AD DS) and control who can sign in with Azure RBAC and Conditional Access.

## Enable
At creation use the Management tab option to log in with Microsoft Entra ID; it enables a system-assigned managed identity
and installs the **AADLoginForWindows** extension (publisher `Microsoft.Azure.ActiveDirectory`). On an existing VM the
managed identity must be enabled before the extension is installed (managed identities do not support cross-directory
scenarios). The VM becomes Entra joined and cannot also be joined to on-premises AD or Microsoft Entra Domain Services;
uninstall the extension to disconnect it.

Supported Windows Server: 2022 and 2025 (and later) with Desktop Experience; the extension is intended for Windows Server
2022 or Windows 10 1809 and later. Passwordless sign-in (and Windows Hello for Business with certificate trust)
needs Windows Server 2022 with the October 2022 cumulative update (KB5018421) or later, or Windows Server 2025.

## Grant access (Azure RBAC on the VM, resource group or subscription)
- **Virtual Machine Administrator Login**: sign in with administrator privileges.
- **Virtual Machine User Login**: sign in with regular user privileges.
Owner or Contributor alone does not grant sign-in. Adding a user to the local Administrators group by hand (for example
`net localgroup administrators /add "AzureAD\<UPN>"`) is not supported: use the Azure roles.

## Connect
- From a Windows 10 or later PC that is Entra registered (20H1 or later), Entra joined or hybrid joined to the same tenant.
  Registered PCs must enter credentials as `AzureAD\<UPN>`.
- Remote Desktop Connection > Advanced > **Use a web account to sign in to the remote computer** (the `enablerdsaadauth` RDP
  property); with that option the local PC need not be domain or Entra joined.
- Azure Bastion with Entra authentication via the Azure CLI native RDP client.
- Conditional Access: select the **Microsoft Azure Windows Virtual Machine Sign-in** app. To require MFA, the client must
  supply an MFA claim; with web sign-in use a Windows Hello for Business PIN or biometrics. Policies restricting sign-in by
  device configuration are not supported from a Windows Server client.

## Troubleshoot
```cmd
dsregcmd /status      (AzureAdJoined : YES; AzureAdPrt : YES for SSO)
```
- Extension logs: `%SystemDrive%\WindowsAzure\Logs\Plugins\Microsoft.Azure.ActiveDirectory.AADLoginForWindows\<version>\CommandExecution.log`.
- Sign-in events: Event Viewer > Applications and Services Logs > Microsoft > Windows > AAD > Operational.
- "Your account is configured to prevent you from using this device": the RBAC role is missing.
- The VM needs outbound access to `login.microsoftonline.com`, `enterpriseregistration.windows.net`,
  `device.login.microsoftonline.com` and `pas.windows.net` (a 404 from some of these is expected).

## Verify
- [ ] `dsregcmd /status` shows `AzureAdJoined : YES`.
- [ ] A user with only VM User Login cannot elevate; an admin-role user can.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): "Sign in to a Windows virtual machine in Azure by using Microsoft
Entra ID". Confirmed extension and publisher names, role names, the Owner or Contributor note, the RDP property, the
Conditional Access app name, log locations and endpoints. Corrected supported OS (Windows Server 2022 and 2025, not
2019), the claim that only Entra-joined clients can connect (registered PCs are also allowed), and the Bastion wording.
Removed the `az` CLI commands, which the page does not give as written.
Method: documentation only; no commands were run.
