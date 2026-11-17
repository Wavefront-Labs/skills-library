---
id: computing-software.cryptography-implementation.applied-cryptography.hkdf-extract-and-expand-parameters
name: hkdf-extract-and-expand-parameters
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, key-derivation, hkdf, hkdf-extract-expand, rfc-5869, salt, info-string, openssl, pyca]
level: practitioner
status: verified
description: "Choose HKDF salt, info and length correctly: when to skip extract, the 255xHashLen limit, distinct info per key, and OpenSSL, pyca and Go calls."
sources: ["https://www.rfc-editor.org/rfc/rfc5869", "https://eprint.iacr.org/2010/264", "https://docs.openssl.org/3.0/man7/EVP_KDF-HKDF/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HKDF extract and expand parameter choices

HKDF (RFC 5869) has two steps:

- **Extract** `PRK = HMAC(salt, IKM)` turns non-uniform input (a DH shared
  secret) into a uniform pseudorandom key.
- **Expand** `OKM = T(1) || T(2) ...` with `T(i) = HMAC(PRK, T(i-1) || info || i)`
  stretches PRK into as many keys as you need, bound to `info`.

## Parameter rules

| Parameter | Choice |
|---|---|
| IKM | DH/KEM shared secret or a high-entropy key. Never a password (use Argon2id/PBKDF2). |
| salt | Random or fixed non-secret value, ideally HashLen bytes; omitted means HashLen zero bytes. A salt the attacker cannot choose strengthens extraction. |
| info | Unique per derived key and purpose: protocol, version, role, key purpose, peer ids. Length-prefix variable parts. |
| L | At most 255 x HashLen (8160 bytes for SHA-256). |

**Skipping extract:** if IKM is already a uniformly random key (from a
CSPRNG or a previous HKDF), HKDF-Expand alone is fine (TLS 1.3 does this
for its traffic secrets via HKDF-Expand-Label). If IKM is a DH output, keep
extract.

Derive multiple keys with separate `info` values rather than slicing one
long output, so each key's purpose is explicit and independently testable.

## Calls

```bash
openssl kdf -keylen 32 -kdfopt digest:SHA256 -kdfopt hexkey:$IKM \
  -kdfopt hexsalt:$SALT -kdfopt info:"myapp v1 enc" HKDF
# -kdfopt mode:EXTRACT_ONLY / EXPAND_ONLY for one step (EXTRACT_ONLY needs
# keylen equal to the hash size; `hexinfo:` takes hex; info max 1024 bytes;
# output is colon-separated hex; checked with OpenSSL 3.2.3 against RFC 5869 A.1)
```

```python
from cryptography.hazmat.primitives.kdf.hkdf import HKDF, HKDFExpand
from cryptography.hazmat.primitives import hashes
k = HKDF(hashes.SHA256(), 32, salt=salt, info=b"myapp v1 enc").derive(ikm)
```

```go
key, err := hkdf.Key(sha256.New, secret, salt, "myapp v1 enc", 32) // crypto/hkdf, Go 1.24+ (run on 1.24.0)
```

## Pitfalls

- Reusing one `info` for two purposes gives two components the same key.
- Using HKDF output length > 255 x HashLen errors (pyca: `Cannot derive keys
  larger than 8160 octets`; Go: `hkdf: requested key length too large`);
  use a longer hash or derive more keys with distinct `info`.
- Treating `salt` as secret: it is not, and storing it is fine.

## Verify

- [ ] RFC 5869 Appendix A vectors pass.
- [ ] Each derived key has a documented unique `info`.
