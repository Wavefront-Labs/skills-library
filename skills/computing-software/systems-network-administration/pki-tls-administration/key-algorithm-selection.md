---
id: computing-software.systems-network-administration.pki-tls-administration.key-algorithm-selection
name: key-algorithm-selection
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [key-algorithm-selection, pki-key-mgmt, nist-800-52, key-algorithm, ecdsa-vs-rsa, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Pick RSA or ECDSA key types and sizes for CAs and TLS leaves using NIST SP 800-52r2 and SP 800-57 security-strength guidance."
sources:
  - https://csrc.nist.gov/pubs/sp/800/52/r2/final
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing key algorithms and sizes
Goal: algorithms that meet policy and still validate on your clients.
- NIST SP 800-57 Part 1 Rev 5 security strengths for asymmetric keys: 128 bits is RSA 3072 or an elliptic curve with f = 256-383 (P-256 class); 192 bits is RSA 7680 or f = 384-511 (P-384 class); 256 bits is RSA 15360 or f = 512+. The elliptic-curve column covers ECDSA and EdDSA. These estimates drop significantly if quantum computing becomes practical.
- SP 800-52r2: a conforming TLS server shall have at least an RSA signature certificate or an ECDSA signature certificate. DSA, DH and ECDH certificates exist but are rare on externally reachable servers.
- For an ECDSA server certificate, SP 800-52r2 says the curve should be P-256 or P-384. For RSA it gives 2048-bit modulus "or other approved lengths" in its certificate profile.
- Certificates with RSA, ECDSA or DSA public keys should be signed with those same algorithm families (an ECDH certificate should be signed with ECDSA). The sample CA profile there uses sha256WithRSAEncryption or RSASSA-PSS for an RSA CA.
- SP 800-52r2 recommends servers support algorithm and key-size agility, so keep certificate keys replaceable.
- Where old clients matter you can serve an RSA and an ECDSA certificate side by side on one server (check your server software supports multiple certificate types).
Gotcha: compatibility of ECDSA with very old clients and HSM curve support are your own checks; test the oldest supported client before standardising.
Verify:
- [ ] `openssl x509 -noout -text` shows the chosen key and `Signature Algorithm`.
- [ ] Oldest supported client validates the chain.

## Checked
Method: docs-checked 2026-11-09 against NIST SP 800-52r2 PDF (sections on server certificates and Table of certificate profile) and NIST SP 800-57 Part 1 Rev 5 PDF (security-strength table, section 5.6.1.1).
Removed: hash policy line, Ed25519/Ed448 WebPKI status, X25519, "RSA 3072 for long-lived CA", PQC claim, Java 6/Windows XP/HSM P-384 gotcha, nginx two-ssl_certificate claim (none in these sources).
