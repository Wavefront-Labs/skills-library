---
id: computing-software.cryptography-implementation.crypto-libraries.rsa-oaep-parameter-interop
name: rsa-oaep-parameter-interop
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, oaep-interop, rsa-oaep, interop, oaepparameterspec, mgf1, java, openssl, web-crypto, dotnet, nodejs]
level: practitioner
status: verified
description: "Fix RSA-OAEP interop failures: Java's SHA-1 MGF1 default, OpenSSL rsa_oaep_md and rsa_mgf1_md, WebCrypto, .NET, Node and pyca parameter matching and labels."
sources: ["https://www.rfc-editor.org/rfc/rfc8017#section-7.1", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/spec/OAEPParameterSpec.html", "https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/com/sun/crypto/provider/RSACipher.java", "https://docs.openssl.org/3.0/man1/openssl-pkeyutl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RSA-OAEP parameter interop

OAEP has three parameters: the label hash, the MGF1 hash, and the label (usually empty). Libraries pick different
defaults, and a mismatch produces a generic "decryption error".

## Defaults
| Library | Call | Label hash | MGF1 hash |
|---|---|---|---|
| Java SunJCE | `RSA/ECB/OAEPWithSHA-256AndMGF1Padding` | SHA-256 | **SHA-1** |
| Java with spec | `OAEPParameterSpec("SHA-256","MGF1",MGF1ParameterSpec.SHA256,PSource.PSpecified.DEFAULT)` | SHA-256 | SHA-256 |
| OpenSSL | default OAEP | SHA-1 | SHA-1 (a Node default ciphertext decrypted with `pkeyutl` defaults) |
| OpenSSL | `-pkeyopt rsa_oaep_md:sha256` | SHA-256 | SHA-256 (follows oaep_md unless `rsa_mgf1_md` set) |
| Web Crypto | `{name:"RSA-OAEP"}` with key `hash:"SHA-256"` | SHA-256 | SHA-256 (Node `crypto.subtle` output decrypted by `pkeyutl` with `rsa_oaep_md:sha256` only) |
| .NET | `RSAEncryptionPadding.OaepSHA256` | SHA-256 | confirm in a cross-test (the API docs name one hash; not run, no .NET SDK) |
| Node | `publicEncrypt({key, padding: RSA_PKCS1_OAEP_PADDING, oaepHash:"sha256"})` | SHA-256 | SHA-256 (decrypted by `pkeyutl` with only `rsa_oaep_md:sha256`; without `oaepHash` Node uses SHA-1 for both) |
| pyca | `padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)` | explicit | explicit (decrypted the Node SHA-256 ciphertext; MGF1 SHA-1 raised `Decryption failed`) |

The Java row is the classic trap: "OAEPWithSHA-256AndMGF1Padding" does not mean MGF1-SHA-256 in SunJCE (other providers may differ, so pass the spec explicitly). OpenJDK's `RSACipher.java` builds the spec as `new OAEPParameterSpec(oaepHashAlgorithm, "MGF1", MGF1ParameterSpec.SHA1, PSource.PSpecified.DEFAULT)` when none is passed, and a Java 8 ciphertext from that transformation failed `openssl pkeyutl` with `rsa_oaep_md:sha256` alone and decrypted only with `-pkeyopt rsa_mgf1_md:sha1` added.

## Java fix (run on Java 8 via jjs; the ciphertext decrypted with `openssl pkeyutl ... rsa_oaep_md:sha256`)
```java
Cipher c = Cipher.getInstance("RSA/ECB/OAEPPadding");
c.init(Cipher.ENCRYPT_MODE, pub, new OAEPParameterSpec("SHA-256", "MGF1",
        MGF1ParameterSpec.SHA256, PSource.PSpecified.DEFAULT));
```

## OpenSSL test
```
openssl pkeyutl -encrypt -pubin -inkey pub.pem -in key.bin -out ct.bin \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256
```

## Rules
- Specify all three parameters explicitly on both sides; document them with the ciphertext format.
- Labels: most systems use empty; if you set one (`rsa_oaep_label`), both sides must match byte for byte.
- Max plaintext = modulus bytes - 2*hashLen - 2 (190 bytes for RSA-2048 with SHA-256; Node encrypted 190 bytes and failed on 191 with `data too large for key size`).

## Verify
- [ ] Cross-library round trip test for every pair in production.
