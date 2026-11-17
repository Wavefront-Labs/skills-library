---
id: computing-software.cryptography-implementation.openssl.openssl-smime-versus-cms
name: openssl-smime-versus-cms
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, openssl-smime, openssl-cms, pkcs7, cms, s-mime]
level: practitioner
status: verified
description: "Choose between openssl smime and openssl cms: smime is PKCS#7 legacy, cms adds AuthEnvelopedData (AES-GCM), RSA-OAEP, ECDH recipients and receipts; flags mostly shared."
sources: ["https://docs.openssl.org/3.0/man1/openssl-smime/", "https://docs.openssl.org/3.0/man1/openssl-cms/", "https://www.rfc-editor.org/rfc/rfc5652"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# openssl smime versus cms

## Differences
| Feature | `smime` | `cms` |
|---|---|---|
| Format | PKCS#7 (RFC 2315) | CMS (RFC 5652), a superset |
| AES-GCM AuthEnvelopedData | no | yes (`-aes-256-gcm`, 3.0+) |
| RSA-OAEP / RSA-PSS | no | `-keyopt rsa_padding_mode:oaep` / `pss` |
| ECDH key-agreement recipients | no | yes (KeyAgreeRecipientInfo) |
| Password and KEK recipients | no | `-pwri_password`, `-secretkey` |
| Signed receipts, compression | no | yes |

## Equivalent commands
```sh
openssl smime -sign -in msg.txt -signer cert.pem -inkey key.pem -out msg.p7m
openssl cms   -sign -in msg.txt -signer cert.pem -inkey key.pem -out msg.p7m
openssl cms -encrypt -aes-256-gcm -in data.bin -recip bob.pem -out data.p7m
openssl cms -decrypt -in data.p7m -recip bob.pem -inkey bob.key -out data.bin
```

## Guidance
- Use `cms` for new work. Use `smime` only when the receiver is a legacy PKCS#7 consumer; `cms` can still
  produce compatible output with CBC ciphers and RSA PKCS#1 v1.5 recipients.
- Both default to S/MIME MIME output; use `-outform DER` for binary blobs and `-binary` to avoid CRLF translation
  of binary content (signature failures otherwise).

## Verify
- [ ] Receiver (Outlook, Thunderbird, Java BouncyCastle) decrypts and verifies a sample produced with chosen options.

## Checked
- OpenSSL 3.2.3: the equivalent `smime`/`cms` sign commands both succeed and write S/MIME output by default; `cms -encrypt -aes-256-gcm` writes AuthEnvelopedData while `smime -encrypt -aes-256-gcm` fails ("cipher parameter error"); `smime -help` lists none of `-keyopt`, `-pwri_password`, `-secretkey`, `-compress` or `-receipt_request_all`, which `cms -help` offers (`-compress` and password recipients also ran). The 3.0 `openssl-cms` manual already documents AES-GCM.
