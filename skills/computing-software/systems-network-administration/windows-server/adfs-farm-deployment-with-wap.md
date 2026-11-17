---
id: computing-software.systems-network-administration.windows-server.adfs-farm-deployment-with-wap
name: adfs-farm-deployment-with-wap
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-fs, adfs, adfs-farm, web-application-proxy, install-adfsfarm, gmsa, federation-service, sql-farm]
level: advanced
status: docs-checked
description: "Deploy an AD FS farm with WAP: SSL certificate, gMSA, WID vs SQL, Install-AdfsFarm, adding nodes, WAP in the DMZ, load balancing and health checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/design/federation-server-farm-using-wid
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/overview/ad-fs-requirements
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/deployment/best-practices-securing-ad-fs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD FS farm deployment with Web Application Proxy

## Prerequisites
- Public SSL certificate for the federation service name (`sts.example.com`), with the
  private key, also covering `certauth.sts.example.com` if using certificate auth.
- gMSA for the service (KDS root key present): `New-ADServiceAccount adfsgmsa -DNSHostName sts.example.com -PrincipalsAllowedToRetrieveManagedPassword 'ADFS-Servers'`.
- SPN `HOST/sts.example.com` registered on the gMSA (Install-AdfsFarm does this if
  permitted).
- Database: WID (up to 30 federation servers with 100 or fewer relying party trusts; no SAML artifact resolution or token
  replay detection) or SQL Server for larger or advanced farms.
- Certificate SAN must include the federation service name; add `certauth.<service name>` for user certificate auth on 443 and
  `enterpriseregistration.<upn suffix>` for device registration. The load balancer and servers must support SNI.
- The gMSA must live in the default Managed Service Accounts container and needs a DC on Windows Server 2012 or later.

## First node
```powershell
Install-WindowsFeature ADFS-Federation -IncludeManagementTools
$cert = (Get-ChildItem Cert:\LocalMachine\My | ? Subject -like '*sts.example.com*').Thumbprint
Install-AdfsFarm -CertificateThumbprint $cert -FederationServiceName sts.example.com `
  -FederationServiceDisplayName 'Example Sign-in' -GroupServiceAccountIdentifier 'CORP\adfsgmsa$'
```
Additional nodes: `Add-AdfsFarmNode -CertificateThumbprint $cert -PrimaryComputerName adfs01 -GroupServiceAccountIdentifier 'CORP\adfsgmsa$'`.

## WAP (DMZ, not domain joined)
```powershell
Install-WindowsFeature Web-Application-Proxy -IncludeManagementTools
Install-WebApplicationProxy -CertificateThumbprint $cert -FederationServiceName sts.example.com -FederationServiceTrustCredential (Get-Credential)
```
WAP resolves `sts.example.com` to the internal AD FS VIP (hosts file or split DNS).
Ports: Internet > WAP 443 (and TCP 49443 only if user certificate auth is not on 443); WAP > AD FS 443. AD FS servers
sync configuration over HTTP 80 from the primary, so allow 80 between farm nodes and WAP.

## Load balancing
- Internal LB to AD FS nodes, external LB to WAPs, TCP 443, HTTP health probe
  `http://<node>/adfs/probe` (port 80, returns 200 OK served locally).
- Use an SNI-capable LB; without SNI support, use the 0.0.0.0 fallback binding on the server.

## Security
Enable extranet smart lockout (`Set-AdfsProperties -ExtranetLockoutMode AdfsSmartLockoutEnforce`), audit levels, and keep AD FS servers Tier 0.

## Verify
- [ ] A test sign-in works internally and externally through WAP.
- [ ] `Get-AdfsFarmInformation` lists all nodes; `Get-WebApplicationProxyConfiguration` lists the connected WAP servers.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main (AD FS content, ms.date 2023-2024; AD FS in Windows Server 2016-2025).
Confirmed from Federation-Server-Farm-Using-WID, ad-fs-requirements (certificate SAN, gMSA, SPN, SNI, probe URLs) and Best-Practices-Securing-AD-FS (ports 443, 49443, 80):
WID limits and unsupported features, certauth SAN, probe endpoint and its 200 OK behaviour, port roles. Replaced the idpinitiatedsignon test page step (not covered by these pages) with a generic sign-in test, dropped the Get-WebApplicationProxyHealth check in favour of Get-WebApplicationProxyConfiguration, and the 'no SSL termination' wording (docs only require SNI support).
Method: documentation only; no commands were run.
