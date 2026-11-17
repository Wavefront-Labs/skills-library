---
id: computing-software.cryptography-implementation.applied-cryptography.rsa-public-key-validation
name: rsa-public-key-validation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, rsa-public-key-validation, rsa, sp-800-89, sp-800-56b, public-key-validation, input-validation, rsa-exponent]
level: advanced
status: docs-checked
description: "Validate RSA public keys received from peers or users: modulus size and parity, exponent range, small factors and full validation per SP 800-89 and 800-56B."
sources: ["https://csrc.nist.gov/pubs/sp/800/89/final", "https://csrc.nist.gov/pubs/sp/800/56/b/r2/final", "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-89.pdf", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Br2.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RSA public key validation

Accepting an arbitrary (n, e) and using it for encryption or verification can break protocols: e = 1 makes
"encryption" the identity, an even or tiny n is factorable, huge keys are a DoS vector.

## Partial public-key validation (SP 800-89, SP 800-56B Rev 2)
1. The modulus bit length is one of the sizes your policy allows, and n has exactly that bit length.
2. n and e are odd.
3. n has no factors smaller than 752 (SP 800-89).
4. e is an odd integer with 65,537 <= e < 2^256 (SP 800-56B Rev 2). In practice require e = 65537 unless
   interoperability forces otherwise.

Full validation additionally needs more than the public key alone (SP 800-56B Rev 2 describes checks that use the
prime factors or assurance from the key generator), so it is only possible for your own keys or with assurance
from the generator.

## Also check
- Set an upper bound on modulus size: verification cost grows with modulus size, so unbounded sizes are a CPU DoS.
- Known weak-key blocklists for keys you will trust long-term.
- The key's intended use (keyUsage in certificates) matches what you do with it.

## Verify
- [ ] Keys with e = 3, e = 1, an even n, or a modulus below your minimum size are rejected in tests.
- [ ] The size cap stops oversized keys from reaching verification.

## Checked
2026-11-01. Confirmed in SP 800-89 (modulus and exponent odd; modulus has no factors smaller than 752) and
SP 800-56B Rev 2 (odd e with 65,537 <= e < 2^256). Removed: specific allowed modulus sizes, the perfect-power
test, the FIPS 186-5 attribution for the exponent range, the code sample, the OpenSSL commands and the named
weak-key families.
Method: documentation only; no commands were run.
