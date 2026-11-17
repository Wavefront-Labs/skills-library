---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-offline-root-publishing
name: adcs-offline-root-publishing
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-offline-root-publishing, pki-adcs-design, adcs, certutil, dspublish, aia-cdp, pki-tls-administration]
level: practitioner
status: draft
description: "Publish an offline root certificate and CRL into Active Directory and an HTTP location with certutil, and set AIA and CDP on the root."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/active-directory-certificate-services-overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offline root publishing to AD and web
Goal: domain machines trust the root and can fetch its CRL.
On the root before first use:
```
certutil -setreg CA\CACertPublicationURLs "1:%windir%\system32\CertSrv\CertEnroll\%3%4.crt\n2:http://pki.example.com/pki/%3%4.crt"
certutil -setreg CA\CRLPublicationURLs "1:%windir%\system32\CertSrv\CertEnroll\%3%8.crl\n2:http://pki.example.com/pki/%3%8.crl"
certutil -setreg CA\CRLPeriodUnits 6 & certutil -setreg CA\CRLPeriod Months
certutil -crl
```
Copy `.crt`/`.crl` from CertEnroll to the web server, then on a DC or admin:
```
certutil -dspublish -f root.crt RootCA
certutil -dspublish -f root.crl <rootcaname>
```
This puts the root in AD (Trusted Root store via autoenrol) and CDP containers.
Gotcha: the HTTP name must match the AIA/CDP written into the issuing CA certs; changing it later requires reissuing.
Verify:
- [ ] `certutil -URL issuing.cer` shows AIA and CDP retrievable.
- [ ] `gpupdate /force` on a client puts the root in `Cert:\LocalMachine\Root`.
