---
id: computing-software.cryptography-implementation.openssl.inspecting-certificate-fields-and-fingerprints
name: inspecting-certificate-fields-and-fingerprints
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, x509, csr, certificate-inspection, fingerprint, cert-expiry, pem-bundle, openssl-x509]
level: practitioner
status: verified
description: "Inspect certificates with openssl x509 and storeutl: subject/issuer, serial, validity, extensions, fingerprints, hashes, and every cert in a bundle or live endpoint."
sources: ["https://docs.openssl.org/3.0/man1/openssl-x509/", "https://docs.openssl.org/3.0/man1/openssl-storeutl/", "https://docs.openssl.org/3.0/man1/openssl-namedisplay-options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting certificate fields and fingerprints

## The fields people actually need
```
openssl x509 -in cert.pem -noout -subject -issuer -serial -dates -nameopt RFC2253
openssl x509 -in cert.pem -noout -ext subjectAltName,keyUsage,extendedKeyUsage,basicConstraints
openssl x509 -in cert.pem -noout -fingerprint -sha256
openssl x509 -in cert.pem -noout -ocsp_uri
openssl x509 -in cert.pem -noout -text            # everything
```
DER input: add `-inform DER`. `-nameopt RFC2253` (or `oneline`, `multiline`, `utf8`) gives a
stable, greppable DN; the default output varies between versions.

## Expiry in scripts
```
openssl x509 -in cert.pem -noout -enddate          # notAfter=Jan  1 00:00:00 2027 GMT
openssl x509 -in cert.pem -noout -checkend 1209600 || echo "expires within 14 days"
```
`-checkend` uses the exit code, so monitoring needs no date parsing.

## Bundles: show every certificate, not just the first
`openssl x509` reads only the first PEM block. For a chain file or CA bundle:
```
openssl storeutl -noout -text -certs chain.pem | grep -E "^[0-9]+: Certificate|Subject:|Issuer:|Not After"
# 1.1.1 fallback
openssl crl2pkcs7 -nocrl -certfile chain.pem | openssl pkcs7 -print_certs -noout
# split into files
awk '/BEGIN CERT/{n++} {print > ("cert" n ".pem")}' chain.pem
```

## Live endpoints
```
openssl s_client -connect host:443 -servername host -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```
That reads the leaf; use `-showcerts` plus the split above to inspect intermediates.

## Hashes and identifiers
- `-fingerprint -sha256`: hash of the full DER cert; what most UIs and pinning-by-cert show.
  Avoid SHA-1 fingerprints for identification.
- `-hash` / `-issuer_hash`: OpenSSL's subject-name hash used for `c_rehash` directory lookups
  (`<hash>.0` symlinks).
- `-ext subjectKeyIdentifier,authorityKeyIdentifier`: match a leaf's AKI to its issuer's SKI to find
  the right intermediate.
- `-serial`: needed for revocation requests and CA database lookups.

## Reading -text output carefully
- `Signature Algorithm` appears twice: the first under `Certificate:` is what the issuer used.
- `Public-Key: (256 bit)` with `ASN1 OID: prime256v1` = P-256.
- Unknown extensions print as hex; `openssl asn1parse -in cert.pem -i` shows the raw tree.
- Precertificate poison or embedded SCT lists indicate CT logging (public certs).

## Gotchas
- Tested on OpenSSL 3.2.3 with a local test chain and a live `s_client | x509 -ext` pipeline; `-checkend` exits 1 with
  `Certificate will expire` and 0 with `Certificate will not expire`.
- Windows `.cer` may be PEM or DER; check the first bytes (`-----BEGIN` vs `0x30 0x82`).
- PKCS#7 `.p7b` holds certs only: `openssl pkcs7 -in f.p7b -print_certs -out certs.pem`.
- Validity times are UTC; `notBefore` in the future breaks clients with skewed clocks.

## Verify
- [ ] Monitoring uses `-checkend` (or equivalent) on every deployed cert, including intermediates.
- [ ] Every cert in a bundle was inspected, not only the first.
