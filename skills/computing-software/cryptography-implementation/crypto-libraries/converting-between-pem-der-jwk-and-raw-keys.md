---
id: computing-software.cryptography-implementation.crypto-libraries.converting-between-pem-der-jwk-and-raw-keys
name: converting-between-pem-der-jwk-and-raw-keys
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, interoperability, jwk-pem-conversion, jwk, pem, der, spki, pkcs8]
level: practitioner
status: verified
description: "Convert keys between PEM, DER, JWK and raw bytes: SPKI/PKCS8 structure, JWK field encodings for RSA, EC and OKP, thumbprints, and tools that do it safely."
sources: ["https://www.rfc-editor.org/rfc/rfc7468", "https://www.rfc-editor.org/rfc/rfc7517", "https://www.rfc-editor.org/rfc/rfc7518#section-6", "https://www.rfc-editor.org/rfc/rfc8037", "https://www.rfc-editor.org/rfc/rfc7638"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting between PEM, DER, JWK and raw keys

## The formats
- **DER**: binary ASN.1. Public keys as SubjectPublicKeyInfo (SPKI), private keys as PKCS#8
  (RFC 5958). Legacy: PKCS#1 `RSAPublicKey`/`RSAPrivateKey`, SEC1 `ECPrivateKey`.
- **PEM** (RFC 7468): base64 DER between labels. The label tells you the structure:
  `PUBLIC KEY` = SPKI, `PRIVATE KEY` = PKCS#8, `ENCRYPTED PRIVATE KEY` = PKCS#8 PBES2,
  `RSA PRIVATE KEY` / `EC PRIVATE KEY` = legacy.
- **JWK** (RFC 7517/7518/8037): JSON, every integer/octet field base64url without padding.
- **Raw**: bare bytes - EC points (SEC1 `0x04||X||Y`), 32-byte Ed25519/X25519 keys.

## JWK fields
| kty | public | private |
|---|---|---|
| RSA | `n`, `e` (big-endian, no leading zero) | `d`, `p`, `q`, `dp`, `dq`, `qi` |
| EC (`crv` P-256/384/521) | `x`, `y` (fixed field length: 32/48/66 bytes, left-padded) | `d` (same length) |
| OKP (`crv` Ed25519/X25519) | `x` (raw 32 bytes) | `d` (raw 32-byte seed) |

Common bugs: dropping leading zero bytes from EC `x`/`y`/`d` (fails one time in 256: 3 of 955 generated P-256 keys had an `x` starting
with 0x00, and Node still emitted a 32-byte, 43-character `x`), keeping the ASN.1 sign byte on RSA `n`, using standard base64 with `+/=`.
Node 24.22 exports: EC private `kty,x,y,crv,d`; RSA private `kty,n,e,d,p,q,dp,dq,qi` (`e` = `AQAB`); Ed25519 `kty:OKP,crv,x,d` with a
32-byte `d` (all run).

## Doing it in code (prefer library calls to hand-rolled ASN.1)
- Node: `crypto.createPublicKey(pem).export({format: "jwk"})`; reverse with
  `createPublicKey({key: jwk, format: "jwk"}).export({type: "spki", format: "pem"})` (byte-identical PEM round trip, run).
  PEM labels from `export`: `{type:"pkcs8"}` gives `PRIVATE KEY`, `sec1` gives `EC PRIVATE KEY`, `pkcs1` gives `RSA PRIVATE KEY`, and a
  PKCS#8 export with `cipher` and `passphrase` gives `ENCRYPTED PRIVATE KEY` (all run).
- Web Crypto: `importKey("spki"|"pkcs8"|"jwk"|"raw", ...)` then `exportKey` to another format
  (key must be extractable: a non-extractable key threw `key is not extractable`; an EC public `raw` export was 65 bytes starting 0x04; the
  JWK export also carries `key_ops` and `ext`, so strip them if you hash or publish the JWK).
- Python: `jwcrypto.jwk.JWK.from_pem(pem)` / `.export_to_pem()` (jwcrypto 1.6.1; the exported PEM equals the `openssl` PEM apart from
  line endings, and the JWK gains a `kid` that is the RFC 7638 thumbprint); `export(private_key=False)` omitted `d`; or pyca + manual
  base64url of `public_numbers()`.
- Go: `x509.ParsePKIXPublicKey` / `MarshalPKIXPublicKey` (run; an X25519 SPKI parses to `*ecdh.PublicKey`); `github.com/go-jose/go-jose/v4`
  `JSONWebKey` for JWK (type exists on pkg.go.dev; not run).
- Java: `KeyFactory` with `X509EncodedKeySpec` (SPKI) and `PKCS8EncodedKeySpec` (both classes are in the Java 21 API docs); the Nimbus JOSE
  library has PEM-parsing helpers on its `JWK` classes (check its Javadoc for the current method names). Not run: no JDK 11+ here.
- CLI: `openssl pkey -in k.pem -pubout -outform DER`; `openssl pkey -in legacy.pem -out pkcs8.pem`
  converts traditional to PKCS#8 (OpenSSL 3.2.3: a `BEGIN EC PRIVATE KEY` file became `BEGIN PRIVATE KEY`; the P-256 SPKI DER was 91 bytes).

## Thumbprints and kid
RFC 7638 thumbprint = SHA-256 over the required members only, lexicographically ordered, no
whitespace (`{"crv":..,"kty":..,"x":..,"y":..}` for EC), base64url encoded. Use it as a stable `kid`. A hand-built hash of that string
matched jwcrypto's `thumbprint()` for a P-256 key.

## Safety
- Never paste private keys into web converters.
- After converting, compare public keys: SPKI DER bytes or JWK thumbprint must match.
- Strip private members (`d`, `p`, `q`...) before publishing a JWKS; libraries' "public" export
  does this, `JSON.stringify(privateJwk)` does not.

## Verify
- [ ] Round trip PEM -> JWK -> PEM yields byte-identical SPKI.
- [ ] Tests include EC keys whose coordinates start with 0x00.
- [ ] Published JWKS contains no private members.
