---
id: computing-software.cryptography-implementation.applied-cryptography.sp800-108-kbkdf-counter-mode
name: sp800-108-kbkdf-counter-mode
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, key-derivation, kbkdf, sp-800-108, counter-mode-kdf, hmac, cmac, openssl, pyca]
level: advanced
status: verified
description: "Derive keys with NIST SP 800-108 KBKDF in counter mode: input layout, label and context, r and L encodings, interop parameters, OpenSSL and pyca."
sources: ["https://csrc.nist.gov/pubs/sp/800/108/r1/upd1/final", "https://docs.openssl.org/3.0/man7/EVP_KDF-KB/", "https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#kbkdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SP 800-108 counter-mode KBKDF

SP 800-108 derives keys from a key (not a password) with a PRF (HMAC,
CMAC, or KMAC in Rev 1). It is the FIPS-friendly choice when HKDF is not
acceptable to an auditor, and appears in Windows CNG
(`BCRYPT_SP800108_CTR_HMAC_ALGORITHM` is listed in Microsoft's CNG algorithm identifiers) and Kerberos AES-SHA2 (RFC 8009,
which cites the counter-mode KDF of SP 800-108 section 5.1 of the original edition).

## Counter mode input

```
K(i) = PRF(KI, [i]_r || Label || 0x00 || Context || [L]_2)
OKM  = K(1) || K(2) || ... truncated to L bits
```

- `[i]_r`: counter, r bits, big-endian, starting at 1. SP 800-108 Rev 1 allows 1 <= r <= 32 (n must not exceed 2^r - 1);
  OpenSSL's `r` supports 8, 16, 24 and 32 (default 32).
- `Label`: purpose of the derived key.
- `0x00`: separator.
- `Context`: parties, nonces, session id.
- `[L]_2`: requested output length in bits, usually 32-bit big-endian.

Interop failures almost always come from disagreeing on r, the length
encoding width, whether the separator is present, or the counter position.
Write these down in the protocol spec.

## OpenSSL 3

```bash
openssl kdf -keylen 32 -kdfopt mac:HMAC -kdfopt digest:SHA256 \
  -kdfopt hexkey:$KI -kdfopt salt:"enc" -kdfopt info:"session-42" KBKDF
```

In OpenSSL's KBKDF, `salt` is the **Label** and `info` is the **Context** (EVP_KDF-KB man page: key, salt, info and seed are KI,
Label, Context and IV). Options `use-l` and `use-separator` (default on) toggle `[L]_2` and `0x00`; `mode` is `counter`
(default) or `feedback`, the only two OpenSSL implements. Run on OpenSSL 3.2.3: this command, the pyca code below and a
20-line HMAC loop of the formula above all return the same 32 bytes for KI = 00..1f, and `use-l:0` / `use-separator:0`
match the loop without `[L]_2` / without `0x00`. pyca's `fixed=None` builds Label || 0x00 || Context || [L]_2 the same way.

## pyca/cryptography

```python
from cryptography.hazmat.primitives.kdf.kbkdf import KBKDFHMAC, Mode, CounterLocation
from cryptography.hazmat.primitives import hashes
kdf = KBKDFHMAC(algorithm=hashes.SHA256(), mode=Mode.CounterMode, length=32,
                rlen=4, llen=4, location=CounterLocation.BeforeFixed,
                label=b"enc", context=b"session-42", fixed=None)
key = kdf.derive(ki)
```

`KBKDFCMAC` exists for the CMAC PRF.

## Rules

- KI must be a full-entropy key; for DH output, use SP 800-56C first.
- Distinct Label per purpose; Context binds the instance.

## Verify

- [ ] NIST CAVP KBKDF vectors for your r/L/location choice pass on both peers.
- [ ] Parameters (PRF, r, L width, separator) are fixed in the spec.
