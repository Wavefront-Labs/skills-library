---
id: computing-software.cryptography-implementation.openssl.cross-signing-roots-and-intermediates
name: cross-signing-roots-and-intermediates
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, cross-signing, cross-certificate, openssl-ca, root-migration, chain-building]
level: advanced
status: docs-checked
description: "Cross-sign a new root or intermediate with OpenSSL so old trust stores accept it: same subject and key, issued by the old root, and verifying both paths."
sources: ["https://www.rfc-editor.org/rfc/rfc4158", "https://docs.openssl.org/3.0/man1/openssl-x509/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-signing roots and intermediates

A cross-certificate has the same subject and public key as the new CA certificate but is issued by an old,
widely trusted root. Clients that trust only the old root can build a path through it.

## Make one
```sh
# CSR from the new root's key and subject (-x509toreq needs -key for the self-signature)
openssl x509 -x509toreq -in newroot.pem -key newroot.key -copy_extensions copyall -out newroot.csr
# Issue from the old root, with CA extensions
openssl x509 -req -in newroot.csr -CA oldroot.pem -CAkey oldroot.key -CAcreateserial -days 1825 \
  -extfile ext.cnf -extensions v3_ca -out newroot-cross.pem
```
`ext.cnf` should set `basicConstraints=critical,CA:TRUE`, `keyUsage` and an `authorityKeyIdentifier` for the old
root. `-extfile` and `-extensions` choose the section the extensions come from.

## Serving chains
- Leaf, intermediate, then the cross-certificate (issued by the old root). Clients that trust the new root can stop
  earlier; clients that trust only the old root continue through the cross-certificate.
- Path-building behaviour differs between clients; test each client family you care about.

## Rules
- Keep the new root's self-signed certificate and the cross-certificate on identical subject and public key.

## Verify
- [ ] `openssl verify -CAfile oldroot.pem -untrusted chain.pem leaf.pem` and the same with `newroot.pem` both OK.

## Checked

2026-11-01. Confirmed in the OpenSSL openssl-x509 man page: `-x509toreq` (needs `-key`/`-signkey`), `-copy_extensions` with `copy`/`copyall`, `-req`, `-CA`, `-CAkey`, `-CAcreateserial`, `-days`, `-extfile`, `-extensions`; and in openssl-verification-options: `-CAfile`, `-untrusted`. Removed: the Let's Encrypt case study, OpenSSL-before-1.1.0 and old-Android path-building claims, Subject Key Identifier and validity-period rules, which were not confirmed.
Method: documentation only; no commands were run.
