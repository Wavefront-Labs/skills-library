---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-two-tier-deployment
name: adcs-two-tier-deployment
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-two-tier-deployment, pki-adcs-design, adcs, enterprise-ca, standalone-root, pki-tls-administration]
level: practitioner
status: draft
description: "Deploy a standalone offline root CA and an enterprise issuing CA on Windows Server, with CAPolicy.inf and post-install configuration."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/active-directory-certificate-services-overview
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AD CS two-tier deployment
Goal: offline root plus domain-joined enterprise issuing CA.
1. Root (workgroup, offline): write `%windir%\CAPolicy.inf` before install:
```
[Version]
Signature="$Windows NT$"
[certsrv_server]
RenewalKeyLength=4096
RenewalValidityPeriod=Years
RenewalValidityPeriodUnits=20
CRLPeriod=Months
CRLPeriodUnits=6
```
2. `Install-AdcsCertificationAuthority -CAType StandaloneRootCa -KeyLength 4096 -HashAlgorithmName SHA256 -ValidityPeriod Years -ValidityPeriodUnits 20`
3. Set AIA/CDP (see publishing skill), then issue the subordinate: submit the issuing CA's request, `certreq -submit`, then `certutil -resubmit`.
4. Issuing CA (domain joined, Enterprise Subordinate): install, import the root, install the signed cert with `certutil -installcert`.
Gotcha: CAPolicy.inf is read at install and renewal only; a typo is silently ignored, so verify the resulting CA settings.
Verify:
- [ ] `certutil -CAInfo` and `certutil -getreg CA\CRLPeriod*` show the expected values.
- [ ] `pkiview.msc` shows all certs and CRLs green.
