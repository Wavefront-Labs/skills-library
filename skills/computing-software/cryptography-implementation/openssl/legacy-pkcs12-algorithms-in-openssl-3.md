---
id: computing-software.cryptography-implementation.openssl.legacy-pkcs12-algorithms-in-openssl-3
name: legacy-pkcs12-algorithms-in-openssl-3
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, pkcs12, pfx, pkcs12-legacy, legacy-provider, rc2-40, 3des, openssl-3]
level: practitioner
status: verified
description: "Fix OpenSSL 3 PKCS#12 interop both ways: read old RC2/3DES PFX files with -legacy, and write files that older Windows, macOS and Java versions can import."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkcs12/", "https://docs.openssl.org/3.0/man7/OSSL_PROVIDER-legacy/", "https://docs.openssl.org/3.0/man7/migration_guide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy PKCS#12 algorithms and OpenSSL 3

Older PKCS#12 files encrypt certificates with RC2-40-CBC and keys with 3DES under the SHA-1
PKCS#12 KDF. OpenSSL 3 moved RC2 (and other old ciphers) into the **legacy provider**, which is
not loaded by default, and switched its own output to AES/PBKDF2.

## Symptom 1: reading an old .pfx fails
```
Error outputting keys and certificates
...error:0308010C:digital envelope routines::unsupported
```
Fix:
```
openssl pkcs12 -in old.pfx -legacy -noenc -out old.pem
```
`-legacy` loads the legacy provider. If that errors with "unable to load provider legacy",
the module isn't installed or `OPENSSL_MODULES` points elsewhere: check
`openssl list -providers -provider legacy` and install your distro's legacy provider package.
In code: `OSSL_PROVIDER_load(NULL, "legacy")` plus `"default"`.

The same `digital envelope routines::unsupported` error appears in Node.js 17+ webpack builds (webpack issue #14532);
that is a hashing problem in the build, not PKCS#12. Node has a `--openssl-legacy-provider` flag, but upgrading the
build tool is the better fix.

## Symptom 2: consumers reject OpenSSL 3 output
"The password is incorrect" on import or a MAC verification failure usually means the consumer can't handle
PBES2/AES or the SHA-256 MAC. Older Windows, macOS Keychain, JDK and appliance releases are the usual suspects; check
the consumer's documentation for the versions that support them.

Write the most compatible variant that still avoids RC2-40:
```
openssl pkcs12 -export -inkey k.pem -in c.pem -certfile chain.pem -out compat.pfx \
  -keypbe PBE-SHA1-3DES -certpbe PBE-SHA1-3DES -macalg sha1 -passout file:pw.txt
```
Only if that still fails, use `-legacy` (RC2-40 for certs, 3DES for keys). Treat these files as
transport-only: weak protection means the password and the file must not travel together, and
re-export after import isn't protected by them.

## Decide per consumer
Try the modern default first; if the target rejects it, try the compat command above; use `-legacy` only as the last
resort. Test on the real target; support depends on the consumer's version, so confirm it in the consumer's documentation.

Tested on OpenSSL 3.2.3 (the Windows build ships the legacy provider): `-legacy` export gives RC2-40 certificate bags
and a 3DES key bag with a SHA-1 MAC; reading it without `-legacy` fails with `unsupported ... RC2-40-CBC`; the compat
command gives 3DES for both bags.

## Long-term fix
Re-export legacy files once with modern settings after reading them, and upgrade consumers.
Keep the legacy provider out of production processes that don't need it, since loading it makes
weak algorithms fetchable application-wide.

## Verify
- [ ] Old files convert with `-legacy` and re-export with AES/SHA-256.
- [ ] The compat file imports on the target and `-info` shows 3DES, not RC2-40, where possible.
- [ ] Production configs do not load the legacy provider globally.
