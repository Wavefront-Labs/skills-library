---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-crl-aia-config
name: adcs-crl-aia-config
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-crl-aia-config, pki-adcs-revocation, adcs, crl-publishing, delta-crl, cdp, pki-tls-administration]
level: practitioner
status: draft
description: "Configure CRL and delta CRL periods, CDP and AIA locations and overlap on an AD CS issuing CA."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/active-directory-certificate-services-overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AD CS CRL and AIA publishing
Goal: clients always find a fresh CRL and the issuer certificate.
```
certutil -setreg CA\CRLPeriod Weeks
certutil -setreg CA\CRLPeriodUnits 1
certutil -setreg CA\CRLDeltaPeriod Days
certutil -setreg CA\CRLDeltaPeriodUnits 1
certutil -setreg CA\CRLOverlapPeriod Hours
certutil -setreg CA\CRLOverlapUnits 12
certutil -setreg CA\CRLPublicationURLs "65:%windir%\system32\CertSrv\CertEnroll\%3%8%9.crl\n6:http://pki.example.com/pki/%3%8%9.crl"
Restart-Service certsvc; certutil -crl
```
- Flag meaning: 1 publish locally, 2 include in CDP extension, 4 include in CRL IDP, 64 publish delta, 128 include in FreshestCRL.
- Copy CRLs to the web tier automatically with a scheduled task or by publishing to a UNC path.
- Avoid LDAP CDPs for non-domain clients.
Gotcha: forgetting the web-server copy leaves HTTP CDP stale while the CA looks healthy.
Verify:
- [ ] `certutil -URL leaf.cer` shows CDP and Delta CDP verified.
- [ ] PKIView shows CRL and Delta CRL as OK.
