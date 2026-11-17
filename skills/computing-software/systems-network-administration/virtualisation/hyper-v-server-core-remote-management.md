---
id: computing-software.systems-network-administration.virtualisation.hyper-v-server-core-remote-management
name: hyper-v-server-core-remote-management
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v-remote-management, hyper-v, server-core, winrm, powershell-remoting]
level: practitioner
status: docs-checked
description: "Manage Server Core Hyper-V hosts remotely with Hyper-V Manager and PowerShell: remote management, workgroup TrustedHosts and CredSSP, Kerberos delegation for second hops."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/remotely-manage-hyper-v-hosts
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/set-up-hosts-for-live-migration-without-failover-clustering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote management of Server Core Hyper-V hosts

**Goal:** administer GUI-less hosts from a management workstation, including tasks that need a second hop.

## Client tools
- Windows Server: Server Manager > Manage > Add roles and features > Features > Remote Server Administration Tools >
  Role Administration Tools > Hyper-V Management Tools.
- Windows: Hyper-V Manager is available on any Windows operating system that includes Hyper-V; a tools-only
  installation works on machines that cannot host Hyper-V.
- Windows Admin Center gives a browser view (see the WAC virtual machines skill).

## Enable remote management
On the host and on the managing computer (Server Manager > Local Server > Remote management > Allow remote
connections, or from an elevated PowerShell prompt):
```powershell
Enable-PSRemoting
```
Your account must belong to the Administrators or Hyper-V Administrators group on the host.

## Domain-joined hosts
Hyper-V Manager > *Connect to Server* > *Another computer* with the host name, NetBIOS name or FQDN. PowerShell:
`Get-VM -ComputerName hv01`, `Invoke-Command -ComputerName hv01 { Get-VMSwitch }`. *Connect as another user* >
*Set User* works when your own account lacks rights on the host. An IP address can be entered in the same box.

## Hosts outside the domain or with no domain
```powershell
# On the host (elevated): firewall rules for private network zones, then CredSSP and WinRM for public zones
Enable-PSRemoting
Enable-WSManCredSSP -Role server
# On the managing computer (elevated)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "fqdn-of-hyper-v-host"
Enable-WSManCredSSP -Role client -DelegateComputer "fqdn-of-hyper-v-host"
```
You might also need the group policy *Computer Configuration > Administrative Templates > System > Credentials
Delegation > Allow delegating fresh credentials with NTLM-only server authentication*, enabled with
`wsman/fqdn-of-hyper-v-host` added. Then use *Connect to Server* in Hyper-V Manager.

## Second hop (ISO on a share, live migration started remotely)
- **Kerberos constrained delegation** avoids signing in to the server: on the computer objects allow delegation of
  `cifs` (storage) and `Microsoft Virtual System Migration Service` (VM moves), configured by a Domain Admin.
- **CredSSP** avoids delegation setup but requires you to be signed in to the source server.
- Simplest: run the command on the host (`Invoke-Command`) so there is only one hop.

## Gotchas
- Hyper-V Manager shows nothing for a host until you add it with *Connect to Server*, including the local computer.
- If you cannot connect to a local host, check that the Virtual Machine Management service exists: only the tools
  may be installed.

## Verify
Hyper-V Manager lists the VMs; mounting an ISO from a file share works without access-denied errors.

## Checked

Date checked: 2026-10-27. Documentation: "Remotely manage Hyper-V hosts with Hyper-V Manager" and "Set up hosts for live migration without Failover Clustering" (windowsserverdocs main branch), "Install Hyper-V" Server Core note.
Confirmed: Enable-PSRemoting, Enable-WSManCredSSP roles, TrustedHosts and the credential delegation policy; connect-as-another-user; Server Manager route to the tools; group membership requirement; Kerberos and CredSSP behaviour with the delegated services.

Method: documentation only; no commands were run.
