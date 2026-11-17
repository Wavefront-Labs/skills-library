---
id: computing-software.systems-network-administration.windows-server.rds-deployment-certificates
name: rds-deployment-certificates
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, rds, rds-certificates, set-rdcertificate, rd-gateway, sso]
level: practitioner
status: docs-checked
description: "Assign RDS deployment certificates with Set-RDCertificate for RD Connection Broker SSO and publishing, RD Web Access and RD Gateway: names, renewal and session host certs."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdcertificate
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/get-rdcertificate
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remote-desktop-web-client-admin
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/certificates-and-public-key-infrastructure-pki/remote-desktop-server-certificates-renewed
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# RDS deployment certificates

Four roles in an RDS deployment use certificates; mismatches cause "publisher cannot be identified", repeated
credential prompts or gateway failures.

## Roles
| Role | Name it must cover | Used for |
|---|---|---|
| RDRedirector (Connection Broker - Enable SSO) | broker FQDN or HA client access name | SSO to session hosts |
| RDPublishing (Connection Broker - Publishing) | same | signing RDP files / RemoteApp |
| RDWebAccess | external RD Web name (e.g. `rdweb.example.com`) | HTTPS for RD Web Access |
| RDGateway | external gateway name (e.g. `rdgw.example.com`) | TLS for gateway connections |
`Set-RDCertificate -Role` accepts exactly these four values. Every certificate must be trusted by the clients.

## Apply
```powershell
$pw = Read-Host -AsSecureString
'RDRedirector','RDPublishing','RDWebAccess','RDGateway' | % {
  Set-RDCertificate -Role $_ -ImportPath '<CERTS>\rds-2026.pfx' -Password $pw -ConnectionBroker rdcb01.ad.example.com -Force
}
Get-RDCertificate -ConnectionBroker rdcb01.ad.example.com | ft Role,Level,ExpiresOn,Subject
```
`Get-RDCertificate` returns properties including Level, ExpiresOn and Subject; `Level` should be **Trusted**. `-ImportPath` and
`-Password` import a PFX; Windows Server 2019 and later also accept `-Thumbprint`.

## Session host certificates
Session hosts use their own RDP listener certificate (self-signed by default). Replace it with a CA-issued certificate
through the Group Policy setting **Server Authentication Certificate Template** (Remote Desktop Session Host > Security),
or set the registry value `SSLCertificateSHA1Hash` (REG_BINARY, the certificate's SHA1 hash) under
`HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp`.

## Renewal
Calendar the expiry. Renew, then re-run `Set-RDCertificate` for each role. For the RD web client, rerun
`Import-RDWebClientBrokerCert <.cer file path>` whenever the broker certificate is renewed, or users get an unexpected
server authentication certificate error.

## Verify
- [ ] `Get-RDCertificate` shows every role Trusted with a future expiry; launching a RemoteApp shows no name mismatch warning.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: Set-RDCertificate role values (RDGateway, RDWebAccess, RDRedirector, RDPublishing) and parameters (-ImportPath, -Password, -Thumbprint on Windows Server 2019 and later, -ConnectionBroker, -Force); Get-RDCertificate properties; the Server Authentication Certificate Template Group Policy setting; the RDP-Tcp SSLCertificateSHA1Hash registry value; Import-RDWebClientBrokerCert after broker certificate renewal. Removed as unconfirmed: the claim that the broker pushes the certificate to all servers in a role, the single SAN or wildcard recommendation, the Win32_TSGeneralSetting WMI route, and the publisher verification wording.

Method: documentation only; no commands were run.
