---
id: computing-software.cryptography-implementation.openssl.pkcs12-friendlyname-and-local-key-id
name: pkcs12-friendlyname-and-local-key-id
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, pkcs12-friendlyname, pkcs12, local-key-id, keystore-alias, openssl-pkcs12]
level: practitioner
status: docs-checked
description: "Set friendlyName in PKCS#12 files with openssl pkcs12: -name for the key and certificate, -caname for chain certificates, and inspecting bag attributes."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkcs12/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKCS#12 friendlyName

## Set it
```sh
openssl pkcs12 -export -inkey key.pem -in cert.pem -certfile chain.pem \
  -name "api-server" -caname "Example Issuing CA" -caname "Example Root" -out bundle.p12
```
- `-name` sets the "friendly name" for the certificates and private key; importing software typically shows it in list
  boxes.
- `-caname` sets the friendly name for other certificates; it may be repeated, one per certificate, in order.
- `-certfile` adds extra certificates to the output when exporting.

## Inspect
```sh
openssl pkcs12 -in bundle.p12 -info -noout
```
`-info` outputs extra information about the file structure, algorithms and iteration counts; `-nokeys` suppresses
private keys in the output. Keystore tools may use the friendly name as an alias, so set `-name` deliberately and
check how your target tool lists it.

## Verify
- [ ] Inspecting the file shows the intended friendly names on the key and certificates.
- [ ] The consuming tool lists the entry under the expected name.

## Checked

2026-11-01. Confirmed in the OpenSSL openssl-pkcs12 man page: `-export`, `-name`, `-caname` (repeatable, in order), `-certfile`, `-info`, `-nokeys`, `-noout`. Removed: localKeyID details, Java keytool and Windows behaviour claims (default alias, lowercasing, thumbprint binding), which that page does not cover.
Method: documentation only; no commands were run.
