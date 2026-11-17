---
id: computing-software.systems-network-administration.pki-tls-administration.smime-certificate-admin
name: smime-certificate-admin
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [smime-certificate-admin, pki-smime, smime, email-signing, key-escrow, certificate-store, pki-tls-administration]
level: practitioner
status: draft
description: "Run S/MIME certificates: choose profiles, issue via CA or MDM, handle key archival, distribution to directories and client configuration."
sources:
  - https://cabforum.org/working-groups/smime/
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# S/MIME certificate administration
Goal: users can sign and encrypt mail reliably.
- Profiles: separate certificates for signing (digitalSignature, nonRepudiation) and encryption (keyEncipherment) when you want key archival only for decryption.
- Public S/MIME BRs (2023+) define Legacy, Multipurpose and Strict profiles; mailbox validation is required (confirm).
- AD CS: template "User" duplicate with email in SAN (rfc822Name) and `emailProtection` EKU; enable key archival with a Key Recovery Agent for encryption templates.
- Distribute: publish the encryption certificate in AD `userCertificate` or LDAP/GAL so others can encrypt.
- Client: Outlook Trust Center > Email Security selects certs; Apple Mail auto-detects.
- Expiry: keep old encryption keys so archived mail stays readable (retain in key store).
- Revocation: CRL and OCSP, plus mailbox disablement process.
Gotcha: signing-only reissue overwriting the encryption certificate locks users out of old encrypted mail; keep key history.
Verify:
- [ ] Test message signs and recipients' clients show valid signature.
- [ ] KRA can recover a test encryption key.
