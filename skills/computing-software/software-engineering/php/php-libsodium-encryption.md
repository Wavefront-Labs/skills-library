---
id: computing-software.software-engineering.php.php-libsodium-encryption
name: php-libsodium-encryption
category: computing-software
field: software-engineering
product: php
tags: [php, libsodium-encryption, cryptography]
level: advanced
status: docs-checked
description: "Encrypt, sign and hash in PHP with ext-sodium: secretbox, XChaCha20-Poly1305, signatures, nonces, password hashing and key handling."
sources: ["https://www.php.net/manual/en/book.sodium.php", "https://www.php.net/manual/en/sodium.installation.php", "https://www.php.net/manual/en/function.sodium-crypto-secretbox.php", "https://www.php.net/manual/en/function.sodium-crypto-secretbox-open.php", "https://www.php.net/manual/en/function.sodium-crypto-pwhash-str.php", "https://www.php.net/manual/en/function.sodium-crypto-aead-xchacha20poly1305-ietf-encrypt.php", "https://www.php.net/manual/en/function.sodium-memcmp.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encryption with libsodium

ext-sodium is bundled with PHP as of 7.2.0 (older versions: PECL).
```php
// Symmetric authenticated encryption
$key   = sodium_crypto_secretbox_keygen();                 // cryptographically secure random key; store in a secret manager
$nonce = random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES); // 24 bytes, unique per message
$ct    = $nonce . sodium_crypto_secretbox($plaintext, $nonce, $key);

$nonce = substr($ct, 0, SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
$pt    = sodium_crypto_secretbox_open(substr($ct, SODIUM_CRYPTO_SECRETBOX_NONCEBYTES), $nonce, $key);
if ($pt === false) { /* tampered or wrong key */ }
sodium_memzero($key);

// Signatures
$kp = sodium_crypto_sign_keypair();
$sig = sodium_crypto_sign_detached($msg, sodium_crypto_sign_secretkey($kp));
sodium_crypto_sign_verify_detached($sig, $msg, sodium_crypto_sign_publickey($kp));

// Password hashing and constant-time compare
$hash = sodium_crypto_pwhash_str($pw, SODIUM_CRYPTO_PWHASH_OPSLIMIT_INTERACTIVE, SODIUM_CRYPTO_PWHASH_MEMLIMIT_INTERACTIVE);
sodium_crypto_pwhash_str_verify($hash, $pw);
sodium_crypto_generichash($data);   // BLAKE2b
hash_equals($a, $b);                // bool; sodium_memcmp returns an int instead
```

## What the manual states
- `sodium_crypto_secretbox($message, $nonce, $key)`: authenticated shared-key encryption. The nonce is 24 bytes (`SODIUM_CRYPTO_SECRETBOX_NONCEBYTES`), "must be only used once, per message", and is large enough to generate randomly with `random_bytes()`. The key is 256-bit (32 bytes, `SODIUM_CRYPTO_SECRETBOX_KEYBYTES`). A wrong nonce or key length throws `SodiumException`.
- `sodium_crypto_secretbox_open()` takes the ciphertext-and-tag output of `secretbox` and returns `string|false`; false means failure. The same nonce and key are needed.
- `sodium_crypto_secretbox_keygen()` returns cryptographically secure random bytes for use with those two functions.
- `sodium_crypto_sign_detached($message, $secret_key)` returns a detached signature verifiable with the matching public key.
- `sodium_crypto_pwhash_str()` uses a memory- and CPU-hard algorithm with an automatically generated salt, and the manual notes the hashes are Argon2ID. `opslimit` and `memlimit` are required (not optional like `password_hash()` options); constants run INTERACTIVE, MODERATE, SENSITIVE and should be paired. They are embedded in the hash, so `sodium_crypto_pwhash_str_verify()` needs no separate storage.
- `sodium_crypto_generichash()` hashes with BLAKE2b; an optional key works like an HMAC key; output is raw bytes (`sodium_bin2hex()` for hex).
- `sodium_memzero()` zeroes a string passed by reference.
- `sodium_memcmp()` compares in constant time and returns 0 if equal, -1 otherwise; the manual says you almost always want `hash_equals()` instead, which returns a bool.
- `sodium_crypto_aead_xchacha20poly1305_ietf_encrypt()` is labelled "(Preferred)"; the manual says "Generally, XChaCha20-Poly1305 is the best of the provided AEAD modes to use."

## Gotchas
- Never reuse a nonce with the same key.
- Decryption failure returns `false`; handle it, do not treat it as empty plaintext.
- Slice ciphertext with a byte-based function (`substr`), and keep keys out of the repo and logs.
- Do not invent protocols; for whole-file or field encryption prefer a vetted, maintained library built on a well-reviewed primitive.

Verify: flip one ciphertext byte and confirm `secretbox_open` returns false.

## Checked
Confirmed 2026-11-08 against the PHP manual pages for the Sodium book, installation, secretbox, secretbox_open, secretbox_keygen, sign_detached, pwhash_str, generichash, memzero, memcmp and the XChaCha20-Poly1305 AEAD encrypt function. Removed as not stated by those pages: the cipher name "XSalsa20-Poly1305", the `mb_substr(..., '8bit')` advice, named third-party libraries, and the claim that `openssl_encrypt` needs particular modes; also the doc.libsodium.org source, which was not read. The key length of keygen output is taken from the secretbox page (32 bytes).
Method: docs-only read of cited pages, 2026-11-08
