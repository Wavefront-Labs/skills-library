---
id: computing-software.systems-network-administration.windows-server.two-tier-pki-offline-root
name: two-tier-pki-offline-root
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-cs, certificate-services, offline-root-ca, enterprise-ca, subordinate-ca, capolicy-inf, install-adcscertificationauthority, pki-hierarchy]
level: sme
status: draft
description: "Build a two-tier AD CS PKI: standalone offline root with CAPolicy.inf, enterprise issuing CA, signing the subordinate request, CRL/AIA paths and validity periods."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/core-network-guide/cncg/server-certs/install-the-certification-authority
  - https://learn.microsoft.com/en-us/powershell/module/adcsdeployment/install-adcscertificationauthority
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Two-tier PKI: offline root and enterprise issuing CA

## Design
- **Root CA**: standalone, workgroup, powered off between uses (VM kept offline, or HSM).
  Validity 20 years, publishes a CRL every 6-12 months.
- **Issuing CA**: enterprise (AD-integrated) subordinate, validity 10 years (half or less
  of the root's), CRL weekly with delta CRLs daily.
- HTTP CDP/AIA on a highly available web location (`http://pki.example.com/pki/`); LDAP
  paths optional and harmful for non-domain clients.

## Root CA
`CAPolicy.inf` in `%windir%` before installing:
```
[Version]
Signature="$Windows NT$"
[Certsrv_Server]
RenewalKeyLength=4096
RenewalValidityPeriod=Years
RenewalValidityPeriodUnits=20
CRLPeriod=Months
CRLPeriodUnits=6
CRLDeltaPeriodUnits=0
AlternateSignatureAlgorithm=0
```
```powershell
Install-WindowsFeature ADCS-Cert-Authority -IncludeManagementTools
Install-AdcsCertificationAuthority -CAType StandaloneRootCA -CACommonName 'Example Root CA' `
  -KeyLength 4096 -HashAlgorithmName SHA256 -ValidityPeriod Years -ValidityPeriodUnits 20
certutil -setreg CA\DSConfigDN 'CN=Configuration,DC=corp,DC=example,DC=com'
certutil -setreg CA\ValidityPeriodUnits 10        # max lifetime of certs it issues
certutil -setreg CA\CRLPublicationURLs '1:%windir%\system32\CertSrv\CertEnroll\%3%8%9.crl\n2:http://pki.example.com/pki/%3%8%9.crl'
certutil -setreg CA\CACertPublicationURLs '1:%windir%\system32\CertSrv\CertEnroll\%1_%3%4.crt\n2:http://pki.example.com/pki/%1_%3%4.crt'
Restart-Service certsvc; certutil -crl
```
Copy the root cert and CRL to the web location and publish to AD:
`certutil -dspublish -f root.crt RootCA` and `certutil -dspublish -f root.crl`.

## Issuing CA
```powershell
Install-AdcsCertificationAuthority -CAType EnterpriseSubordinateCA -CACommonName 'Example Issuing CA 1' `
  -KeyLength 4096 -HashAlgorithmName SHA256 -OutputCertRequestFile '<vol>:\issuing.req'
```
On the root: `certreq -submit issuing.req`, approve in the CA console (pending
requests), `certreq -retrieve <id> issuing.crt`. On the issuing CA:
`certutil -installcert issuing.crt`, `Start-Service certsvc`, set CDP/AIA like above
plus delta CRL settings, `certutil -crl`.

## Verify
- [ ] `pkiview.msc` all locations OK.
- [ ] `certutil -verify -urlfetch issued.cer` succeeds from a domain client and a non-domain client.
