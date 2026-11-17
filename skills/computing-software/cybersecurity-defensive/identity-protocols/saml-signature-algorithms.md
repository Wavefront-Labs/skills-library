---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-signature-algorithms
name: saml-signature-algorithms
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-signature-algorithms, saml-xml-signature, rsa-sha256, sha1, ecdsa, digest-method, signaturemethod, identity-protocols]
level: practitioner
status: docs-checked
description: "Choose SAML signature and digest algorithms: RSA-SHA256 or ECDSA-SHA256 with a SHA-256 digest, SHA-1 only as a dated legacy exception."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://www.w3.org/TR/xmldsig-core1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signature and digest algorithm selection

Goal: use algorithms that are still acceptable.

Method: declare `SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"` and `DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"`. `http://www.w3.org/2001/04/xmldsig-more#ecdsa-sha256` is the ECDSA alternative. In XML Signature 1.1 both RSAwithSHA256 and ECDSAwithSHA256 are listed as required signature algorithms, and SHA256 as a required digest.

- XML Signature 1.1 says SHA-256 is strongly recommended over SHA-1 and SHA-1 support is required only for backwards compatibility. SHA1 digest and HMAC-SHA1 are marked "use is DISCOURAGED"; RSAwithSHA1 is for verification, and generating it is discouraged.
- SAML Core 2.0 (2005) names only `rsa-sha1` (`http://www.w3.org/2000/09/xmldsig#rsa-sha1`) as the algorithm processors SHOULD support, and its examples use SHA-1. Treat that as dated: follow XML Signature 1.1 for new deployments, and agree algorithms with the peer.

Gotchas:
- Both the digest (in each Reference) and the signature algorithm matter; a SHA-1 DigestMethod keeps the SHA-1 weakness even under an RSA-SHA256 SignatureMethod.
- Rolling to SHA-256 requires the peer to accept it; test with a non-production app first.
- Do not accept `rsa-sha1` just to unblock a legacy peer without a dated exception.

Verify: inspect the signed XML for the Algorithm URIs.

## Checked

2026-11-09. Confirmed in W3C XML Signature 1.1 (algorithm identifiers section 6, message digests 6.2): the rsa-sha256, ecdsa-sha256 and xmlenc#sha256 URIs, required status, SHA-1 discouragement. Confirmed in SAML Core 2.0 section 5.4.1 and the example (rsa-sha1). Removed: the 2048-bit key size, the alg:SigningMethod/DigestMethod metadata extension, and the SaaS default claim (not in the cited pages).
Method: documentation only; no commands were run.
