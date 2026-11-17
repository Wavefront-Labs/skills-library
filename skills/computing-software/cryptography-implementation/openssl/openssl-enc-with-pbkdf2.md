---
id: computing-software.cryptography-implementation.openssl.openssl-enc-with-pbkdf2
name: openssl-enc-with-pbkdf2
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-enc, enc-pbkdf2, pbkdf2, salt, iteration-count, aes-256-cbc, deprecated-key-derivation-warning]
level: practitioner
status: verified
description: "Use openssl enc with -pbkdf2 and a high -iter correctly when you must, file format (Salted__ header), the 'deprecated key derivation' warning, and decrypt-side matching."
sources: ["https://docs.openssl.org/3.0/man1/openssl-enc/", "https://csrc.nist.gov/pubs/sp/800/132/final", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#pbkdf2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# openssl enc with -pbkdf2

`openssl enc` is a password-based file encryption tool from the 1990s. If you
must use it (scripts, minimal systems where only OpenSSL is installed), use
the PBKDF2 options added in 1.1.1.

```bash
openssl enc -aes-256-cbc -pbkdf2 -iter 600000 -salt -md sha256 \
  -in secrets.tar -out secrets.tar.enc -pass file:./passfile
openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -md sha256 \
  -in secrets.tar.enc -out secrets.tar -pass file:./passfile
```

## Options that matter

- `-pbkdf2`: derive key and IV with PBKDF2 instead of the legacy
  `EVP_BytesToKey` (one MD5/SHA-256 iteration, trivially brute-forced). Without
  it OpenSSL 1.1.1+ prints `*** WARNING : deprecated key derivation used.`
- `-iter N`: default is 10,000 - too low. OWASP 2023+: 600,000 for
  PBKDF2-HMAC-SHA256. The count is **not stored** in the file; the decryptor
  must pass the same `-iter` and `-md`.
- `-md sha256`: PBKDF2 PRF digest (default SHA-256 in 1.1.0+, MD5 before).
- `-salt` (default): 8-byte random salt stored after the `Salted__` magic.
  `-nosalt` makes identical passwords produce identical keys - never use.
- `-pass file:`, `env:` or `fd:` keep the password off the command line
  (`pass:` is visible in `ps` and shell history).

## File format

`"Salted__" (8 bytes) || salt (8 bytes) || ciphertext`. No version, no
iteration count, no algorithm id, and no MAC. Store parameters alongside
(README, filename suffix) or you will not be able to decrypt in five years.

## Why it is still weak

- No integrity: CBC ciphertext can be modified; corruption is detected only by
  bad padding (not reliably) - see enc limitations skill.
- PBKDF2 is not memory-hard; passwords must be long random strings
  (`openssl rand -base64 32 > passfile`).

## Checked
Run with OpenSSL 3.2.3 on 2026-10-18: encrypting with `-pbkdf2 -iter 600000 -salt -md sha256` writes a file starting `Salted__` (8-byte magic, 8-byte salt, then ciphertext: 5 bytes of input gave 32 bytes); decrypting with a different `-iter` fails with `bad decrypt`; omitting `-pbkdf2` prints `*** WARNING : deprecated key derivation used.`; `openssl enc -help` states the default iteration count is 10000 and that `-iter` forces PBKDF2; OWASP's Password Storage Cheat Sheet lists 600,000 iterations for PBKDF2-HMAC-SHA256.

## Verify

- [ ] No `deprecated key derivation` warning on encrypt.
- [ ] `-iter` >= 600000 and recorded with the file.
- [ ] Password supplied via file/env/fd, not `pass:`.
- [ ] Integrity covered separately (signature or HMAC) or tool replaced (age, CMS).
