---
id: computing-software.systems-network-administration.windows-server.adfs-troubleshooting
name: adfs-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [ad-fs, adfs-troubleshooting, adfs-farm, token-signing-certificate, event-logs]
level: practitioner
status: docs-checked
description: "Troubleshoot AD FS: admin and debug event logs, IdpInitiatedSignOn test page, correlating activity IDs, certificate and trust errors, and WAP proxy trust."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/troubleshooting/ad-fs-tshoot-overview
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/troubleshooting/ad-fs-tshoot-logging
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/troubleshooting/ad-fs-tshoot-wap-trust
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/troubleshooting/ad-fs-tshoot-initiatedsignon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD FS troubleshooting

## Logs
- Event Viewer > Applications and Services Logs > **AD FS > Admin** on every farm node.
- **AD FS Tracing > Debug** (View > Show Analytic and Debug Logs, then enable) for deep traces; disable afterwards.
- Security log with auditing: `auditpol /set /subcategory:"Application Generated" /success:enable /failure:enable`
  and `Set-AdfsProperties -AuditLevel Verbose` raise the audit detail (default Basic: five or fewer events per request).
  Event types: 1200/1201 application token success/failure, 1202/1203 fresh credential validation success/failure,
  1204/1205 password change, 1206/1207 sign out.

## Correlate
The error page shows an **Activity ID**; search all nodes' Admin logs for it:
```powershell
Get-WinEvent -LogName 'AD FS/Admin' | Where-Object Message -match '<activity-id>'
```

## Test sign-in without an app
Enable the IdP-initiated page (off by default in AD FS 2016+):
```powershell
Set-AdfsProperties -EnableIdPInitiatedSignonPage $true
```
Browse `https://sts.example.com/adfs/ls/idpinitiatedsignon.aspx`. If that works and an app fails, the problem is the
relying party trust (identifiers, claim rules, signing/encryption certificates).

## Common errors
| Symptom | Where to look |
|---|---|
| App fails but the test page works | relying party trust: identifiers, claim rules, signing/encryption certificates |
| Partners reject tokens after a rollover | token-signing certificate promoted before partners consumed it (see the rollover skill) |
| WAP cannot reach AD FS / proxy trust broken | TLS/SSL certificate and trusted root store on AD FS and WAP; as a last resort reset the trust with `Install-WebApplicationProxy` |

## Health checks
```powershell
Get-AdfsCertificate | Select CertificateType,Thumbprint,NotAfter
Get-AdfsCertificate -CertificateType Service-Communications | Select Thumbprint   # compare with the bound TLS/SSL certificate
```

## Verify
- [ ] Test page sign-in succeeds; no new errors for the app in the Admin log after fixing.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main and windows-powershell-docs (winserver2025-ps ADFS and WebApplicationProxy modules), entra-docs main.
Confirmed from ad-fs-tshoot-logging (Admin log path, Debug trace steps, audit levels, events 1200-1207, the auditpol Application Generated command), ad-fs-tshoot-initiatedsignon
(EnableIdpInitiatedSignonPage off by default) and ad-fs-tshoot-wap-trust (certificate checks, Install-WebApplicationProxy to reset trust).
Removed event 411, the specific event numbers 364, 248, 249, 394 and 422, the MSIS error mappings, the 503 and clock-skew rows and Test-AdfsServerHealth, which none of the pages confirm.
Method: documentation only; no commands were run.
