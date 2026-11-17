---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-keydescriptor-use
name: saml-keydescriptor-use
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-keydescriptor-use, saml-metadata, keydescriptor, signing, encryption, x509certificate, key-rollover, identity-protocols]
level: advanced
status: docs-checked
description: "Publish keys in SAML metadata with KeyDescriptor use=signing or use=encryption, with ds:KeyInfo and optional EncryptionMethod."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KeyDescriptor use signing and encryption

Goal: tell peers which key verifies signatures and which encrypts to you.

Method: `md:KeyDescriptor` describes the key an entity uses to sign data or receive encrypted keys. The optional `use` attribute takes `signing` or `encryption`. `ds:KeyInfo` is required and identifies the key directly or indirectly; zero or more `md:EncryptionMethod` elements list algorithms the entity supports (see XML Encryption).

- A requester that encrypts the principal's identifier in a logout request can use the responder's `KeyDescriptor` with `use="encryption"` to choose algorithm settings and the public key.

Gotchas:
- SAML does not require `ds:KeyInfo` inside signed messages or restrict its use, so do not treat a key carried in a message as trusted; rely on keys obtained through trusted metadata (practice).
- Check product documentation for key types, sizes and certificate expiry handling; the specification does not set them.

Verify: extract the certificate and compare its fingerprint with the one in the peer config.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Metadata to text and read 2.4.1.1 (KeyDescriptor: use, KeyInfo, EncryptionMethod), 3.1.5 (KeyInfo) and the Single Logout metadata note in Profiles 4.4.5. Removed the no-use-means-both claim, the rollover advice, the 2048-bit RSA/ECDSA guidance and the self-signed remarks (none stated there).
