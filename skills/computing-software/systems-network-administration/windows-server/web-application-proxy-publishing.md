---
id: computing-software.systems-network-administration.windows-server.web-application-proxy-publishing
name: web-application-proxy-publishing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-access, web-application-proxy, wap, adfs-proxy, add-webapplicationproxyapplication, preauthentication, pass-through, kerberos-constrained-delegation, entra-application-proxy]
level: practitioner
status: docs-checked
description: "Publish internal web apps through Web Application Proxy: ADFS proxy role, pass-through vs ADFS pre-auth, KCD for Windows-auth apps, certificates, and modern alternatives."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/web-application-proxy/web-app-proxy-windows-server
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/web-application-proxy/publishing-applications-using-ad-fs-preauthentication
  - https://learn.microsoft.com/en-us/powershell/module/webapplicationproxy/add-webapplicationproxyapplication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Application Proxy (WAP) publishing

**What:** a reverse proxy role in the DMZ that (1) proxies AD FS to the internet and (2)
publishes internal web apps with optional AD FS pre-authentication. Not domain-joined
unless KCD is needed.

## Install and join to AD FS
```powershell
Install-WindowsFeature Web-Application-Proxy -IncludeManagementTools
Install-WebApplicationProxy -FederationServiceName 'sts.example.com' `
  -FederationServiceTrustCredential (Get-Credential AD\adfs-admin) -CertificateThumbprint '<THUMBPRINT>'
```
The certificate (public CA) must cover `sts.example.com` and published app names (SAN/wildcard).
Hosts file or DMZ DNS must resolve the AD FS service name to the internal AD FS farm/LB.

## Publish an app
```powershell
# pass-through (app does its own auth)
Add-WebApplicationProxyApplication -Name 'Intranet' -ExternalUrl 'https://intranet.example.com/' `
  -BackendServerUrl 'https://intranet.ad.example.com/' -ExternalCertificateThumbprint '<THUMBPRINT>' `
  -ExternalPreauthentication PassThrough
# AD FS pre-auth + Kerberos to an IIS app with Windows auth (WAP must be domain-joined, KCD configured)
Add-WebApplicationProxyApplication -Name 'HR' -ExternalUrl 'https://hr.example.com/' `
  -BackendServerUrl 'https://hr.ad.example.com/' -ExternalCertificateThumbprint '<THUMBPRINT>' `
  -ExternalPreauthentication ADFS -ADFSRelyingPartyName 'HR WAP' -BackendServerAuthenticationSPN 'HTTP/hr.ad.example.com'
```
KCD: the WAP server must be domain-joined, and delegation must be configured so the WAP computer account can delegate
to the backend service's SPN (`HTTP/hr.ad.example.com`).

## Position today
The Windows Server docs for the on-premises Web Application Proxy point to **Microsoft Entra application proxy**
for secure access to on-premises apps over the cloud. Use WAP mainly where AD FS remains.

## Verify
- [ ] `Get-WebApplicationProxyHealth` shows no errors; `Get-WebApplicationProxyApplication` lists apps.
- [ ] External test: pre-auth redirect to AD FS, then the app loads with SSO.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main and windows-powershell-docs (winserver2025-ps ADFS and WebApplicationProxy modules), entra-docs main.
Confirmed from Publishing-Applications-using-AD-FS-Preauthentication, web-app-proxy-windows-server (ms.date 2026-04-16) and the Add-WebApplicationProxyApplication reference:
-ExternalPreauthentication values (ADFS, PassThrough, ClientCertificate, ADFSforRichClients, ADFSforOAuth), -ADFSRelyingPartyName, -BackendServerAuthenticationSPN, -ExternalCertificateThumbprint,
domain join requirement for Kerberos constrained delegation, wildcard publishing, HTTP-to-HTTPS redirect option, and the pointer to Entra application proxy.
Removed the delegation-dialog wording and the Conditional Access/MFA feature claims, which the Windows Server pages do not state.
Method: documentation only; no commands were run.
