---
id: computing-software.cryptography-implementation.openssl.x509v3-extension-configuration
name: x509v3-extension-configuration
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, x509, csr, x509v3-extensions, basic-constraints, key-usage, extended-key-usage, authority-key-identifier]
level: advanced
status: docs-checked
description: "Configure x509v3 extensions correctly for CA, server, client and code-signing certs: basicConstraints, keyUsage, EKU, SKI/AKI, CDP, AIA and criticality."
sources: ["https://docs.openssl.org/master/man5/x509v3_config/", "https://docs.openssl.org/master/man1/openssl-ca/", "https://docs.openssl.org/master/man1/openssl-x509/", "https://docs.openssl.org/master/man1/openssl-verification-options/", "https://www.rfc-editor.org/rfc/rfc5280"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# x509v3 extension configuration

Extensions decide what a certificate is allowed to do. Wrong ones cause either outages
(clients reject it) or security holes (a leaf that can sign other certs).

## Profiles (put in an extfile and pass `-extfile f.cnf -extensions <section>`)
```
[root_ca]
basicConstraints       = critical, CA:TRUE
keyUsage               = critical, keyCertSign, cRLSign
subjectKeyIdentifier   = hash

[issuing_ca]
basicConstraints       = critical, CA:TRUE, pathlen:0
keyUsage               = critical, keyCertSign, cRLSign
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always
crlDistributionPoints  = URI:http://pki.example.com/root.crl
authorityInfoAccess    = caIssuers;URI:http://pki.example.com/root.crt

[server]
basicConstraints       = critical, CA:FALSE
keyUsage               = critical, digitalSignature
extendedKeyUsage       = serverAuth
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always
subjectAltName         = ${ENV::SAN}
crlDistributionPoints  = URI:http://pki.example.com/issuing.crl
authorityInfoAccess    = OCSP;URI:http://ocsp.example.com, caIssuers;URI:http://pki.example.com/issuing.crt

[client]
basicConstraints = critical, CA:FALSE
keyUsage         = critical, digitalSignature
extendedKeyUsage = clientAuth

[codesign]
basicConstraints = critical, CA:FALSE
keyUsage         = critical, digitalSignature
extendedKeyUsage = codeSigning
```
Sign with `openssl x509 -req -in r.csr -CA ca.pem -CAkey ca.key -extfile ext.cnf -extensions server
-days 90 -out leaf.pem` (or the same `-extensions` with `openssl ca`).

## Field-by-field rules
- **basicConstraints**: always critical on CAs; `pathlen:0` on issuing CAs so they cannot mint
  sub-CAs. Leaves get `CA:FALSE`.
- **keyUsage**: the defined values are digitalSignature, nonRepudiation (contentCommitment), keyEncipherment,
  dataEncipherment, keyAgreement, keyCertSign, cRLSign, encipherOnly and decipherOnly. Under `-purpose sslserver` a
  target certificate's keyUsage must allow digitalSignature, keyEncipherment and/or keyAgreement, so `digitalSignature`
  alone suffices for ECDSA TLS leaves; add `keyEncipherment` only for RSA key exchange you want to keep. CA certificates
  use `keyCertSign` and `cRLSign`.
- **extendedKeyUsage**: prefer one purpose per certificate and issue separate client certificates. With
  `-purpose sslserver` any EKU present must allow serverAuth (and `sslclient` clientAuth); how verifiers treat EKU on
  intermediates differs, so test with your own clients.
- **SKI/AKI**: `subjectKeyIdentifier = hash` uses the SHA-1 hash of the public key; `authorityKeyIdentifier = keyid:always`
  makes the issuer's key identifier mandatory. With `-x509_strict`, the AKI must be present on X.509v3 certificates
  (unless apparently self-signed) and the SKI on all CA certificates.
- **CDP / AIA**: `crlDistributionPoints = URI:...`; `authorityInfoAccess` takes `OCSP;URI:...` and
  `caIssuers;URI:...` entries.
- **Criticality**: write `critical,` before the value to mark an extension critical; a verifier that does not understand
  a critical extension must reject the certificate (RFC 5280). Mark basicConstraints and keyUsage on CAs critical.

## Copying from the CSR safely
`-copy_extensions copy` (x509) or `copy_extensions = copy` (ca) copies request extensions into the certificate; in
`ca`, `copy` only adds extensions not already present and `copyall` deletes a present one first and takes the request's.
Use `copy` only when the profile sets basicConstraints (with `CA:FALSE`) and keyUsage itself: with `copyall` a request
containing `CA:TRUE` can hand the requester a valid CA certificate (see the WARNINGS section of openssl-ca(1)).

## Inspect the result
```
openssl x509 -in leaf.pem -noout -ext basicConstraints,keyUsage,extendedKeyUsage,subjectAltName
openssl x509 -in leaf.pem -noout -purpose
```

## Verify
- [ ] Leaves show `CA:FALSE`; issuing CAs show `pathlen:0`.
- [ ] `-purpose` reports Yes only for the intended purpose.
- [ ] Chain verifies with `openssl verify -purpose sslserver` (or `sslclient`).

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in x509v3_config(5) (`critical` prefix, basicConstraints and pathlen syntax, keyUsage value list, `codeSigning` EKU name, `subjectKeyIdentifier = hash` meaning, `keyid:always`, authorityInfoAccess `OCSP;URI`/`caIssuers;URI`, crlDistributionPoints syntax), openssl-ca(1) (`copy_extensions` copy and copyall behaviour and the CA:TRUE warning), openssl-x509(1) (`-copy_extensions`, `-ext`, `-purpose`, `-extfile`/`-extensions`) and openssl-verification-options(1) (`sslserver` and `sslclient` purpose checks, `-x509_strict` AKI/SKI rules). Removed unchecked claims about public CA direction, Windows and Go EKU enforcement, chain-building failures from missing AKI and the reason for HTTP-only CDP/AIA URLs.

Method: documentation only; no commands were run.
