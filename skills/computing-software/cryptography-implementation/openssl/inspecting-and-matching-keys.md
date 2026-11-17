---
id: computing-software.cryptography-implementation.openssl.inspecting-and-matching-keys
name: inspecting-and-matching-keys
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-pkey, genpkey, key-inspection, key-cert-match, spki-fingerprint, key-check]
level: practitioner
status: verified
description: "Inspect a key's type, size, curve and consistency with openssl pkey, and prove a key matches a certificate or CSR by comparing SPKI hashes and fingerprints."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkey/", "https://docs.openssl.org/3.0/man1/openssl-x509/", "https://www.rfc-editor.org/rfc/rfc7469#section-2.4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting and matching keys

## What is this key?
```
openssl pkey -in key.pem -noout -text | head -5     # "Private-Key: (3072 bit, 2 primes)" / curve
openssl pkey -in key.pem -noout -text_pub           # public part only
openssl pkey -pubin -in pub.pem -noout -text
openssl asn1parse -in key.pem                        # raw structure, algorithm OID
```
EC keys print `ASN1 OID: prime256v1` and `NIST CURVE: P-256`. Ed25519 shows `ED25519 Private-Key`.

## Is it internally consistent?
```
openssl pkey -in key.pem -check -noout       # private key consistency (RSA: p*q=n, d*e etc.)
openssl pkey -pubin -in pub.pem -pubcheck -noout   # public key validity (EC point on curve)
```
Run `-check` on keys received from outside or restored from backup to catch corruption.

## Does this key match that certificate / CSR?
Compare the SubjectPublicKeyInfo, which works for every algorithm:
```
openssl pkey -in key.pem -pubout -outform DER | openssl dgst -sha256
openssl x509 -in cert.pem -noout -pubkey | openssl pkey -pubin -outform DER | openssl dgst -sha256
openssl req  -in req.csr  -noout -pubkey | openssl pkey -pubin -outform DER | openssl dgst -sha256
```
Identical hashes mean a match. The older `-modulus | md5` trick only works for RSA.

## Fingerprints people ask for
```
# SPKI pin (base64 SHA-256), used by HPKP-style pinning and many mobile pinning libraries
openssl x509 -in cert.pem -noout -pubkey | openssl pkey -pubin -outform DER \
  | openssl dgst -sha256 -binary | openssl base64
# certificate fingerprint (hash of the whole cert DER)
openssl x509 -in cert.pem -noout -fingerprint -sha256
# Subject Key Identifier as stamped in the cert
openssl x509 -in cert.pem -noout -ext subjectKeyIdentifier
# SSH-style fingerprint
ssh-keygen -lf id_ed25519.pub
```
Know which one a system wants: a cert fingerprint changes on every renewal, an SPKI pin only
changes when the key changes.

## Matching across a directory
```
for f in *.pem; do printf '%s ' "$f"; openssl x509 -in "$f" -noout -pubkey 2>/dev/null \
  | openssl pkey -pubin -outform DER | openssl dgst -sha256 -r | cut -c1-16; done
```
Useful after a messy renewal when nobody knows which key belongs to which cert.

## Gotchas
- `openssl pkey -text` prints the private components to the terminal; don't paste it into tickets.
- A PKCS#12 must be unpacked first (`openssl pkcs12 -in f.p12 -nokeys` / `-nocerts`).
- HSM-held keys: export the public key from the token with your vendor's tool and compare its SPKI hash with the cert's.

## Checked
Run with OpenSSL 3.2.3 and OpenSSH on 2026-10-18 using a freshly generated RSA-3072 key, certificate and CSR, plus EC P-256 and Ed25519 keys: `pkey -text` prints `Private-Key: (3072 bit, 2 primes)`, `-text_pub` and `-pubin -text` print `Public-Key: (3072 bit)`, `-check` and `-pubcheck` print `Key is valid`, the three SPKI SHA-256 hashes (key, certificate, CSR) were identical, the SPKI pin pipeline, `x509 -fingerprint -sha256`, `-ext subjectKeyIdentifier` and `ssh-keygen -lf` all ran, EC output shows `ASN1 OID: prime256v1` and `NIST CURVE: P-256`, and Ed25519 shows `ED25519 Private-Key`. RFC 7469 defines an SPKI fingerprint as a hash of the DER SPKI, base64-encoded. The RSA-only `-modulus | md5` comparison is likewise RSA-specific.

## Verify
- [ ] Key/cert/CSR SPKI hashes match before deploying a renewed cert.
- [ ] `-check` passes on imported keys.
- [ ] Pins in clients are SPKI hashes, with a backup pin for the next key.
