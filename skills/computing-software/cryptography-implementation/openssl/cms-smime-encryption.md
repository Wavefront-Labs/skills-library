---
id: computing-software.cryptography-implementation.openssl.cms-smime-encryption
name: cms-smime-encryption
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-cms, cms-encryption, smime, envelopeddata, authenvelopeddata, aes-gcm, rsa-oaep, kari, rfc5083]
level: advanced
status: verified
description: "Encrypt files or messages to certificate holders with openssl cms: AuthEnvelopedData with AES-GCM, RSA-OAEP vs ECDH recipients, multiple recipients, and decrypt."
sources: ["https://docs.openssl.org/3.0/man1/openssl-cms/", "https://datatracker.ietf.org/doc/html/rfc5652#section-6", "https://datatracker.ietf.org/doc/html/rfc5083", "https://datatracker.ietf.org/doc/html/rfc8551"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CMS / S/MIME encryption with openssl cms

CMS EnvelopedData encrypts content with a random content-encryption key (CEK)
and wraps the CEK for each recipient's certificate. It is the right tool when
recipients already have X.509 certificates (S/MIME, B2B file exchange).

## Encrypt

```bash
# AES-256-GCM (AuthEnvelopedData, RFC 5083) to two recipients; OAEP for RSA recipients
openssl cms -encrypt -binary -aes-256-gcm -in report.pdf -outform DER -out report.pdf.p7m \
  -recip alice.crt -keyopt rsa_padding_mode:oaep -keyopt rsa_oaep_md:sha256 \
  -recip bob_ec.crt
```

- `-aes-256-gcm` produces AuthEnvelopedData (integrity included). `-aes256` produces
  EnvelopedData with AES-CBC and **no integrity**, as does the default, which is 3DES-CBC before OpenSSL 3.5
  (3.2.3 printed `des-ede3-cbc`) and AES-256-CBC from 3.5 (per the 3.5 manual); sign
  then encrypt if you must use CBC for compatibility (older Outlook/clients).
- RSA recipients: default key transport is PKCS#1 v1.5; add `-keyopt
  rsa_padding_mode:oaep` per recipient (after its `-recip`).
- EC recipients use key agreement (KARI, ECDH ephemeral-static with SHA-1 KDF and `id-aes256-wrap` on 3.2.3)
  automatically.
- Each `-recip` adds a RecipientInfo; any one of them can decrypt.

## Decrypt

```bash
openssl cms -decrypt -binary -inform DER -in report.pdf.p7m -recip alice.crt \
  -inkey alice.key -out report.pdf
openssl cms -cmsout -print -inform DER -in report.pdf.p7m | grep -E 'contentType|algorithm'
```

## Sign and encrypt order

S/MIME convention: sign first, then encrypt (`openssl cms -sign ... | openssl
cms -encrypt ...`), so the signature is hidden and the recipient verifies after
decrypting. Encrypting then signing reveals the signer to observers and allows
signature stripping and re-signing.

## Gotchas

- Recipient certificate must allow key encipherment (RSA keyUsage
  `keyEncipherment`, EC `keyAgreement`). Some clients ignore this; OpenSSL may
  not enforce it either; check yourself.
- `-binary` again matters for non-text content.
- Decryption errors are deliberately generic; check you used the matching
  certificate (`-recip`) and key pair.

## Verify

- [ ] Output structure shows `id-smime-ct-authEnvelopedData` and an AES-GCM OID when integrity is required
      (tested on 3.2.3: `contentType: id-smime-ct-authEnvelopedData`, `aes-256-gcm`).
- [ ] RSA recipients show `rsaesOaep` key encryption.
- [ ] Each recipient decrypts successfully with their tooling.
