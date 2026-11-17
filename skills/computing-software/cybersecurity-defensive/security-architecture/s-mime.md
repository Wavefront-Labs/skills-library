---
id: computing-software.cybersecurity-defensive.security-architecture.s-mime
name: s-mime
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [s-mime, smime, email-encryption, email-signing, certificate-enrolment, key-escrow, pki]
level: practitioner
status: draft
description: "Deploy S/MIME signing and encryption: certificate issuance and templates, key escrow for decryption keys, client configuration, GAL publication, and gateway interaction."
sources: ["https://datatracker.ietf.org/doc/html/rfc8551", "https://learn.microsoft.com/en-us/exchange/security-and-compliance/smime-exo/smime-exo", "https://cabforum.org/working-groups/smime/documents/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# S/MIME email encryption

## Certificates
- Public trust (for external recipients): S/MIME certificates under the CA/Browser Forum S/MIME Baseline Requirements (mailbox-validated, organisation-validated, sponsor-validated profiles).
- Internal: AD CS template with Secure Email EKU (1.3.6.1.5.5.7.3.4), subject email = mailbox address.
- Use **separate** signing and encryption keys: signing keys never escrowed (non-repudiation); encryption keys **must** be archived (AD CS key archival / KRA) or encrypted mail becomes unreadable when a user loses a key.

## Distribution
- Publish encryption certificates to the GAL (`userCertificate` / `userSMIMECertificate` attributes) so senders can find them.
- Exchange Online: upload the trusted root/intermediate chain as a virtual certificate collection (`Set-SmimeConfig -SMIMECertificateIssuingCA`).
- Clients: Outlook Trust Center -> Email Security; Outlook mobile and iOS Mail need certificate deployment via MDM (Intune PKCS/SCEP profiles).

## Operations
- Renew before expiry and keep old decryption keys - users need them to read old mail.
- Revocation: publish CRL/OCSP reachable by external recipients.

## Gateway interaction
- Encrypted mail cannot be scanned by the SEG/AV/DLP; decide policy: allow with caveats, decrypt at gateway (gateway holds keys), or block inbound encrypted from unknown senders.
- Signatures break if the gateway adds disclaimers/banners to the body; exempt signed mail or add banners only via headers.

## Gotchas
- Lost encryption key without archival = permanent data loss.
- Certificate email address must exactly match the sending address (aliases need SANs).

## Verify
- [ ] Signed message validates externally (recipient sees valid signature).
- [ ] Encrypted message readable after simulated key loss via KRA recovery.
