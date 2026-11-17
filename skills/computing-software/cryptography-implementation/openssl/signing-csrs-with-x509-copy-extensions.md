---
id: computing-software.cryptography-implementation.openssl.signing-csrs-with-x509-copy-extensions
name: signing-csrs-with-x509-copy-extensions
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, copy-extensions, openssl-x509, csr-signing, x509v3-extensions, basic-constraints, extfile, certificate-issuance]
level: practitioner
status: verified
description: "Sign CSRs with openssl x509 -req safely: -copy_extensions behaviour, mandatory extfile overrides for basicConstraints and keyUsage, serials and validity."
sources: ["https://docs.openssl.org/3.0/man1/openssl-x509/", "https://docs.openssl.org/3.0/man5/x509v3_config/", "https://docs.openssl.org/3.0/man1/openssl-ca/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing CSRs with x509 -req and -copy_extensions

## The basic command (OpenSSL 3.0+)
```
openssl x509 -req -in leaf.csr -CA ca.pem -CAkey ca.key -CAcreateserial \
  -days 90 -sha256 -copy_extensions copy -extfile leaf.ext -extensions v3_leaf -out leaf.pem
```
`leaf.ext`:
```
[v3_leaf]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature
extendedKeyUsage = serverAuth
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid
```

## -copy_extensions values
| Value | Effect |
|---|---|
| `none` (default) | Ignore all CSR extensions, including SANs. Common cause of "my SANs vanished". |
| `copy`, `copyall` | For `openssl x509`, the manual treats them the same: all CSR extensions are copied. Tested on 3.2.3: an extension also set in the extfile keeps the extfile value, and one the extfile does not set comes from the CSR. |

The `openssl ca` command differs: `copy` only adds extensions not already present, while `copyall` copies all request
extensions and deletes an existing one first (so `copyall` can override the config there).

## Safety rules
- Whichever of `copy`/`copyall` you use, always set `basicConstraints` and `keyUsage` in the extfile; otherwise a CSR
  containing `CA:TRUE` is copied and you issue a sub-CA (tested: both modes produced `CA:TRUE` when the extfile omitted
  basicConstraints, and `CA:FALSE` when it set it).
- With `openssl ca`, never use `copyall` for CSRs you did not create (the manual's warning).
- If you must accept requester SANs, validate them (allowed domains) before signing; the safest path is to put the
  approved SANs in the extfile yourself and use `-copy_extensions none`.

## OpenSSL 1.1.1
No `-copy_extensions` on `x509`; SANs must be supplied via `-extfile`. `openssl ca` has had `copy_extensions` in the
config for longer and has the same `copy`/`copyall` semantics.

## Serials and validity
- `-CAcreateserial` writes `ca.srl`; for anything beyond a lab use random 128-bit serials (`-set_serial 0x$(openssl rand -hex 16)`).
- OpenSSL 3.4+ supports `-not_before` / `-not_after` for exact dates (3.4 changelog; 3.2.3 rejects them as unknown options);
  otherwise `-days`.

## Verify
- [ ] `openssl x509 -in leaf.pem -noout -ext basicConstraints,keyUsage,subjectAltName` shows the intended values.
- [ ] A CSR requesting `CA:TRUE` produces a leaf with `CA:FALSE`.
