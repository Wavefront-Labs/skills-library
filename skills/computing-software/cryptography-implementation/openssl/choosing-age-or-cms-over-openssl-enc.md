---
id: computing-software.cryptography-implementation.openssl.choosing-age-or-cms-over-openssl-enc
name: choosing-age-or-cms-over-openssl-enc
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-enc, age-encryption, age, age-tool, gpg, sops, file-encryption, tool-selection]
level: practitioner
status: docs-checked
description: "Pick a file encryption tool instead of openssl enc: age (passphrase or X25519/SSH recipients), CMS for X.509 recipients, sops for config secrets, gpg for PGP estates."
sources: ["https://age-encryption.org/v1", "https://github.com/FiloSottile/age", "https://docs.openssl.org/3.0/man1/openssl-cms/", "https://github.com/getsops/sops"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing age or CMS over openssl enc

| Need | Tool |
|---|---|
| Encrypt a file with a passphrase | `age -p` (scrypt recipient, ChaCha20-Poly1305 chunks) |
| Encrypt to people/servers with keys | `age -r age1...` or `-R ~/.ssh/id_ed25519.pub` |
| Recipients have X.509 certs (B2B, S/MIME) | `openssl cms -encrypt` |
| Secrets in YAML/JSON/ENV/INI in git | `sops` with age, PGP or cloud KMS keys |
| Existing PGP keyring / Debian-style signing | `gpg` |
| Programmatic | library AEAD (libsodium secretstream, Tink streaming AEAD) |

## age essentials

```bash
age-keygen -o key.txt                       # prints public key age1...
age -r age1<recipient> -o file.age file     # to recipient
age -R ~/.ssh/id_ed25519.pub -o f.age f     # to an SSH key
age -p -o f.age f                           # passphrase (prompted)
age -d -i key.txt f.age > f
age -a ...                                  # ASCII armor (--armor)
```

Format (age v1 spec): a header with one stanza per recipient wrapping a random file key, an HMAC-SHA-256 header MAC,
then the payload in 64 KiB chunks, each ChaCha20-Poly1305 encrypted with a final-chunk flag in the nonce; streaming
decryption must signal an error if the end of file arrives without a valid final chunk (truncation detected). An
scrypt stanza must be the only stanza in a header. Hardware keys use plugins such as `age-plugin-yubikey`. SSH
recipients (ssh-rsa, ssh-ed25519) are supported but `ssh-agent` is not, and an SSH recipient embeds a public key tag
in the file, so files can be linked to a specific public key.

## sops for config secrets

SOPS is an editor of encrypted files for YAML, JSON, ENV, INI and BINARY, encrypting with AWS KMS, GCP KMS, Azure Key
Vault, HuaweiCloud KMS, age and PGP. A `.sops.yaml` in the repository holds its configuration; see the sops README for
the exact flags.

## When CMS wins

Regulated B2B exchanges, government portals and email clients that speak S/MIME already have certificate
infrastructure; age would be a new key system to manage. `openssl cms -encrypt` takes recipient certificates, a
cipher option (for example `-aes256`) and `-keyopt` to select RSA-OAEP. Check your OpenSSL version's man page for
supported content-encryption ciphers before choosing one.

## Verify

- [ ] Chosen tool authenticates ciphertext (tamper test fails decryption).
- [ ] Recipient keys documented with owners; identity files protected (0600 or hardware).
- [ ] No remaining `openssl enc` in new scripts.

## Checked
2026-11-01. Confirmed in the age README, the age v1 spec, the openssl-cms 3.0 man page and the sops README: age flags
(`-r`, `-R`, `-p`, `-a`, `-d`, `-i`, `-o`), SSH recipient behaviour, plugin-yubikey, 64 KiB ChaCha20-Poly1305 payload
chunks with final-chunk handling, HMAC-SHA-256 header MAC, scrypt-stanza-alone rule, sops formats and key backends,
cms `-encrypt`, cipher options and `-keyopt` for RSA-OAEP. Removed unconfirmed: `-aes-256-gcm` for CMS, `age-plugin-tpm`,
the sops `--encrypted-regex` example and its AES-256-GCM data-key detail, and the no-signature, no-revocation and
scrypt work-factor statements.
Method: documentation only; no commands were run.
