---
id: computing-software.cybersecurity-defensive.security-architecture.post-quantum-migration-planning
name: post-quantum-migration-planning
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [cryptography, post-quantum-migration, pqc, ml-kem, ml-dsa, fips-203, fips-204, crypto-agility, cryptographic-inventory, harvest-now-decrypt-later]
level: advanced
status: draft
description: "Plan post-quantum cryptography migration: cryptographic inventory, harvest-now-decrypt-later prioritisation, hybrid ML-KEM TLS, and crypto agility."
sources: ["NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA), August 2024", "NIST IR 8547 Transition to Post-Quantum Cryptography Standards (draft)", "CISA/NSA/NIST Quantum-Readiness factsheet", "NSA CNSA 2.0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-quantum migration planning

**Goal:** move to quantum-resistant algorithms before a cryptographically relevant quantum
computer exists, starting with data that must stay secret for many years.

## Standards (NIST, August 2024)
- **ML-KEM** (FIPS 203, from Kyber): key establishment.
- **ML-DSA** (FIPS 204, from Dilithium): signatures. **SLH-DSA** (FIPS 205, SPHINCS+): hash-based signatures.
- NIST IR 8547 (draft) proposes deprecating RSA and ECC-based quantum-vulnerable algorithms
  by 2030 and disallowing them by 2035. NSA CNSA 2.0 sets earlier dates for national security systems.

## Plan
1. **Cryptographic inventory**: where public-key crypto is used (TLS, VPN, SSH, code signing,
   PKI, S/MIME, document signing, databases, HSMs, embedded devices, third-party products).
   Sources: TLS scans, certificate inventory, SBOMs and crypto libraries, vendor questionnaires.
2. **Prioritise**:
   - Data with long confidentiality needs exposed to **harvest now, decrypt later** (recorded
     traffic today, decrypted in the future): key exchange in TLS/VPN for such data first.
   - Long-lived signatures and roots of trust (firmware signing, root CAs) next, since they are slow to replace.
3. **Hybrid key exchange now** where supported: TLS 1.3 `X25519MLKEM768` is enabled by default in
   current Chrome, Firefox, Cloudflare and recent OpenSSL (3.5+) and BoringSSL builds. OpenSSH
   9.9+ supports `mlkem768x25519-sha256` (default from 10.0).
4. **Crypto agility**: abstract algorithm choices in code and config, avoid hard-coded key sizes,
   be able to rotate algorithms without redesign.
5. **Vendor roadmap**: require PQC plans in procurement for HSMs, VPNs, PKI and IoT.

## Gotchas
- PQC keys and signatures are much larger (ML-DSA signatures ~2.4-4.6 KB): certificate chains and handshakes grow; some middleboxes break on large ClientHello messages.
- Symmetric crypto (AES-256) and hashes (SHA-384+) need only larger sizes, not replacement.
- "Quantum-safe" products not based on NIST standards: avoid proprietary schemes.

## Verify
- [ ] Inventory exists with algorithm, owner and migration priority for each use.
- [ ] Test: hybrid key exchange negotiated with a supporting client (check `openssl s_client -groups X25519MLKEM768`).
