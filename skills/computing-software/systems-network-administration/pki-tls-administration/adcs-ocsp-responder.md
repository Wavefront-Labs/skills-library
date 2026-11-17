---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-ocsp-responder
name: adcs-ocsp-responder
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-ocsp-responder, pki-adcs-revocation, adcs, online-responder, ocsp, revocation-configuration, pki-tls-administration]
level: practitioner
status: draft
description: "Install the Online Responder role, issue the OCSP Response Signing template, create revocation configurations and add the OCSP URL to AIA."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/active-directory-certificate-services-overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AD CS Online Responder
Goal: lightweight OCSP for Windows and non-Windows clients.
1. `Install-WindowsFeature ADCS-Online-Cert` then `Install-AdcsOnlineResponder`.
2. On the issuing CA publish the "OCSP Response Signing" template; give the responder computer account Read + Enroll (Autoenroll).
3. CA properties > Extensions > AIA: add `http://ocsp.example.com/ocsp`, tick "Include in the online certificate status protocol (OCSP) extension".
4. Responder console (ocsp.msc): Revocation Configuration > Add: choose the CA cert, auto-enroll for the signing cert, set Base CRL source.
5. Array members share config for HA; load balance on the OCSP URL.
- Signing cert must carry `id-pkix-ocsp-nocheck`.
- Update clients' certs: only newly issued certs carry the OCSP URL.
Gotcha: reissue is required for the AIA OCSP entry to appear in existing certificates; until then clients fall back to CRL.
Verify:
- [ ] `certutil -URL leaf.cer` > OCSP shows Verified.
- [ ] `openssl ocsp -issuer ca.pem -cert leaf.pem -url http://ocsp.example.com/ocsp` returns `good`.
