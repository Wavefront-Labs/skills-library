---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-encrypted-nameid-attribute
name: saml-encrypted-nameid-attribute
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-encrypted-nameid-attribute, saml-xml-encryption, encryptedid, encryptedattribute, partial-encryption, privacy, identity-protocols]
level: advanced
status: docs-checked
description: "Encrypt only the NameID or specific attributes with EncryptedID and EncryptedAttribute when full assertion encryption is not possible."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://www.w3.org/TR/xmlenc-core1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EncryptedID and EncryptedAttribute

Goal: hide the sensitive part of an assertion from untrusted relays.

Method (SAML Core 2.0 sections 2.2.4, 2.7.3.2, 6): `saml:EncryptedID` replaces a `BaseID` or `NameID`, and `saml:EncryptedAttribute` replaces an `Attribute`; each contains a required `xenc:EncryptedData` and zero or more `xenc:EncryptedKey`, as for EncryptedAssertion. Core describes encrypted identifiers as a privacy protection when the plaintext value passes through an intermediary, and requires the ciphertext to be unique to each encryption operation. The identifier may be requested with NameIDPolicy Format `urn:oasis:names:tc:SAML:2.0:nameid-format:encrypted`, which means the resulting assertions MUST contain `EncryptedID` instead of plaintext. `EncryptedID` is also allowed in `LogoutRequest` and in name identifier management requests (including `NewEncryptedID`).

- Order (section 6.2): when a `BaseID`, `NameID` or `Attribute` is encrypted, encryption MUST be performed first and then the signature calculated over the assertion or message containing the encrypted element. This is the reverse of the whole-assertion case, where the signature is inside the encrypted Assertion.
- Query processing (section 3.3.4): when a query Subject is matched against a returned Subject, the identifier MAY be encrypted or not in either, but its content and attribute values MUST be the same.

Gotchas:
- The recipient must be able to decrypt, so confirm it holds the private key for the certificate you encrypted to, and log decryption failures explicitly.
- Encrypting parts leaves Issuer, conditions and timing visible; this does not give message confidentiality.

Verify: use a test SP whose private key is missing and confirm the failure is reported as a decryption error.

## Checked

2026-11-09. Confirmed in SAML Core 2.0 sections 2.2.4, 2.7.3.2, 3.3.4, 3.4.1.1 and the name ID management and logout request definitions (EncryptedID, NewEncryptedID), 6.1 and 6.2 (encrypt then sign for identifiers and attributes); XML Encryption structure from the same elements. Removed: the claim that many SPs cannot handle EncryptedID in LogoutRequest and the "unknown user" symptom claim (not in the pages).
Method: documentation only; no commands were run.
