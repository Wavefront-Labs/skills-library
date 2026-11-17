---
id: computing-software.systems-network-administration.pki-tls-administration.openssl-csr-with-san
name: openssl-csr-with-san
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [openssl-csr-with-san, pki-openssl-csr, openssl, req, csr, addext, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Create a certificate signing request with subjectAltName and extensions using openssl req, without a config file, and inspect it before sending."
sources:
  - https://docs.openssl.org/master/man1/openssl-req/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSSL CSR with SAN
Goal: a CSR the CA signs with the right names.
```
openssl req -new -key leaf.key -out leaf.csr \
  -subj "/O=Example Corp/CN=app.example.com" \
  -addext "subjectAltName=DNS:app.example.com,DNS:app" \
  -addext "extendedKeyUsage=serverAuth"
openssl req -in leaf.csr -noout -text -verify
```
- `-addext` takes a key=value pair as it would appear in a config file; each extension may appear once and the command line overrides the config. For a reusable list, put a section in a config and name it with `req_extensions`.
- One-liner keypair: `openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:P-256 -noenc -keyout k.pem -out r.csr` (`-noenc` leaves the key unencrypted; `-nodes` is the deprecated name for it since OpenSSL 3.0).
- The CA may ignore requested extensions; the issued cert is authoritative.
Gotcha: `-x509` makes `req` output a certificate instead of a request; do not send it to a CA. With `-x509`, `-days` sets the lifetime (default 30 days).
Verify:
- [ ] `openssl req -in leaf.csr -noout -text -verify` lists the SAN; `-verify` checks the request's self-signature and exits on failure.
- [ ] CSR public key hash equals the key: compare `openssl req -pubkey -noout -in leaf.csr | sha256sum` with `openssl pkey -pubout -in leaf.key | sha256sum`.

## Checked
2026-11-03. Confirmed in the openssl-req, openssl-genpkey and openssl-pkey manual pages: `-new`, `-key`, `-subj`, `-addext` (key=value, once per extension, overrides config), `req_extensions`, `-verify`, `-pubkey`, `-newkey`, `-pkeyopt` with `ec_paramgen_curve` and the curve name `P-256`, `-noenc` and the deprecated `-nodes`, `-x509`, `-days` default 30, `-pubout`. Removed: the OpenSSL 1.1.1 version claim for `-addext` (not on the page), the `verify OK` output string. The CA-may-ignore-extensions point is the `copy_extensions = none` behaviour on the openssl-ca page.
Method: documentation only; no commands were run.
