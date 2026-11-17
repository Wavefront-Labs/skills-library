---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-cbc-padding-oracle
name: saml-cbc-padding-oracle
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-cbc-padding-oracle, saml-xml-encryption, aes-cbc, padding-oracle, rsa-oaep, rsa-1_5, gcm, identity-protocols]
level: sme
status: docs-checked
description: "Avoid XML Encryption CBC and RSA PKCS1 v1.5 weaknesses: prefer AES-GCM and RSA-OAEP, reject legacy ciphertexts, fail with one generic error."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://www.w3.org/TR/xmlenc-core1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block cipher choice and padding oracle risk

Goal: close known XML Encryption attacks.

Background (XML Encryption 1.1, section 6): chosen-ciphertext attacks have been demonstrated against CBC mode and against RSA PKCS#1 v1.5 key transport (Bleichenbacher). They need a server that signals whether decrypted text is well-formed, by different error messages or timing. The only fully effective countermeasure is to stop the attacker sending arbitrary ciphertext, which requires integrity protection bound to the encryption key; the spec calls an authenticating mode such as GCM the simplest and most efficient way. Implementations are told to avoid distinct error messages and timing differences, though that alone is not sufficient in an XML protocol (encryption wrapping). The spec recommends RSA-OAEP over PKCS#1 v1.5 for the encrypted key.

Method:
- Use AES-GCM for content (`http://www.w3.org/2009/xmlenc11#aes128-gcm` is required by XML Encryption 1.1; `...#aes256-gcm` is optional) and RSA-OAEP for key transport (`http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p`, required; `http://www.w3.org/2009/xmlenc11#rsa-oaep` is optional). The spec says AES-CBC and RSA-1.5 identifiers remain only for backward compatibility.
- Backwards-compatibility attacks (section 6.1.3): if a server also accepts AES-CBC or RSA-PKCS#1 v1.5, an attacker may force legacy processing of eavesdropped GCM or OAEP ciphertext. The spec says implementations SHOULD restrict algorithms to those known secure against chosen-ciphertext attacks (RSA-OAEP, AES-GCM) and SHOULD reject documents containing PKCS#1 v1.5 or AES-CBC ciphertexts without decrypting them; and SHOULD use different key pairs for confidentiality and for signing.
- Return one generic error for any decryption failure (section 6.7) and keep processing time for distinct errors from differing systematically (6.8); treat bursts of algorithm-processing errors from one origin as suspect, so rate limit the ACS endpoint.

Gotchas:
- Libraries differ; some peers still send only CBC. Confirm peer support before refusing it.
- Signing the assertion inside the encrypted content does not stop oracle probing of the outer EncryptedData; integrity of the ciphertext (GCM) does.

Verify: send a malformed EncryptedData and confirm the response is identical to a wrong-key case.

## Checked

2026-11-09. Confirmed in W3C XML Encryption 1.1 sections 6.1 to 6.1.3, 6.7, 6.8, 6.9 and the algorithm identifier list (GCM URIs use the xmlenc11 namespace; rsa-oaep-mgf1p is the required key transport). Removed: the claim that 1.1 adds RSA-OAEP with SHA-256 options (not read), and the SAML Core PDF is cited only for the SAML context. Corrected: the earlier unqualified aes256-gcm and rsa-oaep names.
Method: documentation only; no commands were run.
