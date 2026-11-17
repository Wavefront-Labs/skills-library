---
id: computing-software.cryptography-implementation.libsodium.php-sodium-and-pynacl
name: php-sodium-and-pynacl
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, libsodium-advanced, php-sodium, pynacl, sodium-compat, python, php, bindings, password-hash]
level: practitioner
status: docs-checked
description: "Use libsodium from PHP (ext/sodium, sodium_compat) and Python (PyNaCl): function naming, exceptions vs return codes, key encoding, and password hashing helpers."
sources: ["https://github.com/php/php-src/blob/master/ext/sodium/libsodium.stub.php", "https://github.com/paragonie/sodium_compat", "https://github.com/pyca/pynacl/tree/main/docs", "https://doc.libsodium.org/bindings_for_other_languages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libsodium from PHP and Python

## PHP: ext/sodium (bundled since PHP 7.2)

```php
$key   = sodium_crypto_aead_xchacha20poly1305_ietf_keygen();
$nonce = random_bytes(SODIUM_CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES);
$ct    = sodium_crypto_aead_xchacha20poly1305_ietf_encrypt($msg, $ad, $nonce, $key);
$pt    = sodium_crypto_aead_xchacha20poly1305_ietf_decrypt($ct, $ad, $nonce, $key);
if ($pt === false) { /* reject: auth failed */ }
sodium_memzero($key);
```

- Decrypt functions return `false` on failure (not an exception) - always
  check with `=== false`.
- Strings are byte strings; store with `sodium_bin2base64($ct, SODIUM_BASE64_VARIANT_URLSAFE_NO_PADDING)`.
- `sodium_memzero` works on the variable but PHP may have copied the string
  elsewhere (copy-on-write); best effort.
- Password hashing: `sodium_crypto_pwhash_str($password, SODIUM_CRYPTO_PWHASH_OPSLIMIT_MODERATE, SODIUM_CRYPTO_PWHASH_MEMLIMIT_MODERATE)`;
  verify with `sodium_crypto_pwhash_str_verify($hash, $password)` (returns bool) and check `sodium_crypto_pwhash_str_needs_rehash`.
- `paragonie/sodium_compat`: a pure PHP polyfill for hosts without the
  extension. Its README has a "Sodium_Compat is Slow" section recommending PHP 7.2+ or the PECL extension and describing a `fastMult` trade-off between speed and constant-time safety on some processors; use the extension in production.

## Python: PyNaCl

```python
from nacl.secret import SecretBox      # XSalsa20-Poly1305, random 24-byte nonce
from nacl.public import PrivateKey, SealedBox
from nacl.exceptions import CryptoError
import nacl.utils, nacl.pwhash

box = SecretBox(nacl.utils.random(SecretBox.KEY_SIZE))
ct = box.encrypt(b"msg")                # nonce prepended automatically
try:
    pt = box.decrypt(ct)
except CryptoError:
    ...                                  # reject
sk = PrivateKey.generate(); sealed = SealedBox(sk.public_key).encrypt(b"x")
h = nacl.pwhash.argon2id.str(b"password")
nacl.pwhash.verify(h, b"password")       # True, or raises InvalidkeyError on a wrong password
```

- High-level classes handle nonces (`SecretBox.encrypt` prepends one).
- Failures raise exceptions (they derive from `nacl.exceptions.CryptoError`); do not catch broadly and continue.
- Lower-level functions live in `nacl.bindings` (e.g. AEAD XChaCha20).

## Verify

- [ ] PHP decrypt results checked with `=== false`; Python CryptoError handled by rejecting.
- [ ] Production PHP uses ext/sodium, not the polyfill (`extension_loaded('sodium')`).
- [ ] Ciphertexts interoperate with other services' libsodium (same construction and encoding).

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed against php-src ext/sodium stubs (master): sodium_crypto_aead_xchacha20poly1305_ietf_encrypt, decrypt (returns string or false), keygen, sodium_crypto_pwhash_str, _str_verify and _str_needs_rehash (both bool), sodium_memzero, sodium_bin2base64 and the SODIUM_BASE64_VARIANT_URLSAFE_NO_PADDING constant; PHP 7.2 or later bundles libsodium (libsodium docs); PyNaCl SecretBox.KEY_SIZE, automatic nonce, CryptoError family, SealedBox, nacl.pwhash.verify raising InvalidkeyError; sodium_compat README on speed. Removed an unconfirmed password_hash claim and a PyNaCl version-function remark.

Method: documentation only; no commands were run.
