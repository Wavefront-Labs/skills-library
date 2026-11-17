---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-esc-hardening
name: adcs-esc-hardening
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-esc-hardening, pki-adcs-templates, adcs, esc1, certificate-template-abuse, hardening, pki-tls-administration]
level: practitioner
status: draft
description: "Audit AD CS for known misconfigurations (ESC1 through ESC8 families) and fix them with template, CA flag and web enrolment settings."
sources:
  - https://posts.specterops.io/certified-pre-owned-d95910965cd2
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AD CS misconfiguration hardening
Goal: close the common paths where enrolment rights become domain compromise (defensive audit).
- ESC1: template allows requester-supplied SAN with an authentication EKU and low-privileged enrol rights. Fix: remove "Supply in the request" or restrict enrollment.
- ESC2/3: Any Purpose or enrollment-agent templates open to broad groups; restrict.
- ESC4: write access on templates for non-admins; review ACLs.
- ESC6: CA flag `EDITF_ATTRIBUTESUBJECTALTNAME2`; check `certutil -getreg policy\EditFlags` and clear it.
- ESC7: ManageCA or ManageCertificates rights for low-privilege groups.
- ESC8: HTTP web enrolment or CES with NTLM; enforce HTTPS with Extended Protection or disable NTLM.
- Strong certificate mapping: apply KB5014754 StrongCertificateBindingEnforcement (confirm enforcement mode).
- Audit tools: `certutil`, PSPKIAudit or Certify/Certipy used by your own team in a lab, and Defender for Identity alerts.
Gotcha: removing the SAN flag breaks apps that rely on it; migrate them to dedicated templates with approvals first.
Verify:
- [ ] No enrollable authentication template permits requester-supplied subject for Authenticated Users.
- [ ] `certutil -getreg policy\EditFlags` does not include 0x40000.
