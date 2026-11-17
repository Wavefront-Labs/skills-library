---
id: computing-software.systems-network-administration.pki-tls-administration.pqc-readiness-hybrid-kex
name: pqc-readiness-hybrid-kex
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [pqc-readiness-hybrid-kex, pki-pqc-migration, post-quantum, ml-kem, hybrid-kex, x25519mlkem768, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Prepare for post-quantum TLS: NIST FIPS 203/204/205, the TLS 1.3 hybrid groups incl. X25519MLKEM768, and an inventory-first migration plan."
sources:
  - https://csrc.nist.gov/projects/post-quantum-cryptography
  - https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-quantum readiness and hybrid key exchange
Goal: protect long-lived confidentiality against harvest-now-decrypt-later.

## What the sources confirm
- NIST released its principal PQC standards in August 2024: FIPS 203 (ML-KEM, key encapsulation), FIPS 204 (ML-DSA, signatures) and FIPS 205 (SLH-DSA, stateless hash-based signatures). NIST says organisations should begin applying them now; Falcon (signatures) and HQC (key encapsulation) were selected for ongoing standardisation.
- NIST says organisations must identify where vulnerable algorithms are used and plan to replace or update them. Under NIST IR 8547, NIST will deprecate and ultimately remove quantum-vulnerable algorithms from its standards by 2035, with high-risk systems transitioning much earlier.
- The IETF TLS working group document `draft-ietf-tls-ecdhe-mlkem` defines three post-quantum/traditional hybrid key agreement groups for TLS 1.3: X25519MLKEM768, SecP256r1MLKEM768 and SecP384r1MLKEM1024. The datatracker page now lists it as RFC 10024 (Proposed Standard, August 2026). X25519MLKEM768 has code point 4588 (0x11EC); SecP256r1MLKEM768 is 4587 (0x11EB). Per the document, the shared secret is the concatenation of the ML-KEM secret and the ECDHE secret, ML-KEM first for X25519MLKEM768 and ECDHE first for the two NIST-curve groups; this matters where FIPS-certified implementations are required (the document notes which component must be certified for each).

## Plan (practitioner guidance, not from the sources)
- Inventory where RSA, ECDH and ECDSA are used (TLS endpoints, internal mTLS, code signing, VPNs) and rank by how long the data must stay confidential.
- Prefer a hybrid group in the server's TLS 1.3 group list once your TLS library supports it; check your library's release notes for the exact group name and version, then test with a client that offers it.
- Treat PQC certificates and signature migration as a separate, later track from key exchange; plan crypto-agility and test larger handshakes and HSM firmware support.

## Verify
- [ ] An inventory exists that lists algorithms and key sizes per endpoint.
- [ ] A test client negotiates a hybrid group against a staging server, confirmed from the library's own handshake output.
- [ ] Handshake failure rate is monitored before and after any change.

## Checked
Method: docs-checked 2026-11-09 against the NIST PQC project page and the IETF datatracker page for draft-ietf-tls-ecdhe-mlkem (read in full).
Removed as unconfirmed: that X25519MLKEM768 is default in Chrome, Firefox and Cloudflare, OpenSSL 3.5 and Go support claims, the OpenSSL `Groups` and nginx `ssl_ecdh_curve` configuration lines, the `openssl s_client -groups` test command, the "deprecates RSA/ECC by 2030" figure (the NIST page says 2035), "PQC certificates are not in WebPKI yet", and the middlebox fragmentation gotcha. The draft's "not yet standardised" status was corrected: datatracker now lists an RFC.
