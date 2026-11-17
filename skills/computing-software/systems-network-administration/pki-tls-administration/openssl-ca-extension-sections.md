---
id: computing-software.systems-network-administration.pki-tls-administration.openssl-ca-extension-sections
name: openssl-ca-extension-sections
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [openssl-ca-extension-sections, pki-openssl-ca, openssl, v3-extensions, ext-section, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Maintain separate extension sections for intermediate CA, server and client certificates in openssl.cnf and select them with -extensions."
sources:
  - https://docs.openssl.org/master/man5/x509v3_config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension sections per certificate type
Goal: one config, several certificate profiles without copy-paste mistakes.
```
[ v3_intermediate_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
[ server_ext ]
basicConstraints = CA:false
keyUsage = critical, digitalSignature
extendedKeyUsage = serverAuth
subjectAltName = @alt
authorityInfoAccess = OCSP;URI:http://ocsp.example.com
[ client_ext ]
basicConstraints = CA:false
keyUsage = critical, digitalSignature
extendedKeyUsage = clientAuth
[ alt ]
DNS.1 = app.example.com
```
Select with `-extensions server_ext` (with `-extfile file`, the section is read from that file instead of the main config). SANs differ per cert, so generate `alt` in a temporary extfile, or set `copy_extensions = copy` in the `openssl ca` config to take extensions from a vetted CSR. `openssl x509` and `openssl req -x509` also have a `-copy_extensions` option.
Gotcha: with `copy_extensions = copyall`, a CSR carrying `basicConstraints CA:TRUE` can hand the requester a valid CA certificate if nobody spots it. The manual's mitigation: use `copy`, which only adds extensions not already present, and put `basicConstraints = CA:FALSE` plus values for keyUsage and the like in the section so request values are ignored.
Verify:
- [ ] `openssl x509 -noout -text` shows CA:FALSE for leafs and CA:TRUE pathlen:0 for the intermediate.
- [ ] `openssl verify -purpose sslserver` accepts the server cert.

## Checked
2026-11-03. Confirmed in the x509v3_config and openssl-ca manual pages: basicConstraints with `pathlen` (zero means no sub-CAs), keyUsage names `keyCertSign` and `cRLSign`, extendedKeyUsage `serverAuth` and `clientAuth`, `subjectKeyIdentifier = hash`, the AKID `keyid` and `issuer` keywords with `always`, `authorityInfoAccess = OCSP;URI:...`, `@section` references for subjectAltName, `-extensions` and `-extfile` on `openssl ca`, the `copy_extensions` values none, copy and copyall and the WARNINGS text. Removed: `-copy_extensions copy` as an `openssl ca` flag (it is a config option there) and the claim that `copy` is SAN-only (it copies every extension not already present); code-signing from the description.
Method: documentation only; no commands were run.
