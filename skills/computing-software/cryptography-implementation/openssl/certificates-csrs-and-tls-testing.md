---
id: computing-software.cryptography-implementation.openssl.certificates-csrs-and-tls-testing
name: certificates-csrs-and-tls-testing
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-3, x509, certificates, csr, certificate-signing-request, san, subject-alt-name, self-signed, private-ca, genpkey, ed25519, ecdsa, p-256, rsa, s-client, tls, tls-testing, pem, der, pkcs12, pfx, legacy-provider, chain-verification, cert-expiry, key-cert-match]
level: practitioner
status: docs-checked
description: "OpenSSL 3 CLI recipes: generate Ed25519/P-256/RSA keys, CSRs with SANs, self-signed certs and a small CA, verify chains, test TLS with s_client, convert PEM/DER/PKCS#12."
sources: ["https://docs.openssl.org/master/man1/openssl-req/", "https://docs.openssl.org/master/man1/openssl-x509/", "https://docs.openssl.org/master/man1/openssl-s_client/", "https://docs.openssl.org/master/man1/openssl-pkcs12/", "https://www.rfc-editor.org/rfc/rfc5280"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSSL certificates, CSRs and TLS testing

**Goal:** produce correct keys, CSRs and certificates from the command line, and
diagnose a live TLS endpoint, with OpenSSL 3.x (check `openssl version`; 1.1.1 lacks
some flags below).

## 1. Generate a key
Use `genpkey` for every algorithm (the old `genrsa`/`ecparam` still work but differ per type):
```
openssl genpkey -algorithm ed25519 -out ed.key
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ec.key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out rsa.key
chmod 600 *.key
```
P-256 is a conservative default for web server certificates; check that every client you must support accepts
Ed25519 certificates before using them outside internal/mTLS. RSA 3072 if a legacy peer needs RSA.

## 2. Create a CSR with SANs
Put every hostname in subjectAltName and do not rely on the CN.
```
openssl req -new -key ec.key -out www.csr \
  -subj "/CN=www.example.com" \
  -addext "subjectAltName=DNS:www.example.com,DNS:example.com"
openssl req -in www.csr -noout -text -verify
```
For repeatable builds put the same in a config file (`[req]`, `distinguished_name`,
`req_extensions = v3_req`, `[v3_req] subjectAltName = @alt`) and pass `-config`.

## 3. Self-signed certificate and a small CA
Quick self-signed (default validity is only 30 days, so always set `-days`):
```
openssl req -x509 -new -key ec.key -days 365 -out self.pem \
  -subj "/CN=dev.local" -addext "subjectAltName=DNS:dev.local,IP:127.0.0.1"
```
Small internal CA:
```
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ca.key
openssl req -x509 -new -key ca.key -days 3650 -out ca.pem -subj "/CN=Example Internal CA" \
  -addext "basicConstraints=critical,CA:TRUE,pathlen:0" \
  -addext "keyUsage=critical,keyCertSign,cRLSign"
openssl x509 -req -in www.csr -CA ca.pem -CAkey ca.key -CAcreateserial \
  -days 90 -copy_extensions copy -out www.pem
```
`-copy_extensions` on `x509` is OpenSSL 3.0+; on 1.1.1 pass `-extfile leaf.cnf
-extensions v3_req` instead. Without either, the SANs from the CSR are silently
dropped. When signing CSRs you did not create, use an `-extfile` with only the
extensions you permit.

## 4. Inspect, check expiry, verify the chain
```
openssl x509 -in www.pem -noout -subject -issuer -dates -ext subjectAltName
openssl x509 -in www.pem -noout -text
openssl x509 -in www.pem -noout -checkend 2592000 && echo "valid for 30+ days"
openssl verify -CAfile ca.pem -untrusted intermediate.pem www.pem
```
`-checkend N` exits non-zero if the cert expires within N seconds, so you can use it in cron/CI.

## 5. Test a live TLS endpoint
```
openssl s_client -connect example.com:443 -servername example.com \
  -verify_return_error -verify_hostname example.com -showcerts </dev/null
openssl s_client -connect example.com:443 -servername example.com -tls1_3 </dev/null
openssl s_client -connect example.com:443 -servername example.com -alpn h2 -status </dev/null
```
Read `Verify return code`, `Protocol`, `Cipher`, ALPN and the chain. Without `-verify_return_error`, s_client
prints the verification failure and carries on anyway, which is easy to miss.
Pass `-servername` explicitly: without it s_client sets SNI from the name given to `-connect` only when that name has
DNS-name form, and an IP address connection may reach the default vhost's certificate.
Add `-CAfile ca.pem` for a private CA.

## 6. Convert formats
```
openssl x509 -in www.pem -outform DER -out www.der
openssl x509 -in www.der -inform DER -out www.pem
openssl pkcs12 -export -inkey ec.key -in www.pem -certfile chain.pem -out www.p12
openssl pkcs12 -in www.p12 -nodes -out all.pem      # 3.x: -noenc is the new name
```
**Legacy provider gotcha:** OpenSSL 3 encrypts new PKCS#12 files with AES-256-CBC and
PBKDF2, and older importers (older Windows and Java versions, some appliances) reject
them. Going the other way, reading an old `.p12`/`.pfx` that uses RC2-40 or 3DES fails
with an "unsupported" error. Add `-legacy` in both directions (it loads the legacy
provider). Which platform versions need this varies; test against the real consumer.

## 7. Does this key match this cert / CSR?
Compare public-key hashes; this works for every key type, unlike the old `-modulus` trick:
```
openssl pkey -in ec.key -pubout | openssl sha256
openssl x509 -in www.pem -noout -pubkey | openssl sha256
openssl req  -in www.csr -noout -pubkey | openssl sha256
```

## Gotchas
- Serve leaf first, then intermediates; leave the root out. A missing intermediate
  works in browsers that fetch it themselves and fails in curl, Java and mobile apps.
- Public CA certificate lifetimes are being shortened by the CA/Browser Forum (not covered by the OpenSSL docs; check the
  current schedule). Automate renewal (ACME).
- See `computing-software.cryptography-implementation.protocol-implementation.tls-integration-and-certificate-validation`
  for the client-side code.

## Verify
- [ ] `openssl x509 -noout -ext subjectAltName` lists every hostname the cert must serve.
- [ ] `openssl verify` returns `OK` for the full chain against the intended CA.
- [ ] `s_client -verify_return_error -verify_hostname` connects with return code 0.
- [ ] `-tls1_3` succeeds; protocols older than TLS 1.2 fail.
- [ ] Key, CSR and cert public-key hashes are identical.
- [ ] `-checkend` monitoring is in place for expiry.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in the req, x509, pkcs12 and s_client man pages: `req -x509 -days` and `x509 -days` both default to 30; `req -addext`; `x509 -req -copy_extensions copy` (extensions are ignored when the option is absent); `x509 -checkend` exits non-zero if the certificate expires within N seconds; `pkcs12` default encryption is AES-256-CBC with PBKDF2, `-noenc` and `-legacy` exist; `s_client -verify_return_error`, `-verify_hostname` and the SNI default. Removed unconfirmed claims about browser support for Ed25519 and the 47-day schedule.

Method: documentation only; no commands were run.
