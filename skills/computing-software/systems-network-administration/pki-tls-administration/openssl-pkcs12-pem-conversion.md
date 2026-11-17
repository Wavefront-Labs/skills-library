---
id: computing-software.systems-network-administration.pki-tls-administration.openssl-pkcs12-pem-conversion
name: openssl-pkcs12-pem-conversion
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [openssl-pkcs12-pem-conversion, pki-openssl-tools, openssl, pkcs12, pem, der, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Convert certificates and keys between PEM, DER and PKCS#12 with openssl, and export a PFX with the full chain."
sources:
  - https://docs.openssl.org/master/man1/openssl-pkcs12/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PEM, DER and PKCS#12 conversion
Goal: get the format each platform wants.
```
openssl x509 -in c.pem -outform DER -out c.der
openssl pkcs12 -export -inkey k.key -in c.pem -certfile chain.pem -name app -out app.p12
openssl pkcs12 -in app.p12 -nokeys -clcerts -out c.pem
openssl pkcs12 -in app.p12 -nocerts -noenc -out k.key
```
- Current OpenSSL encrypts new PKCS#12 files with AES-256-CBC and PBKDF2 by default. Older importers may need `-legacy` or explicit `-keypbe`, `-certpbe` and `-macalg` values; the openssl-pkcs12 page lists them. Test each target.
- `-noenc` writes the key unencrypted (`-nodes` is its deprecated name since OpenSSL 3.0); `-clcerts` outputs only client certificates.
- Supply the output password via `-passout file:pw.txt`.
Gotcha: forgetting `-certfile chain.pem` exports only the leaf; the importing server then sends an incomplete chain.
Verify:
- [ ] `openssl pkcs12 -in app.p12 -info -nokeys` shows the file structure, algorithms and the certificates it holds.

## Checked
2026-11-03. Confirmed in the openssl-pkcs12 manual page: `-export`, `-inkey`, `-certfile` (extra certificates added with `-export`), `-name`, `-nokeys`, `-nocerts`, `-clcerts`, `-noenc`, deprecated `-nodes`, `-passout`, `-info`, `-legacy`, `-keypbe`, `-certpbe`, `-macalg`, default AES-256-CBC with PBKDF2. Removed: `crl2pkcs7` and PKCS#7 (no page fetched), the Java 8u301 and old Windows claims, specific PBE-SHA1-3DES values and the `-noout` flag.
Method: documentation only; no commands were run.
- [ ] Target system imports it and the key pairs with the cert.
