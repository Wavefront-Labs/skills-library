---
id: computing-software.systems-network-administration.windows-server.adcs-online-responder-ocsp
name: adcs-online-responder-ocsp
category: computing-software
field: systems-network-administration
product: windows-server
tags: [ad-cs, ocsp, online-responder, crl, pkiview]
level: advanced
status: docs-checked
description: "Deploy an AD CS Online Responder: OCSP signing template, revocation configuration, AIA OCSP URL on the CA, array members and monitoring."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/adcsdeployment/install-adcsonlineresponder
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/configure-ml-dsa-online-responder
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/configure-certificate-path-validation-revocation-policy
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD CS Online Responder (OCSP)

OCSP answers "is this certificate revoked" per certificate instead of clients downloading large CRLs. Useful for
VPN, NPS and smart card estates with big CRLs.

## Install
```powershell
Install-WindowsFeature ADCS-Online-Cert -IncludeManagementTools
Install-AdcsOnlineResponder -Force
```

## OCSP signing certificate
1. On the CA, duplicate the **OCSP Response Signing** template; Security: grant the OCSP server computer accounts
   Read and Enroll (and Autoenroll). Keep renewal automatic.
2. Publish the template on the CA (Certificate Templates > New > Certificate Template to Issue).

## Revocation configuration (Online Responder console)
Add Revocation Configuration > select the CA certificate > **Automatically select a signing certificate** with
the template and **Auto-Enroll for an OCSP signing certificate** > provider uses the CA's CRL URLs (base and delta).
For an offline root, a separate revocation configuration uses the root's CRL file location.

## Tell clients where it is
On the CA, Extensions tab > AIA > add `http://ocsp.corp.example.com/ocsp` with **Include in the online certificate
status protocol (OCSP) extension**. Only certificates issued afterwards contain it; restart the CA service.
Then restart the CA service (`Restart-Service certsvc`) if the change requires it.

## Test
```cmd
certutil -URL issued-cert.cer
certutil -verify -urlfetch issued-cert.cer
```
`certutil -URL` opens the URL retrieval tool, where you can test the OCSP location; `-verify -urlfetch` retrieves and
verifies AIA certificates and CDP CRLs.

## Gotchas
- In the Online Responder console, check that Array Configuration shows the revocation configuration status as Working.

## Verify
- [ ] Online Responder array configuration status Working; `certutil -verify -urlfetch` succeeds for a certificate carrying the OCSP URL.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed: Install-AdcsOnlineResponder and the Adcs-Online-Cert feature, the OCSP Response Signing template, Enroll and Autoenroll permissions for the responder computer account, the revocation configuration options (Automatically select a signing certificate, Auto-Enroll for an OCSP signing certificate), the AIA entry option Include in the online certificate status protocol (OCSP) extension, and the certutil -URL and -verify -urlfetch switches. Removed as unconfirmed: the 2-week signing certificate validity, the ocsp-nocheck extension claim, the load balancer advice, CRL fallback behaviour, the pkiview OCSP status claim, the expected output text, and the placeholder certutil -setreg line.

Method: documentation only; no commands were run.
