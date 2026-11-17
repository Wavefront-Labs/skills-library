---
id: computing-software.cryptography-implementation.applied-cryptography.rsa-oaep-parameter-selection
name: rsa-oaep-parameter-selection
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, rsa-oaep, oaep-parameters, mgf1, rsa-encryption, interoperability, sp-800-56b, rfc8017, key-transport]
level: advanced
status: docs-checked
description: "Configure RSA-OAEP so both sides agree: OAEP hash vs MGF1 hash defaults per library, label usage, max plaintext size, and using it only to transport a symmetric key."
sources: ["https://datatracker.ietf.org/doc/html/rfc8017#section-7.1", "https://csrc.nist.gov/pubs/sp/800/56/b/r2/final", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/spec/OAEPParameterSpec.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RSA-OAEP parameter selection

RSA-OAEP (PKCS#1 v2.2, SP 800-56B "RSA-OAEP" key transport) is the only RSA
encryption padding to use. Use it to encrypt a random symmetric key, not
application data.

## Three parameters both sides must match

1. **OAEP hash** (hashes the label): SHA-256 is the sane default.
2. **MGF1 hash**: usually the same as the OAEP hash, but libraries disagree on
   defaults.
3. **Label** (`L`, often empty): optional context binding; a mismatch fails decryption.

Defaults differ between libraries and are the source of most interop bugs. Set both hashes explicitly everywhere:

| Library | Call | Note |
|---|---|---|
| Java | `new OAEPParameterSpec("SHA-256","MGF1",MGF1ParameterSpec.SHA256,PSource.PSpecified.DEFAULT)` | `OAEPParameterSpec.DEFAULT` is SHA-1 with MGF1-SHA1; the Javadoc recommends building your own spec |
| OpenSSL | `EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_OAEP_PADDING)` then `EVP_PKEY_CTX_set_rsa_oaep_md` and `EVP_PKEY_CTX_set_rsa_mgf1_md` | the OAEP digest and the MGF1 digest are set by separate calls |
| .NET | `RSAEncryptionPadding.OaepSHA256` | OAEP with SHA-256 |
| Go | `rsa.EncryptOAEP(sha256.New(), rand.Reader, pub, msg, label)` | one hash; `OAEPOptions.MGFHash` (with `EncryptOAEPWithOptions`, go1.26) when MGF1 must differ |

Pass the full parameter spec explicitly in Java; do not rely on a transformation string or `DEFAULT`.

```bash
openssl pkeyutl -encrypt -pubin -inkey pub.pem -in key.bin -out key.enc \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256
```

## Size limit

Max plaintext = k - 2*hLen - 2 bytes (RFC 8017), where k is modulus bytes and hLen the hash
output length. RSA-2048 with SHA-256: 256 - 64 - 2 = 190 bytes. That is why you encrypt a 32-byte AES key
and then use AES-GCM for the data (hybrid encryption; consider HPKE instead of
inventing the framing).

## Decryption errors

Return one generic error for any OAEP failure and do not distinguish "decoding
error" from later application errors; RFC 8017 warns that leaking the failure point
through error messages or timing enables Manger's attack. Use the library's OAEP decode;
do not unpad yourself.

## Verify

- [ ] OAEP hash, MGF1 hash and label written into the protocol spec.
- [ ] Cross-library round-trip test (e.g. Java encrypt, Go/OpenSSL decrypt).
- [ ] Payload is a symmetric key <= size limit, not raw data.
- [ ] Test vectors for your stack (for example Wycheproof RSA-OAEP files) pass.

## Checked

2026-10-31. Confirmed: RFC 8017 section 7.1 (max message length k - 2hLen - 2, Manger attack and error/timing
warning); Oracle `OAEPParameterSpec` Javadoc (DEFAULT is SHA-1 and MGF1ParameterSpec.SHA1; recommends the explicit
constructor); OpenSSL 3.0 `EVP_PKEY_CTX_ctrl` (separate OAEP and MGF1 digest setters, label setter) and `openssl-pkeyutl`
(`rsa_padding_mode:oaep`, `rsa_oaep_md`, `rsa_mgf1_md`); Go `crypto/rsa` (EncryptOAEP takes one hash, `OAEPOptions.MGFHash`,
`EncryptOAEPWithOptions` added in go1.26); .NET `RSAEncryptionPadding.OaepSHA256`. Removed as unconfirmed: the SunJCE
MGF1-SHA1 behaviour of the SHA-256 transformation string, OpenSSL and pyca default digests, and the Web Crypto row.
Method: documentation only; no commands were run.
