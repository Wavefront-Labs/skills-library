---
id: computing-software.systems-network-administration.windows-server.adfs-ssl-service-communication-certificate-renewal
name: adfs-ssl-service-communication-certificate-renewal
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-fs, adfs-ssl-certificate, service-communications-certificate, web-application-proxy, certificate-renewal]
level: practitioner
status: docs-checked
description: "Renew the AD FS SSL and service communication certificate across farm nodes and Web Application Proxy servers with Set-AdfsSslCertificate, without an outage."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/manage-ssl-certificates-ad-fs-wap
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/overview/ad-fs-requirements
  - https://learn.microsoft.com/en-us/powershell/module/adfs/set-adfssslcertificate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Renew the AD FS SSL / service communication certificate

The SSL certificate (federation service name, e.g. `sts.example.com`) is public-CA issued and is **not**
auto-rolled like token-signing. Expiry = every SSO app breaks.

## Get the new certificate
- Subject/SAN: `sts.example.com`, plus `enterpriseregistration.example.com` if device registration, and
  `certauth.sts.example.com` if certificate authentication on port 443 is used.
- Import the PFX into **Local Computer\Personal** on every AD FS and WAP server, with private key.

## AD FS servers (2016+)
The AD FS TLS/SSL certificate is not the same as the Service communications certificate shown in the AD FS Management
snap-in; change it with PowerShell. On Server 2016 and later, `Set-AdfsSslCertificate` runs only on the primary and
updates all nodes over PowerShell remoting (TCP 5985 must be open to the other nodes); the farm should be at the 2016
behavior level.
```powershell
$t = (Get-ChildItem Cert:\LocalMachine\My | ? Subject -like '*sts.example.com*' | Sort NotAfter -Desc)[0].Thumbprint
Set-AdfsSslCertificate -Thumbprint $t     # primary only; updates every node
```
The cmdlet grants the adfssrv principal read access to the private key, so granting the service account is not required.
Import the certificate into the local machine store on every AD FS and WAP server first.

## WAP servers
```powershell
Set-WebApplicationProxySslCertificate -Thumbprint $t     # on each WAP server
# published apps using the same cert:
Get-WebApplicationProxyApplication | ? ExternalCertificateThumbprint -eq $old | Set-WebApplicationProxyApplication -ExternalCertificateThumbprint $t
```
If the cmdlet fails because the old certificate already expired, re-run `Install-WebApplicationProxy` with the new
thumbprint, `-FederationServiceName` and `-FederationServiceTrustCredential`.

## Verify
```powershell
netsh http show sslcert | findstr /i "hash port"
```
- [ ] Browser shows the new certificate's expiry on AD FS and through WAP; test SSO to two RPs succeeds.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main and windows-powershell-docs (winserver2025-ps ADFS and WebApplicationProxy modules), entra-docs main.
Confirmed from manage-ssl-certificates-ad-fs-wap (ms.date current in the repo): TLS/SSL versus Service communications certificate, Set-AdfsSslCertificate primary-only behaviour on 2016+,
remoting port 5985, adfssrv key permission, Set-WebApplicationProxySslCertificate and the Install-WebApplicationProxy fallback; SAN names from ad-fs-requirements.
Removed the wrong instruction to run Set-AdfsSslCertificate on every node and the Set-AdfsCertificate Service-Communications line, the service restarts and the idpinitiatedsignon probe, which the page does not state.
Method: documentation only; no commands were run.
