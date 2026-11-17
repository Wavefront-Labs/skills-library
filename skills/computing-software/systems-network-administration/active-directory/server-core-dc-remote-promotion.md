---
id: computing-software.systems-network-administration.active-directory.server-core-dc-remote-promotion
name: server-core-dc-remote-promotion
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-ds, server-core-domain-controller, install-addsdomaincontroller, server-core, remote-promotion]
level: practitioner
status: gated
description: "Promote a Server Core domain controller remotely: add AD-Domain-Services, run Install-ADDSDomainController over remoting, and verify without a GUI."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/install-addsdomaincontroller
  - https://learn.microsoft.com/en-us/powershell/module/servermanager/install-windowsfeature
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promote a Server Core DC remotely

Server Core has no desktop, so all promotion work is done from an admin workstation over PowerShell remoting or
with the console tools.

## Prepare the core box (sconfig or PowerShell on console)
```powershell
Rename-Computer -NewName DC03 -Restart
New-NetIPAddress -InterfaceAlias Ethernet -IPAddress 10.0.10.13 -PrefixLength 24 -DefaultGateway 10.0.10.1
Set-DnsClientServerAddress -InterfaceAlias Ethernet -ServerAddresses 10.0.10.11,10.0.10.12
Add-Computer -DomainName ad.example.com -Credential (Get-Credential) -Restart   # optional
```

## Install the role remotely
```powershell
Install-WindowsFeature -ComputerName DC03 -Name AD-Domain-Services -IncludeManagementTools
```
`Install-WindowsFeature` takes `-ComputerName` and `-IncludeManagementTools`.

## Promote over remoting
```powershell
$cred = Get-Credential AD\da-admin
$dsrm = Read-Host -AsSecureString 'DSRM'          # build secure strings locally; no prompts in the remote block
Invoke-Command -ComputerName DC03 -Credential $cred -ScriptBlock {
  Install-ADDSDomainController -DomainName ad.example.com -InstallDns -SiteName HQ `
    -Credential $using:cred -SafeModeAdministratorPassword $using:dsrm `
    -DatabasePath '<DATA_VOLUME>\NTDS' -LogPath '<DATA_VOLUME>\NTDS' -SysvolPath '<DATA_VOLUME>\SYSVOL' -Force
}
```
Passing the DSRM SecureString and credential into the remote block with `$using:`
(gated: unconfirmed, source is paywalled or blocked). No readable Microsoft page documents this pattern for the ADDSDeployment cmdlets, so test it in a
lab; the alternative is to run the cmdlet in a console session on the server.
Run `Test-ADDSDomainControllerInstallation` with the same parameters first; it runs the prerequisite checks and
changes nothing. The server restarts after promotion unless `-NoRebootOnCompletion` is set; reconnect after it
comes back.

## Verify with no GUI
```powershell
Invoke-Command DC03 { Get-Service NTDS,DNS,Netlogon,KDC,DFSR | ft Name,Status }
dcdiag /s:DC03 /v /c /e /q
repadmin /showrepl DC03
Get-SmbShare -CimSession DC03 | ? Name -in 'SYSVOL','NETLOGON'
```
Manage it afterwards with RSAT (ADUC, DNS, GPMC) or Windows Admin Center pointed at DC03.

## Gotchas
- The DC needs a static IP and must have a preferred DNS server that is an existing DC before promotion (the
  cmdlets expect a preferred DNS server to be configured first).
- Pass `-Credential` to the promotion cmdlet inside the block, as above.
- Domain Admins is the credential needed to add a DC to an existing domain.

## Verify
- [ ] NTDS, Netlogon and DFSR running; SYSVOL and NETLOGON shared.
- [ ] `dcdiag` clean and replication shows inbound partners on DC03.

## Checked

Date: 2026-10-27. Documentation: Install-ADDSDomainController (Windows Server 2025 module page), the AD DS install
overview, Install-WindowsFeature module page (MicrosoftDocs repositories, main branch).
Confirmed: `-ComputerName` and `-IncludeManagementTools` on Install-WindowsFeature, the promotion parameters used,
Test- cmdlet behaviour, preferred-DNS-server expectation, Domain Admins for a replica DC.
Gated: the `$using:` SecureString pattern for remote promotion.
Removed unconfirmed claims: "recommended DC install", CredSSP not being needed, and the claim that Server Core cannot
be converted to Desktop Experience.

Method: documentation only; no commands were run.
