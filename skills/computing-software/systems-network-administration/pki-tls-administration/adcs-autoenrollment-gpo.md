---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-autoenrollment-gpo
name: adcs-autoenrollment-gpo
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-autoenrollment-gpo, pki-adcs-templates, adcs, autoenrollment, gpo, certificate-services-client, pki-tls-administration]
level: practitioner
status: draft
description: "Configure certificate autoenrolment for users and computers with GPO, template permissions and renewal settings."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/active-directory-certificate-services-overview
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/certificate-autoenrollment
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Autoenrolment through Group Policy
Goal: certificates arrive and renew without admin action.
1. Template Security tab: group has Read, Enroll, Autoenroll. For users, enable "Publish in AD" only when needed.
2. GPO (Computer or User Configuration > Policies > Windows Settings > Security Settings > Public Key Policies > Certificate Services Client - Auto-Enrollment): Enabled, tick "Renew expired certificates, update pending, and remove revoked" and "Update certificates that use certificate templates".
3. Machines run autoenrol at policy refresh and every 8 hours; force with `certutil -pulse` or `gpupdate /force`.
4. Template Issuance Requirements: set renewal period (default 6 weeks) shorter than validity/2.
5. Lifecycle: set "Validity period" and "Renewal period" together with the CA validity.
Troubleshoot: Event Viewer > Applications and Services > Microsoft > Windows > CertificateServicesClient-Lifecycle-System, and `certutil -v -template`.
Gotcha: Version 1 templates cannot autoenrol; duplicate to v2 or later.
Verify:
- [ ] `Get-ChildItem Cert:\LocalMachine\My` shows the autoenrolled certificate after pulse.
- [ ] Event 19 (enrolled) appears, no event 6/7 errors.
