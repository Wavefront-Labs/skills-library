---
id: computing-software.cryptography-implementation.openssl.reissuing-with-x509toreq
name: reissuing-with-x509toreq
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, x509toreq, openssl-x509, csr, certificate-renewal, copy-extensions]
level: practitioner
status: verified
description: "Re-issue a certificate from an existing cert and key with openssl x509 -x509toreq: copying subject and extensions, re-keying variant, and checking the new CSR."
sources: ["https://docs.openssl.org/3.0/man1/openssl-x509/", "https://docs.openssl.org/3.0/man1/openssl-req/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Re-issuing with x509 -x509toreq

## Same key, same subject
```sh
openssl x509 -x509toreq -in old.pem -signkey key.pem -out renew.csr
openssl x509 -x509toreq -in old.pem -key key.pem -copy_extensions copyall -out renew.csr   # OpenSSL 3
```
Without `-copy_extensions` (3.0+; `copy` and `copyall` behave the same here), extensions such as subjectAltName are
dropped from the CSR (tested on 3.2.3: 0 SANs without it, all three with it). The manual says `-key` (or `-signkey`)
is required; the public key in the CSR is the one from that key.

## New key, same subject and SANs
```sh
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out new.key
openssl x509 -x509toreq -in old.pem -key new.key -copy_extensions copyall -out renew.csr
```
x509toreq takes the subject from the cert but signs the CSR (and sets the public key) from `-key` (tested: the CSR's
public key matched `new.key`, not the old certificate's key; subject key and authority key identifiers are not copied).

## Alternative with req
```sh
openssl req -new -key new.key -subj "$(openssl x509 -in old.pem -noout -subject -nameopt compat | sed 's/^subject=//')" \
  -addext "subjectAltName=$(openssl x509 -in old.pem -noout -ext subjectAltName | tail -1 | sed 's/IP Address:/IP:/g; s/ //g')" -out renew.csr
```

The `sed` matters: `x509 -ext` prints `IP Address:`, and stripping the space gives `IPAddress:`, which `-addext` rejects
(`unsupported option`); the `IP:` form was accepted.

## Check before submitting
```sh
openssl req -in renew.csr -noout -text -verify
```
Look for `verify OK`, the right public key, and SANs under Requested Extensions.

## Pitfalls
- Copying stale extensions (old OCSP/AIA, basicConstraints) into a CSR for a public CA; most CAs ignore them,
  private CAs with `copy_extensions = copyall` will issue them. Strip with a fresh `req` when unsure.

## Verify
- [ ] New certificate's SANs and key match expectations; old key retired if re-keyed.
