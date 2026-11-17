---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-template-versions-permissions
name: adcs-template-versions-permissions
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-template-versions-permissions, pki-adcs-templates, adcs, certificate-template, enroll-permissions, pki-tls-administration]
level: practitioner
status: draft
description: "Duplicate and configure AD CS certificate templates, schema versions, subject name sources, key settings and Enroll or AutoEnroll permissions."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/active-directory-certificate-services-overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Certificate templates and permissions
Goal: purpose-built templates with least-privilege enrolment.
1. certtmpl.msc: duplicate the closest built-in template (never edit the original).
2. Compatibility: pick the lowest Windows version you support; v4 enables CNG and key attestation.
3. Request Handling: set minimum key size (RSA 2048+/ECDSA P-256), "Do not allow private key export", archive only if required.
4. Subject Name: "Build from Active Directory" for machines; "Supply in the request" only for web server templates restricted to named admins.
5. Security tab: grant Read + Enroll to a specific group; add Autoenroll only if the template is autoenrolled.
6. Publish on the CA: `certsrv.msc` > Certificate Templates > New > Template to Issue (or `certutil -setcatemplates +MyTemplate`).
7. Issuance requirements: manager approval or authorised signatures for sensitive templates.
Gotcha: a template with "Supply in the request" plus Client Authentication EKU and broad enrol rights allows impersonation of any account (ESC1); restrict it.
Verify:
- [ ] `certutil -catemplates` lists the template on the CA.
- [ ] `certutil -v -template MyTemplate` shows the intended flags.
