---
id: computing-software.cryptography-implementation.openssl.building-pkcs12-bundles-with-chain
name: building-pkcs12-bundles-with-chain
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, pkcs12, pfx, pkcs12-export, certificate-chain, friendly-name, pbes2]
level: practitioner
status: verified
description: "Build PKCS#12/PFX bundles with openssl pkcs12 -export: key, leaf and full chain, friendly names, modern AES and iteration settings, and inspecting the result."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkcs12/", "https://www.rfc-editor.org/rfc/rfc7292", "https://www.rfc-editor.org/rfc/rfc9879"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building PKCS#12 bundles with chain

PKCS#12 (`.p12`/`.pfx`) is the interchange format for "private key plus its certificates"
for Windows, IIS, Java, Azure Key Vault, macOS and many appliances.

## Build
```
openssl pkcs12 -export -inkey api.key -in api.pem -certfile intermediates.pem \
  -name "api.example.com 2026-10" -out api.p12 -passout file:p12pass.txt
```
- `-in` is the leaf. `-certfile` adds the intermediates; most importers place them in the
  intermediate store and use them for chain sending (IIS, Java SSL).
- `-chain -CAfile bundle.pem` builds and includes the chain automatically and fails if it can't
  (`Error getting chain: unable to get local issuer certificate`), which catches a wrong intermediate early. If the
  root is in the `-CAfile`, it is included in the output too (tested: 3 certificates).
- `-name` sets the friendlyName attribute (shown by `-info` as `friendlyName:`); importers typically use it as the
  entry's label or alias.
- Don't include the root unless the consumer needs it (it's ignored by TLS servers).

## Encryption and MAC settings
OpenSSL 3 defaults: PBES2 with PBKDF2-HMAC-SHA256 and AES-256-CBC for both key and cert bags,
HMAC-SHA256 MAC, 2048 iterations. Raise the count for files that travel:
```
openssl pkcs12 -export ... -iter 600000 -maciter -macalg sha256
```
(`-iter` sets the count for both encryption and MAC; `-maciter` is accepted but unused, `-nomaciter` drops the MAC
count to 1). OpenSSL 3.4+ documents `-pbmac1_pbkdf2` to write a PBMAC1 MAC (RFC 9879, which obsoletes RFC 9579);
confirm your consumer supports PBMAC1 before using it. Old consumers that can't read any of this need the legacy
algorithms (see the legacy PKCS#12 skill).

## Inspect
```
openssl pkcs12 -in api.p12 -info -noout -passin file:p12pass.txt
```
Prints `MAC: sha256, Iteration 600000`, then per bag `PKCS7 Encrypted data: PBES2, PBKDF2,
AES-256-CBC` and `Shrouded Keybag: PBES2...`. Count certificates:
`openssl pkcs12 -in api.p12 -nokeys -passin file:p12pass.txt | grep -c BEGIN`.

## Passwords
- Use a random password from a secrets manager and pass it via `file:`/`env:`, not `pass:`.
- Some importers may fail on an empty password or non-ASCII characters; ASCII-only random passwords are the
  portable choice. (OpenSSL itself accepted an empty password in a test export.)
- The PKCS#12 password protects the file in transit, not in storage; once imported, the
  target platform's own key protection applies.

## Gotchas
- Key/cert mismatch: OpenSSL 3.2.3 refuses with `No cert in -in file ... matches private key`; older versions may not,
  so compare SPKI hashes first.
- Mixed key and cert in one PEM: `-in combined.pem` works, `-inkey` optional.
- Azure Key Vault and AWS ACM import PKCS#12 or PEM with their own size and algorithm limits;
  read their docs for supported key types.

## Verify
- [ ] `-info` shows SHA-256 MAC, AES-256 PBES2 and the intended iteration count.
- [ ] The bundle contains leaf + intermediates and the key, with the right friendlyName.
- [ ] The target platform imports it and serves the full chain.
