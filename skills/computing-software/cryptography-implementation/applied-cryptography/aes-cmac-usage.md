---
id: computing-software.cryptography-implementation.applied-cryptography.aes-cmac-usage
name: aes-cmac-usage
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, message-authentication-code, aes-cmac, cmac, sp-800-38b, rfc-4493, openssl, pyca]
level: practitioner
status: verified
description: "Compute and verify AES-CMAC with OpenSSL 3 EVP_MAC, the openssl mac command and pyca, with RFC 4493 vectors, tag length and when CMAC beats HMAC."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/b/upd1/final", "https://www.rfc-editor.org/rfc/rfc4493", "https://docs.openssl.org/3.0/man7/EVP_MAC-CMAC/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AES-CMAC usage

CMAC (SP 800-38B, RFC 4493 for AES-128) is a block-cipher MAC. Pick it when
only an AES engine is available (smart cards, EMV, HSMs, IoT), or the
protocol requires it (AES-SIV, SP 800-108 KBKDF with CMAC).
Otherwise HMAC-SHA-256 is the default.

## OpenSSL 3

```bash
openssl mac -cipher AES-128-CBC -macopt hexkey:2b7e151628aed2a6abf7158809cf4f3c \
  -in msg.bin CMAC
```

In C use `EVP_MAC_fetch(NULL, "CMAC", NULL)`; the underlying cipher is the
`cipher` parameter (`OSSL_MAC_PARAM_CIPHER`, a UTF-8 string such as
"AES-256-CBC") and the key goes to `EVP_MAC_init()` (EVP_MAC-CMAC man page).
The `openssl mac` command above is the same provider code. The C snippet is
not compiled here (no C compiler): follow the man page example.
The output is the raw tag (16 bytes for AES), printed as colon-less upper-case
hex by `openssl mac` 3.2.

## Python (pyca/cryptography)

```python
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
c = cmac.CMAC(algorithms.AES(key)); c.update(msg)
c.verify(tag)        # constant-time; raises InvalidSignature
```

## Rules

- Key: a dedicated AES key; never the same key used for CBC/CTR encryption.
- Tag: full 128 bits. SP 800-38B Appendix A.2: Tlen of at least 64 should
  suffice against guessing; less than 64 only after a careful risk analysis.
  Appendix A.1: limit unsuccessful verification attempts per key.
- Volume: SP 800-38B default recommendation is no more than 2^48 messages per
  CMAC key for a 128-bit block cipher (2^21 for 64-bit blocks such as TDEA).
- CMAC has no IV; it is deterministic, so identical messages give identical
  tags (fine for a MAC, wrong if you wanted a PRF on low-entropy input you
  meant to hide).
- Do not hand-roll CBC-MAC; raw CBC-MAC is insecure for variable-length
  messages, which is exactly what CMAC's subkeys fix.

## Verify

- [ ] RFC 4493 vectors (empty, 16, 40, 64-byte messages) pass.
- [ ] Verification uses a constant-time compare (`c.verify`, `CRYPTO_memcmp`).
