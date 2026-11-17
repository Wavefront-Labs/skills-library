---
id: computing-software.cybersecurity-defensive.endpoint-security.catalog-signing
name: catalog-signing
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [catalog-signing, catalog-files, wdac-catalog, internal-app-signing, package-inspector, code-signing, application-control]
level: advanced
status: draft
description: "Allow unsigned internal apps under App Control with catalog files: Package Inspector capture, signing catalogs with an internal certificate, deployment, and policy signer rules."
sources: ["https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/deployment/deploy-catalog-files-to-support-appcontrol", "https://learn.microsoft.com/en-us/windows/win32/seccrypto/makecat", "https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalog signing for internal apps

Many internal/LOB apps are unsigned. Rather than hash rules for every file, create a **catalog file**
(`.cat`) listing the hashes of the app's files, sign the catalog with an internal code-signing
certificate, deploy it, and allow that signer in the App Control policy.

## Steps
1. On a clean reference machine, start Package Inspector watching the drive:
   `PackageInspector.exe Start C:`
2. Install and run the application through all its normal functions (so all binaries and DLLs are touched).
3. Stop and generate the catalog:
   `PackageInspector.exe Stop C: -Name .\LOBApp.cat -cdfpath .\LOBApp.cdf`
4. Sign it:
   `signtool sign /n "Contoso Catalog Signing" /fd sha256 /tr http://timestamp.digicert.com /td sha256 /v .\LOBApp.cat`
5. Deploy the `.cat` to `%SystemRoot%\System32\catroot\{F750E6C3-38EE-11D1-85E5-00C04FC295EE}` on clients (Intune Win32 app, ConfigMgr, GPO file copy).
6. Add a signer rule for the catalog signing certificate to the App Control policy (`Add-SignerRule -FilePath policy.xml -CertificatePath catsign.cer -User`).

## Operations
- New app version = new catalog (hashes change).
- Keep the catalog-signing key protected (HSM or at least restricted, separate from general code signing); anyone with it can authorise any binary.
- Verify a file is covered: `signtool verify /kp /c LOBApp.cat <file>` or `Get-AuthenticodeSignature` shows catalog signed after deployment.

## Gotchas
- Missing files exercised only by rare features cause later blocks; check audit events after deployment.
- Package Inspector captures everything changed on the drive during the session - use a clean VM to avoid adding unrelated binaries.
- Alternative: sign the binaries themselves when you control the build (better).

## Verify
- [ ] App runs on an enforced device with no CodeIntegrity 3077 events.
- [ ] Catalog signer restricted to the catalog-signing certificate only (not the whole internal CA).
