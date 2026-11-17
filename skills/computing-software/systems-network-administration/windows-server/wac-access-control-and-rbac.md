---
id: computing-software.systems-network-administration.windows-server.wac-access-control-and-rbac
name: wac-access-control-and-rbac
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-admin-center, wac, wac-rbac, wac-access-control, gateway-users, gateway-administrators, jea, smart-card-authentication, entra-id-authentication]
level: practitioner
status: docs-checked
description: "Control who uses Windows Admin Center: gateway users vs administrators, Entra ID or smart-card auth on the gateway, and JEA-based role-based access on target servers."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/user-access-control
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/plan/user-access-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Admin Center access control and RBAC

Two layers: **who can reach the gateway**, and **what they can do on each target**.

## Gateway layer
Settings > Access (gateway mode):
- **Gateway users**: may connect through the gateway (security group, e.g. `GG-WAC-Users`).
- **Gateway administrators**: may change gateway settings and install extensions (small group).
- Local administrators on the gateway machine are always gateway administrators and cannot be removed. With no group in
  the Users list, anyone who reaches the gateway URL has user access; adding groups restricts it.
- Identity provider: **Active Directory** or local groups (default) with an optional required **smart card** group
  (users must be in a security group AND a smartcard group), or **Microsoft Entra ID** as an **additional** layer
  (register the gateway with Azure; set **User assignment required** on the Entra app; Conditional Access and MFA apply).
  The user's Windows account must still have access to the gateway server.
- Group-based access is not supported in workgroups or across non-trusted domains.
- Gateway access does not grant access to targets: the user needs administrative credentials on the target (passed-through or **Manage as**).

## Target layer: role-based access control
By default users need local admin on targets. WAC RBAC deploys a **Just Enough Administration endpoint** on each
target with three roles (not supported for cluster management; CredSSP-dependent features fail):
- **Windows Admin Center Administrators**: full.
- **Windows Admin Center Hyper-V Administrators**: VMs and virtual switches.
- **Windows Admin Center Readers**: view only.
Enable per server: connect with a local administrator account, Overview > Settings > Role-based access control > Apply
(can take up to 10 minutes and restarts WinRM; status changes to Applied). This installs `Microsoft.Sme.*` PowerShell
modules, creates the three local groups above, and configures a JEA endpoint named **Microsoft.Sme.PowerShell** that runs as a
temporary local administrator. Then add users or groups to those local groups (Local Users and Groups tool, or Restricted Groups
via GPO for scale).

Deploy at scale: download the configuration package from the gateway (`POST` to
`<gateway>/api/nodes/all/features/jea/endpoint/export` with `Invoke-RestMethod -UseDefaultCredentials -OutFile`), then edit
`InstallJeaFeatures.ps1` to use domain groups if wanted and push it with DSC or remoting. Each role needs a unique group.

## Gotchas
- Local administrators on the target already have full rights; RBAC limits only users who are not local administrators.

## Verify
- [ ] A member of `GG-WAC-Readers` (mapped to the readers group) can open a server but cannot stop services.
- [ ] Non-members are refused at the gateway sign-in.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, Windows Admin Center pages (ms.date 2025 for access, install, certificate, HA and troubleshooting; WAC 2410+ modernized gateway).
Confirmed from configure/user-access-control (ms.date 2025-06-26): gateway user and administrator roles, empty-list behaviour, smartcard group rule, Entra additional layer and User assignment required,
RBAC three roles and groups, Microsoft.Sme.PowerShell endpoint name, up-to-10-minute apply with WinRM restart, cluster-management limitation, the export REST call and InstallJeaFeatures.ps1 steps.
Removed the claims about reader-role tool availability and JEA updates on upgrade, which the page does not state, and the lower-case endpoint name.
Method: documentation only; no commands were run.
