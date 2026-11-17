---
id: computing-software.systems-network-administration.virtualisation.esxi-active-directory-join-esx-admins
name: esxi-active-directory-join-esx-admins
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-active-directory, esx-admins, vsphere-security, kerberos, cve-2024-37085, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Join ESXi hosts to Active Directory securely: authentication proxy or direct join, and changing the default ESX Admins group to close the CVE-2024-37085 takeover path."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security-8-0.html
  - https://knowledge.broadcom.com/external/article?articleNumber=369707
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Joining ESXi to Active Directory and the ESX Admins group

## Should you join at all?
Most admins work through vCenter (which has its own identity sources). Join hosts to AD
only if you need named direct-host logins (break-glass, DCUI, SSH) with audit. If not,
keep hosts off AD: smaller attack surface.

## Join
Host → Configure → Authentication Services → Join Domain:
- Direct: domain + an account with rights to create computer objects in the target OU.
- **vSphere Authentication Proxy**: hosts join via the proxy service on vCenter, so no AD
  credentials in profiles (see the vSphere Security guide).
Set-VMHostAuthentication in PowerCLI automates the join; see the PowerCLI documentation
for current parameters.
Prereqs: DNS forward/reverse, time in sync with the DCs, host name matches DNS.

## The ESX Admins problem (CVE-2024-37085)
By default ESXi grants **full admin** to an AD group named `ESX Admins` without checking its
SID. Anyone who can create or rename a group to "ESX Admins" in AD gets root-equivalent on
every domain-joined host. Ransomware crews used this in 2024.
Fix on every joined host (check your version's defaults):
| Advanced setting | Set to |
|---|---|
| `Config.HostAgent.plugins.hostsvc.esxAdminsGroup` | a specific, protected group name (e.g. `SG-ESXi-Admins-Tier0`) or empty |
| `Config.HostAgent.plugins.hostsvc.esxAdminsGroupAutoAdd` | false |
Apply with `esxcli system settings advanced set` or Set-AdvancedSetting in PowerCLI.
Also restrict who can create groups in AD and alert on creation of any group named
"ESX Admins".

## Gotchas
- Lockdown mode still applies to AD users; add them to exception users only if needed.
- Leaving the domain does not delete the computer object; clean it in AD.
- Host profiles capture domain membership; update the profile when the OU changes.

## Verify
Check the host authentication status and the esxAdmins group settings on all hosts; a
test AD user in the group can log in to the host client, a user not in it cannot.

## Checked
2026-10-31: The `vpxuser` account and its Admin/full-access default, the `Config.HostAgent.plugins.hostsvc.esxAdminsGroup` and `Config.HostAgent.plugins.hostsvc.esxAdminsGroupAutoAdd` workaround (including removal of the ESX Admins admin permission on joined hosts) confirmed in KB 369707; AD join and authentication services topics confirmed in the vSphere Security guide TOC. Removed unconfirmed specifics: the PowerCLI join command flags, the `authValidateInterval` 90-minute setting and the 8.0U3 default-change claim.
Method: documentation only; no commands were run.
