---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-encrypted-assertion
name: saml-encrypted-assertion
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-encrypted-assertion, saml-xml-encryption, encryptedassertion, encryptedkey, xmlenc, sign-then-encrypt, identity-protocols]
level: advanced
status: docs-checked
description: "Send assertions encrypted to the SP key: EncryptedAssertion, EncryptedKey, signing before encrypting, and GCM plus OAEP algorithm choice."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://www.w3.org/TR/xmlenc-core1/
  - https://docs.oasis-open.org/security/saml/v2.0/saml-sec-consider-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EncryptedAssertion and sign-then-encrypt

Goal: protect assertion contents from intermediaries.

Method (SAML Core 2.0 sections 2.3.4 and 6): `saml:EncryptedAssertion` carries an assertion in encrypted form. It contains a required `xenc:EncryptedData` (the encrypted content; its Type attribute SHOULD be present and then MUST be `http://www.w3.org/2001/04/xmlenc#Element`) and zero or more `xenc:EncryptedKey` (wrapped decryption keys; each SHOULD carry a Recipient attribute naming the entity the key is encrypted for). The encrypted data and keys replace the plaintext in the same location in the XML instance.

- Order (section 6.2): when a signed Assertion is encrypted, the signature MUST first be calculated and placed inside the Assertion before it is encrypted. The relying party MUST validate the signature and decrypt in the reverse order of signing and encryption, so decrypt first, then verify.
- Algorithms: any XML Encryption algorithm MAY be used. XML Encryption 1.1 strongly recommends AES-GCM over CBC and RSA-OAEP over RSA-1.5 (`http://www.w3.org/2009/xmlenc11#aes128-gcm`, `http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p`); see saml-cbc-padding-oracle.
- Core lists assertion encryption as one of the ways to protect all or part of an assertion; transport confidentiality (for example TLS in a binding) is a separate mechanism.

Gotchas:
- Encryption does not protect against replay: SAML Security Considerations 6.1.2 (written about the SOAP binding) notes that a replayer does not need to understand the message, so XML Encryption gives no replay protection. Keep time and ID checks.
- Decryption failures at the SP surface as a missing or unusable assertion; confirm the SP private key matches the certificate the IdP encrypted to.

Verify: decrypt a sample with the SP private key in your XML security library and confirm the inner signature still validates.

## Checked

2026-11-09. Confirmed in SAML Core 2.0 sections 2.3.4 (EncryptedAssertion), 6.1 and 6.2 (replacement and ordering), SAML Security Considerations 6.1.2 (replay, read from the text), and W3C XML Encryption 1.1 (algorithm identifiers, section 6). Removed: use="encryption" key descriptors (metadata, unread), the claim that an attacker can swap encrypted assertions when only the Response is signed, xmlsec1, and "TLS alone does not" protect attributes from the browser.
Method: documentation only; no commands were run.
