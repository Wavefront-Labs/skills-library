---
id: computing-software.cryptography-implementation.openssl.decrypting-legacy-evp-bytestokey-files
name: decrypting-legacy-evp-bytestokey-files
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-enc, evp-bytestokey, legacy-decryption, salted-header, md5-default, cryptojs, migration]
level: advanced
status: verified
description: "Decrypt old openssl enc and CryptoJS files that used EVP_BytesToKey: MD5 vs SHA-256 default change in 1.1.0, Salted__ parsing, reimplementing the KDF, then re-encrypting."
sources: ["https://docs.openssl.org/3.0/man3/EVP_BytesToKey/", "https://docs.openssl.org/3.0/man1/openssl-enc/", "https://cryptojs.gitbook.io/docs/#the-cipher-output"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decrypting legacy EVP_BytesToKey files

Files made with `openssl enc` before `-pbkdf2` existed (and CryptoJS
`AES.encrypt(text, "passphrase")`, which copies the format) derive key and IV
with `EVP_BytesToKey`: D_i = HASH(D_{i-1} || password || salt), one iteration,
concatenated until key+IV length.

## The default digest changed

| Encrypted with | Default `-md` |
|---|---|
| OpenSSL < 1.1.0 | MD5 |
| OpenSSL >= 1.1.0 | SHA-256 |
| CryptoJS | MD5 |

"bad decrypt" on an old file with a new OpenSSL is usually this:

```bash
openssl enc -d -aes-256-cbc -md md5 -in old.enc -out old.dec -pass file:pw
```

## Parse the file

- Starts with `Salted__` (base64: `U2FsdGVkX1`): next 8 bytes are the salt.
- No `Salted__`: encrypted with `-nosalt`, or raw key/IV mode (`-K`/`-iv`).
- With `-a`/`-base64`, decode first (`openssl base64 -d -A` for single-line).

## Reimplement in code (for bulk migration)

```python
import hashlib
def evp_bytes_to_key(pw: bytes, salt: bytes, klen=32, ivlen=16, h=hashlib.md5):
    d, out = b"", b""
    while len(out) < klen + ivlen:
        d = h(d + pw + salt).digest(); out += d
    return out[:klen], out[klen:klen + ivlen]
blob = open("old.enc","rb").read(); assert blob[:8] == b"Salted__"
key, iv = evp_bytes_to_key(pw, blob[8:16])
# then AES-256-CBC decrypt blob[16:] and strip PKCS#7 padding
```

## Migrate

1. Decrypt in a controlled environment; verify plaintext sanity (magic bytes,
   checksums) since there is no integrity check.
2. Re-encrypt with an authenticated tool (age, CMS AuthEnvelopedData, or app
   AEAD) and a strong passphrase/KDF or recipient keys.
3. Securely delete the legacy ciphertext copies if policy requires, and the
   temporary plaintext (`shred` is unreliable on SSD/COW filesystems; use an
   encrypted tmpfs).

The weak KDF means anyone with these old files can brute-force short
passwords quickly; treat the content as exposed if the files leaked.

## Verify

- [ ] Correct digest identified (md5 vs sha256) on a sample.
- [ ] Python reimplementation matches `openssl enc -P -md md5 -S <salt>` key/IV output.
- [ ] All legacy files re-encrypted; legacy decrypt script archived.

## Checked
- OpenSSL 3.2.3: an `-md md5` file starts `Salted__` (base64 `U2FsdGVkX1`), decrypts with `-md md5` and not with the default digest; the Python function reproduces the key and IV printed by `openssl enc -P -md md5 -S <salt>`; a crypto-js `AES.encrypt(text, "secret")` string decrypts with `-md md5 -a -A` (needs `-A` because crypto-js writes one line) and fails with the default digest.
- OpenSSL CHANGES.md records the `enc`/`dgst` default digest change from MD5 to SHA-256 (1.1.0).
