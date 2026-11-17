---
id: computing-software.systems-network-administration.active-directory.trust-selective-authentication
name: trust-selective-authentication
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-trusts, selective-authentication, allowed-to-authenticate, forest-trust, event-4625, access-control, acquisitions, least-privilege]
level: practitioner
status: gated
description: "Lock a trust down with selective authentication: enable it, grant Allowed to Authenticate on specific computer objects, and debug the resulting access denials."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-trust
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Selective authentication on trusts

**Goal:** users from the trusted forest can authenticate **only** to the servers you name,
instead of to every computer in your forest.

## Enable on the trusting (resource) side
```powershell
netdom trust ad.example.com /domain:fabrikam.example /selectiveauth:yes
netdom trust ad.example.com /domain:fabrikam.example /selectiveauth    # no value displays the current state
```
`/selectiveauth` is valid only on outbound forest and external trusts. The Domains and Trusts GUI path is not covered by a readable page (gated: unconfirmed, source is paywalled or blocked).

## Grant per computer
On each resource server's **computer object** grant the *Allowed to Authenticate* extended right to a group from the trusted forest (gated: unconfirmed, source is paywalled or blocked) (a local domain group containing them also works (gated: unconfirmed, source is paywalled or blocked)). Example script (right GUID per the AD schema; confirm in the Extended Rights reference) (gated: unconfirmed, source is paywalled or blocked):
```powershell
$comp = Get-ADComputer FS01
$sid  = (Get-ADGroup GG-Project-X -Server fabrikam.example).SID
$guid = [guid]'68b1d179-0d15-4d4f-ab71-46152e79a7bc'
$acl  = Get-Acl "AD:$($comp.DistinguishedName)"
$ace  = New-Object System.DirectoryServices.ActiveDirectoryAccessRule($sid,'ExtendedRight','Allow',$guid)
$acl.AddAccessRule($ace); Set-Acl "AD:$($comp.DistinguishedName)" $acl
```
Also grant it on any server touched in the chain (DFS namespace servers for a DFS path, the
web server and SQL server for a web app).

Normal share/NTFS permissions are still required on top.

## Debug denials
Event **4625** with status 0xC0000413 reports "The machine you are logging onto is protected by an authentication firewall. The specified account is not allowed to authenticate to the machine", which means the account lacks Allowed to Authenticate on that computer.

## Verify
- [ ] Test user from the other forest reaches FS01 share; is denied on FS02.
- [ ] `netdom trust ... /selectiveauth` reports selective authentication enabled.

## Checked
Checked 2026-10-27 against Microsoft Learn (netdom trust reference; event 4625 reference).
- Confirmed: `netdom trust /selectiveauth:yes|no` (valid only on outbound forest and external trusts; no value shows state); event 4625 status 0xC0000413 text.
- Wrong in the earlier text: there is no Set-ADTrust cmdlet in the ActiveDirectory module; netdom is used instead. Get-ADTrust property names were removed because the readable page does not list them.
- Gated: the Allowed to Authenticate permission procedure, its GUID, the GUI path and the chain-of-servers rule. Reason: the selective authentication pages are previous-versions only and could not be read.

Method: documentation only; no commands were run.
