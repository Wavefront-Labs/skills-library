---
id: computing-software.systems-network-administration.windows-server.wac-gateway-deployment
name: wac-gateway-deployment
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-admin-center, wac, wac-gateway, wac-certificate, gateway-mode, high-availability, kerberos-delegation, rbcd, winrm]
level: practitioner
status: docs-checked
description: "Deploy Windows Admin Center in gateway mode: install on a server, a trusted TLS certificate, Kerberos RBCD for SSO to targets, HA option, and upgrade path."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/deploy/install
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/update-certificate
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/user-access-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Admin Center gateway deployment

**Goal:** one browser-based management gateway for the server estate, with SSO and a real certificate.

## Install
- Gateway on a dedicated Windows Server (not a DC), domain-joined, in the management tier.
- Download the installer from the Windows Admin Center Evaluation Center; choose Custom setup to set the port, TLS
  certificate type and thumbprint, FQDN, trusted hosts mode and WinRM over HTTPS. Express setup picks them for you.
- The installer can generate a self-signed certificate valid for 60 days (testing only). For production use a CA-issued
  Server Authentication certificate with its private key in the `LocalMachine\My` store, valid for the FQDN users type.
- Unattended (Server Core): `Start-Process .\WindowsAdminCenter.exe -ArgumentList '/VERYSILENT' -Wait`; options include
  `/Silent`, `/VerySilent`, `/HTTPSPortNumber=<port>` and `/CertificateThumbprint=<thumbprint>`. The service is named `WindowsAdminCenter`.
- Renew or replace the certificate on the running service with the Configuration module (`Set-WACCertificateSubjectName`
  or `-Thumbprint`, then `Set-WACCertificateAcl` for Network Service, then `Restart-Service WindowsAdminCenter`), or re-run
  the installer and choose the pre-installed TLS certificate.

## SSO to managed servers (avoid CredSSP)
On Windows Server, single sign-on needs Kerberos delegation that makes the gateway computer trusted to delegate to the
target. Resource-based constrained delegation per the docs:
```powershell
Set-ADComputer -Identity (Get-ADComputer node01) -PrincipalsAllowedToDelegateToAccount (Get-ADComputer wac01)
```
Run it for each target (loop over an OU for many). Remove with `-PrincipalsAllowedToDelegateToAccount $null`.
Otherwise users must supply **Manage as** credentials. WinRM does not allow credential delegation by default; where a tool
needs it, WAC uses CredSSP temporarily.

## High availability
WAC supports an active-passive failover-cluster deployment (see the high-availability skill); check the current docs for
which versions support it. Servers stay manageable by RSAT/PowerShell if the gateway is down.

## Hardening
- Restrict gateway users and administrators (see the RBAC skill); add Microsoft Entra authentication for Conditional Access and MFA;
  don't publish the gateway directly to the internet.
- Keep WAC updated; the gateway can install extensions. Treat it as a Tier 0 asset if it manages domain controllers.

## Verify
- [ ] `https://wac.ad.example.com` presents the trusted certificate.
- [ ] Connecting to a server works without a credential prompt (delegation configured).

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, Windows Admin Center pages (ms.date 2025 for access, install, certificate, HA and troubleshooting; WAC 2410+ modernized gateway).
Confirmed from deploy/install (ms.date 2025-05-28: setup modes, 60-day self-signed certificate, LocalMachine\My, /VERYSILENT, /HTTPSPortNumber, /CertificateThumbprint, Start-Service WindowsAdminCenter),
configure/update-certificate (Set-WACCertificateSubjectName, Set-WACCertificateAcl, service restart) and configure/user-access-control (RBCD example, Entra layer, CredSSP note).
Removed the msiexec parameter claim, the two-gateway load-balancer pattern, the 'not a DC' and 'management tier' assertions and the Entra application proxy publishing advice, none of which the pages state.
Method: documentation only; no commands were run.
