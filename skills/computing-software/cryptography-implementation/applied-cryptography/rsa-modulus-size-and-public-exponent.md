---
id: computing-software.cryptography-implementation.applied-cryptography.rsa-modulus-size-and-public-exponent
name: rsa-modulus-size-and-public-exponent
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, rsa-oaep, rsa-pss, rsa-key-size, public-exponent, e-65537, sp-800-131a, fips-186-5, key-generation, weak-keys]
level: practitioner
status: docs-checked
description: "Choose RSA modulus size and exponent: 2048 vs 3072 by protection lifetime, public exponent bounds from FIPS 186-5, and screening for shared-prime keys."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://csrc.nist.gov/pubs/sp/800/131/a/r2/final", "https://csrc.nist.gov/pubs/fips/186-5/final", "https://factorable.net/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RSA modulus size and public exponent

## Size by security strength (SP 800-57 Part 1 Rev. 5, Table 2)

| Modulus (k) | Strength | Use |
|---|---|---|
| 1024 | 80 bits | Below 112 bits: SP 800-131A Rev. 2 lists RSA signature generation with len(n) < 2048 as disallowed; verification of 1024 <= len(n) < 2048 is legacy use only |
| 2048 | 112 bits | Acceptable for applying protection now |
| 3072 | 128 bits | Needed where protection must outlast 2030 |
| 7680 | 192 bits | Table row for 192-bit strength |
| 15360 | 256 bits | Table row for 256-bit strength |

SP 800-131A Rev. 2 notes that SP 800-57 Part 1 includes a transition to 128-bit security strength
in 2030, so data needing, for example, 15 years of protection cannot rely on 112 bits. SP 800-57
footnotes that the strength estimates will be significantly affected when quantum computing
becomes practical, so plan a migration for long-lived keys. Table 2 has no row for 4096.

## Public exponent
FIPS 186-5 requires the RSA public exponent e to be an odd positive integer with
2^16 < e < 2^256, and p-1 and q-1 relatively prime to e; its key-generation algorithms return
failure when e violates this. The common value 65537 (2^16 + 1) satisfies these bounds, so keep
it as the default; accept no verification key whose e is even or below the bound.

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out k.pem
openssl pkey -in k.pem -noout -text
```

## Weak key screening (for keys you accept from others)
- Shared primes: the factorable.net study (Heninger, Durumeric, Wustrow, Halderman) obtained RSA
  private keys for 0.50% of TLS hosts and 0.03% of SSH hosts because public keys shared nontrivial
  common factors, caused by poor randomness at key generation on headless embedded devices that
  generate keys on first boot. Computing pairwise GCDs across collected moduli finds these.
- Reject moduli under your minimum at import time, not only at generation.

## Verify
- [ ] Inventory shows no RSA below 2048; 3072 or more where protection lifetime passes 2030.
- [ ] Imported public keys pass size and exponent checks and a shared-factor check.
- [ ] A migration plan exists for RSA keys protecting long-lived data.

## Checked
Method: docs-checked 2026-11-09 against SP 800-57 Part 1 Rev. 5 (Table 2, downloaded PDF), SP 800-131A Rev. 2 (signature table and 2030 transition text), FIPS 186-5 (public-exponent constraints and key-generation algorithms) and the factorable.net home page. Removed unconfirmed NIST IR 8547 dates, performance ratios, e=3 attack history, ROCA, Debian and 4096-bit comments.
