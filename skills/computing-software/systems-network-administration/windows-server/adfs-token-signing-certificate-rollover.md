---
id: computing-software.systems-network-administration.windows-server.adfs-token-signing-certificate-rollover
name: adfs-token-signing-certificate-rollover
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-fs, adfs, token-signing-certificate, autocertificaterollover, token-decrypting, certificate-rollover, federation-metadata]
level: advanced
status: docs-checked
description: "Manage AD FS token-signing and decrypting certificate rollover: AutoCertificateRollover timeline, notifying relying parties, manual rollover and Entra federation updates."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/configure-ts-td-certs-ad-fs
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-fed-o365-certs
  - https://learn.microsoft.com/en-us/powershell/module/adfs/update-adfscertificate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD FS token-signing certificate rollover

## Defaults
With `AutoCertificateRollover` true, AD FS renews its self-signed token-signing
and token-decrypting certificates automatically (about one year validity unless `CertificateDuration` is changed). A new cert is generated
`CertificateGenerationThreshold` days before the old one's Not After date and promoted to primary
`CertificatePromotionThreshold` days after generation. Read both values with `Get-AdfsProperties`.
```powershell
Get-AdfsProperties | Select AutoCertificateRollover,CertificateGenerationThreshold,CertificatePromotionThreshold,CertificateDuration
Get-AdfsCertificate -CertificateType Token-Signing | Select Thumbprint,IsPrimary,NotAfter
```

## Relying parties
- Partners that read federation metadata (`/FederationMetadata/2007-06/FederationMetadata.xml`)
  pick up the new cert automatically; those with manually uploaded certs break at
  promotion. Find and notify them before the generation date.
- Entra ID (Microsoft 365) federated domains: Entra monitors the federation metadata and starts updating 35 days before the
  certificate expires; if it cannot reach the metadata, run
  `Update-MgDomainFederationConfiguration -DomainId <domain> -InternalDomainFederationId <id>` after each change.

## Manual rollover (planned window)
```powershell
Update-AdfsCertificate -CertificateType Token-Signing -Urgent   # immediate rollover, removes older certs (may cause an outage)
# controlled: generate a secondary, let partners consume it, then promote
Update-AdfsCertificate -CertificateType Token-Signing           # primary node; creates a secondary certificate
Set-AdfsProperties -AutoCertificateRollover $false              # needed when you manage certificates yourself
Add-AdfsCertificate -CertificateType Token-Signing -Thumbprint <thumb>   # CA-issued certificate
Set-AdfsCertificate -CertificateType Token-Signing -Thumbprint <thumb> -IsPrimary
```
The new certificate needs a private key that the AD FS service account can read on every federation server (Manage Private Keys).

## Gotchas
- `Set-AdfsProperties -CertificateDuration <days>` sets how long certificates the Federation Service generates stay valid;
  it affects certificates generated afterwards.
- The TLS/SSL certificate is separate: renew with `Set-AdfsSslCertificate` (primary) and `Set-WebApplicationProxySslCertificate` on WAPs.

## Verify
- [ ] Secondary cert present before promotion; RP owners confirmed metadata or cert update.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main and windows-powershell-docs (winserver2025-ps ADFS and WebApplicationProxy modules), entra-docs main.
Confirmed from configure-TS-TD-certs-ad-fs, the Update-/Add-/Set-AdfsCertificate and Set-AdfsProperties reference pages, and entra-docs how-to-connect-fed-o365-certs:
rollover semantics, the two thresholds, Update-AdfsCertificate -Urgent behaviour, -IsPrimary promotion, CertificateDuration meaning, private-key read permission, the 35-day Entra monitoring window and Update-MgDomainFederationConfiguration.
Removed the stated default threshold values (20 and 5 days) and the 1095-day example, which the pages do not give.
Method: documentation only; no commands were run.
