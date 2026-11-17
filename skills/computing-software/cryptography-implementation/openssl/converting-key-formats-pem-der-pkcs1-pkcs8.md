---
id: computing-software.cryptography-implementation.openssl.converting-key-formats-pem-der-pkcs1-pkcs8
name: converting-key-formats-pem-der-pkcs1-pkcs8
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-pkey, genpkey, key-format-conversion, pkcs8, pkcs1, sec1, pem, der, openssh-keys]
level: practitioner
status: verified
description: "Convert private and public keys between PEM and DER, PKCS#1, SEC1, PKCS#8, SPKI and OpenSSH formats with openssl pkey/rsa and ssh-keygen, identifying each by header."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkey/", "https://docs.openssl.org/3.0/man1/openssl-pkcs8/", "https://www.rfc-editor.org/rfc/rfc7468", "https://man.openbsd.org/ssh-keygen"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting key formats (PEM, DER, PKCS#1, SEC1, PKCS#8, SPKI, OpenSSH)

Most "invalid key" errors are a format mismatch, not a bad key. Identify first, then convert.

## Identify by PEM label (RFC 7468)
| Label | Structure |
|---|---|
| `BEGIN PRIVATE KEY` | PKCS#8 unencrypted (any algorithm) |
| `BEGIN ENCRYPTED PRIVATE KEY` | PKCS#8 encrypted (PBES2) |
| `BEGIN RSA PRIVATE KEY` | PKCS#1 RSA ("traditional"); may carry `Proc-Type: 4,ENCRYPTED` |
| `BEGIN EC PRIVATE KEY` | SEC1 EC private key |
| `BEGIN PUBLIC KEY` | SubjectPublicKeyInfo (SPKI), any algorithm |
| `BEGIN RSA PUBLIC KEY` | PKCS#1 RSAPublicKey |
| `BEGIN OPENSSH PRIVATE KEY` | OpenSSH's own format (not ASN.1) |
DER has no label; `openssl asn1parse -inform DER -in k.der` shows the structure.

## Conversions with openssl 3.x
```
# anything -> PKCS#8 PEM (pkey's default output in 3.x)
openssl pkey -in in.key -out pkcs8.pem
# PKCS#8 -> traditional PKCS#1 / SEC1 (for old consumers)
openssl pkey -in pkcs8.pem -traditional -out rsa-pkcs1.pem
# PEM <-> DER
openssl pkey -in pkcs8.pem -outform DER -out key.der
openssl pkey -inform DER -in key.der -out key.pem
# public key out (SPKI)
openssl pkey -in key.pem -pubout -out pub.pem
# RSA SPKI -> PKCS#1 RSAPublicKey
openssl rsa -pubin -in pub.pem -RSAPublicKey_out -out rsapub.pem
```
In OpenSSL 3.x `openssl rsa` and `openssl pkey` emit PKCS#8 (`BEGIN PRIVATE KEY`) by default, but
`openssl ec` still writes SEC1 (`BEGIN EC PRIVATE KEY`); add `-traditional` to `rsa`/`pkey` when a
consumer insists on `BEGIN RSA PRIVATE KEY` or `BEGIN EC PRIVATE KEY`.

## OpenSSH
```
ssh-keygen -p -m PEM -f id_ecdsa        # rewrite private key in PEM (prompts for passphrase)
ssh-keygen -e -m PKCS8 -f id_ecdsa.pub > pub.pem      # OpenSSH pub -> SPKI PEM (RSA/ECDSA)
ssh-keygen -i -m PKCS8 -f pub.pem > id.pub            # SPKI PEM -> OpenSSH pub
ssh-keygen -y -f id_ed25519 > id_ed25519.pub          # derive public from private
```
`ssh-keygen -m PEM|PKCS8` handles RSA and ECDSA only. For Ed25519, OpenSSH 9.9p1 fails the public export with
`unsupported key type ED25519` and `-p -m PEM|PKCS8` silently leaves the key in `BEGIN OPENSSH PRIVATE KEY` form;
use a tool that reads OpenSSH keys (for example Python `cryptography`) to produce PKCS#8.

## Language consumers
- Java `PKCS8EncodedKeySpec` needs PKCS#8 DER; `X509EncodedKeySpec` needs SPKI DER.
- .NET `ImportPkcs8PrivateKey`, `ImportRSAPrivateKey` (PKCS#1), `ImportFromPem` (any label).
- Go `x509.ParsePKCS8PrivateKey`, `ParsePKCS1PrivateKey`, `ParseECPrivateKey`, `ParsePKIXPublicKey`.
- Web Crypto `importKey('pkcs8'|'spki'|'raw'|'jwk')`; no PKCS#1.

## Gotchas
- Windows line endings or a missing final newline break some PEM parsers; normalise.
- Never convert by stripping headers and re-adding different ones; the inner ASN.1 differs.
- Converting an encrypted key to unencrypted on disk is a security change; do it in memory or
  re-encrypt immediately.

## Verify
- [ ] The public-key SHA-256 (`openssl pkey -pubout -outform DER | openssl sha256`) is identical
      before and after conversion.
- [ ] The target consumer loads the file in a test.

## Checked
- OpenSSL 3.2.3 and OpenSSH 9.9p1 run in a scratch directory: every conversion above, each PEM label produced, `-traditional` for RSA and EC, encrypted PKCS#8 and `Proc-Type` traditional keys, public-key hash unchanged after conversion, `ssh-keygen -e/-i/-p/-y` for ECDSA and Ed25519.
- Node WebCrypto accepts PKCS#8 and SPKI DER and rejects PKCS#1 (`DataError`). Go `crypto/x509` Parse functions exist (`go doc`); the .NET `RSA.ImportFromPem`, `ImportPkcs8PrivateKey` and `ImportRSAPrivateKey` pages exist on Learn. Java `PKCS8EncodedKeySpec` (PrivateKeyInfo) and `X509EncodedKeySpec` (SubjectPublicKeyInfo) match the JDK 21 Javadoc.
