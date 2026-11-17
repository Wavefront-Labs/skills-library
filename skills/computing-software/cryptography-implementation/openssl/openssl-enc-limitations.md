---
id: computing-software.cryptography-implementation.openssl.openssl-enc-limitations
name: openssl-enc-limitations
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-enc, enc-no-aead, aead-unsupported, malleability, file-encryption, integrity, encrypt-then-mac]
level: practitioner
status: verified
description: "Know what openssl enc cannot do: no AEAD modes (GCM/CCM rejected), no integrity, no streaming authentication, no metadata; and how to add an HMAC if you must keep it."
sources: ["https://docs.openssl.org/3.0/man1/openssl-enc/", "https://github.com/openssl/openssl/issues/471", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# openssl enc limitations

The `openssl enc` manual says it: "This command does not support authenticated
encryption modes like CCM and GCM, and will not support such modes in the future."
`openssl enc -aes-256-gcm` fails with `AEAD ciphers not supported` (tested on 3.2.3).

## What that means

- **No integrity**: anyone who can modify the file can flip bits. In CBC mode
  a flipped ciphertext bit garbles one block and flips the matching bit in the
  next block; in CTR mode (`-aes-256-ctr`) bits flip precisely (tested: flipping the first
  ciphertext bit changed only `h` to `i` in the plaintext). Decryption
  "succeeds" with modified plaintext.
- Bad padding error on decrypt is the only signal, and it is unreliable
  (about 1 in 255 random final blocks still has valid PKCS#7 padding, by calculation).
- No header carrying algorithm, KDF or iterations (see pbkdf2 skill).
- Whole-file operation with no chunk authentication.

## If you must keep enc: add encrypt-then-MAC

```bash
# derive two independent keys is awkward in shell; use separate random secrets
openssl enc -aes-256-ctr -pbkdf2 -iter 600000 -in f -out f.enc -pass file:enc.pass
openssl mac -digest SHA256 -macopt hexkey:$(cat mac.hexkey) -in f.enc HMAC > f.enc.mac
# decrypt side: verify MAC first, compare, then decrypt
test "$(openssl mac -digest SHA256 -macopt hexkey:$(cat mac.hexkey) -in f.enc HMAC)" = "$(cat f.enc.mac)" \
  && openssl enc -d -aes-256-ctr -pbkdf2 -iter 600000 -in f.enc -out f -pass file:enc.pass
```

Shell string comparison is not constant time; acceptable for offline file
checks, not for a network service. Alternatively sign the ciphertext with
`openssl dgst -sign`.

## Better: replace it

- `age` for files to recipients or passphrases (authenticated, chunked).
- `openssl cms -encrypt -aes-256-gcm` when recipients have certificates.
- `gpg --symmetric` (OpenPGP) for PGP estates; check which integrity mode your version uses.
- In code: an AEAD from libsodium/Tink, never shelling out to `openssl enc`.

## Verify

- [ ] Inventory of scripts using `openssl enc` (grep CI, cron, backup scripts).
- [ ] Each either adds a verified MAC/signature or is scheduled for replacement.
- [ ] Tamper test: modify one byte; the pipeline must refuse to decrypt.
