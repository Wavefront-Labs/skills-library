---
id: computing-software.cybersecurity-defensive.application-security.cryptographic-failures
name: cryptographic-failures
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [cryptographic-failures, owasp-a02, encryption, password-hashing, key-management, aes-gcm]
level: practitioner
status: docs-checked
description: "Find and fix cryptographic failures in stored data: password hashing parameters, authenticated encryption, secure randomness, key storage and rotation."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cryptographic failures (OWASP A02:2021)

## Start with the threat model and data minimisation
Decide who you protect the data against; that determines the layer to encrypt at (application, database, filesystem
such as LUKS, hardware). Hardware encryption protects against physical theft but not remote compromise. The best
protection is not storing sensitive data at all (card data is the usual example, because of PCI DSS storage rules).

## Passwords
Hash, never encrypt reversibly; use a unique salt per password (libraries normally generate it). Per the OWASP
Password Storage Cheat Sheet, in order of preference:
- **Argon2id** (minimum configurations, equivalent defence): m=47104 KiB t=1 p=1; m=19456 (19 MiB) t=2 p=1; m=12288
  t=3 p=1; m=9216 t=4 p=1; m=7168 t=5 p=1.
- **scrypt** when Argon2id is unavailable: N=2^17, r=8, p=1 (or N=2^16 p=2, N=2^15 p=3, N=2^14 p=5, N=2^13 p=10).
- **bcrypt** for legacy systems only: work factor 10 or more, and enforce a maximum password length of 72 bytes.
- **PBKDF2** where FIPS-140 is required: HMAC-SHA-256 with 600,000 iterations (HMAC-SHA-512: 220,000).
- Fast hashes such as MD5, SHA-1 and SHA-256 are unsuitable. A pepper (a secret shared across passwords, stored
  outside the database in a vault or HSM) adds defence in depth; changing it forces password resets.
- Benchmark on your hardware; hashing should generally take under a second. Re-hash at next login to raise the work
  factor.

## Encryption of stored data
- Symmetric: AES with a key of at least 128 bits (ideally 256) in an authenticated mode. GCM and CCM are the first
  preference; if unavailable, CTR or CBC with separate authentication (Encrypt-then-MAC). ECB should not be used.
- Public key: a maintained library implementing an established hybrid scheme such as HPKE; RSA keys at least 2048
  bits with OAEP padding. RSA and ECC are not post-quantum secure; for long-lived confidentiality plan for ML-KEM
  (NIST FIPS 203), typically hybrid.
- Do not design custom algorithms. Observe the mode's IV uniqueness and message-size limits (for AES-GCM see NIST
  SP 800-38D) and rotate keys before reaching them.
- Do not rely on encrypted URL parameters; keep access control in place so a crypto failure is not fatal.

## Randomness
Keys, IVs, session IDs and reset tokens must come from a CSPRNG. The cheat sheet's table of unsafe versus secure
functions includes: Java `java.util.Random` versus `SecureRandom`; Python `random()` versus `secrets`; Node.js
`Math.random()` versus `crypto.randomBytes()`; Go `math/rand` versus `crypto/rand`; C `rand()` versus
`getrandom(2)`; .NET `Random()` versus `RandomNumberGenerator`. Do not rely on the randomness of UUIDs: version 1 is
timestamp plus MAC address, and version 4 depends on the implementation.

## Keys
- Generate keys with a CSPRNG, never from words or keyboard mashing; keep data keys and key-encrypting keys
  independent.
- Rotate on compromise or suspicion (including staff leaving), after the cryptoperiod (NIST SP 800-57 Part 1 Rev. 5,
  section 5.3), at mode usage limits, or when an attack on the algorithm is announced. Have the rotation and
  algorithm-change code ready beforehand.
- Store keys in an HSM, key vault (Amazon KMS, Azure Key Vault) or secrets service (Conjur, HashiCorp Vault). Without
  one: no hard-coded keys, none in version control, restrictive file permissions, and avoid environment variables
  (exposed by `phpinfo()` or `/proc/self/environ`).
- Keep keys apart from the data they protect, and use envelope encryption: a data encryption key (DEK) encrypted by a
  key encryption key (KEK) stored on a separate system.

## Checked
Method: docs-checked 2026-11-09 against the OWASP Cryptographic Storage Cheat Sheet and Password Storage Cheat Sheet
(both read in full). Removed unconfirmed claims: the TLS and HSTS section and certificate-validation grep strings,
ChaCha20-Poly1305, libsodium and Tink, the 2^32 GCM message figure, the code-smell list, and the testssl.sh and
SAST verification steps. The OWASP Top 10 A02 page returned only a stub and was not used.
