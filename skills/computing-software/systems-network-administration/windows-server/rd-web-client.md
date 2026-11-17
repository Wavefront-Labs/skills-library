---
id: computing-software.systems-network-administration.windows-server.rd-web-client
name: rd-web-client
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, rds, rd-web-client, html5, rd-web-access, remote-desktop-services]
level: practitioner
status: docs-checked
description: "Publish the HTML5 Remote Desktop web client on RD Web Access: install the RDWebClientManagement module, import the broker certificate and publish the client."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-web-client-admin
  - https://learn.microsoft.com/en-us/azure/virtual-desktop/users/connect-web
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RD Web client (HTML5)

Users open RemoteApps and desktops in a browser with no client install. Runs on the RD Web Access server alongside
the classic RDWeb page.

## Requirements
- Check Microsoft's web client admin page for supported server versions, certificate and licensing requirements.
- The RD Broker certificate (.cer) is copied to the RD Web server and imported with `Import-RDWebClientBrokerCert`.

## Install on the RD Web server
```powershell
Install-Module -Name RDWebClientManagement
Install-RDWebClientPackage
Import-RDWebClientBrokerCert '<CERTS>\rdcb-publishing.cer'
Publish-RDWebClientPackage -Type Production -Latest
```
Users browse to `https://rdweb.example.com/RDWeb/webclient/`. `Publish-RDWebClientPackage -Type Test -Latest` publishes
a test copy on the corresponding test URL first.

## Update
```powershell
Install-RDWebClientPackage
Publish-RDWebClientPackage -Type Production -Latest
```
If the old package came from an older RDWebClientManagement module version, Learn says to uninstall it first; follow
its update steps.

## Configuration
`Set-RDWebClientDeploymentSetting` for deployment options, for example
`Set-RDWebClientDeploymentSetting -Name "SuppressTelemetry" $true`; see the admin page for the other documented names.

## Gotchas
- Rerun `Import-RDWebClientBrokerCert` whenever the RD Broker certificate is updated or renewed (Learn).
- Use certificates the browser trusts on the gateway and web server.

## Verify
- [ ] Test user signs in at `/RDWeb/webclient/`, launches a RemoteApp and copies/pastes text.

## Checked
2026-10-28. Confirmed on the Learn RD web client admin page: RDWebClientManagement module, Install-RDWebClientPackage,
Import-RDWebClientBrokerCert (rerun on broker cert renewal), Publish-RDWebClientPackage Production/Test with -Latest,
Set-RDWebClientDeploymentSetting and SuppressTelemetry. Removed as unconfirmed: OS version requirements, CAL advice,
PowerShellGet step, Update/Get/Uninstall cmdlets, other setting names, specific certificate failure messages.
Method: documentation only; no commands were run.
