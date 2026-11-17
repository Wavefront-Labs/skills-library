---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-cep-ces
name: adcs-cep-ces
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-cep-ces, pki-adcs-enrol, adcs, cep, ces, cross-forest-enrollment, pki-tls-administration]
level: practitioner
status: draft
description: "Deploy CEP and CES for HTTPS-based enrolment by non-domain or cross-forest clients, with Kerberos or certificate authentication."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/certificate-enrollment-web-services
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Certificate Enrollment Policy and Web Service
Goal: enrolment over HTTPS where RPC/DCOM to the CA is not possible.
- CEP returns the template list; CES proxies enrolment to the CA.
- Install: `Install-AdcsEnrollmentPolicyWebService -AuthenticationType Kerberos` and `Install-AdcsEnrollmentWebService -AuthenticationType Kerberos -CAConfig "ca\Issuing CA"`.
- Auth types: Kerberos (domain clients), Username/Password (mobile, TLS required), Client Certificate (renewal-only for outside the domain).
- Kerberos delegation: configure the CES service account for constrained delegation to the CA's `host` SPN.
- Clients: GPO "Certificate Enrollment Policy" > add URI `https://pki.example.com/ADPolicyProvider_CEP_Kerberos/service.svc/CEP`.
- Publish through a reverse proxy for external access.
Gotcha: enable "Allow delegation" and test with `certreq -policyserver` before pointing GPO at it.
Verify:
- [ ] `certreq -enrollmentpolicyserver URL -new` lists templates.
- [ ] A certificate issues for a client not on the CA's network segment.
