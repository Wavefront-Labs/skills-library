---
id: computing-software.cryptography-implementation.libsodium.libsodium-in-javascript
name: libsodium-in-javascript
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, libsodium-advanced, libsodium-wrappers, libsodium-js, sodium-native, javascript, nodejs, wasm, browser-crypto]
level: practitioner
status: docs-checked
description: "Use libsodium from JavaScript: libsodium-wrappers (WASM, browser/Node) vs sodium-native (Node addon), awaiting sodium.ready, sumo builds, output formats and memory caveats."
sources: ["https://github.com/jedisct1/libsodium.js", "https://github.com/holepunchto/sodium-native", "https://doc.libsodium.org/bindings_for_other_languages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libsodium in JavaScript

| Package | Runs in | Notes |
|---|---|---|
| `libsodium-wrappers` | Browsers, Node, Bun | libsodium compiled to WebAssembly and pure JavaScript; standard high-level functions (about 290 KB minified and gzipped) |
| `libsodium-wrappers-sumo` | same | All symbols, including `crypto_pwhash_*` (about 375 KB); the docs say use it only if you need the extra symbols |
| `sodium-native` | Node | Low-level bindings; you allocate and pass in output buffers |

## libsodium-wrappers

```js
import _sodium from 'libsodium-wrappers';
await _sodium.ready;                 // nothing works before this resolves
const sodium = _sodium;
const key = sodium.crypto_aead_xchacha20poly1305_ietf_keygen();
const nonce = sodium.randombytes_buf(sodium.crypto_aead_xchacha20poly1305_ietf_NPUBBYTES);
const ct = sodium.crypto_aead_xchacha20poly1305_ietf_encrypt('hello', 'ad', null, nonce, key);
const pt = sodium.to_string(
  sodium.crypto_aead_xchacha20poly1305_ietf_decrypt(null, ct, 'ad', nonce, key));
```

- Binary inputs should be `Uint8Array`; a string input is converted to its UTF-8 bytes. A single binary output is a
  `Uint8Array`; functions with several outputs return an object (for example `crypto_box_keypair()` returns `publicKey`, `privateKey` and `keyType`). Use `from_hex`/`to_hex`, `from_string`/`to_string`, `from_base64`/`to_base64` to convert.
- Buffer lengths are never passed explicitly.
- The libsodium.js README says crypto functions and constants are added to the module after `ready` resolves, so with ESM access them through the default export (`sodium.crypto_box_PUBLICKEYBYTES`), not named imports.
- Streaming APIs with no final function, such as `crypto_secretstream_xchacha20poly1305_*` and `crypto_xof_*`, need `sodium.free(state)` after the last operation.
- `crypto_pwhash_*` is only in the sumo build; tune `opslimit/memlimit` on the slowest target browser.

## sodium-native

```js
const sodium = require('sodium-native');
const key = sodium.sodium_malloc(sodium.crypto_secretbox_KEYBYTES);
sodium.crypto_secretbox_keygen(key);
const nonce = Buffer.alloc(sodium.crypto_secretbox_NONCEBYTES); sodium.randombytes_buf(nonce);
const c = Buffer.alloc(m.length + sodium.crypto_secretbox_MACBYTES);
sodium.crypto_secretbox_easy(c, m, nonce, key);
```

You allocate outputs; `sodium_malloc` returns secure buffers.

## Caveats

- JS strings and GC: secrets in strings cannot be wiped. Keep keys as
  `Uint8Array` and call `sodium.memzero(key)` when done (it applies to `Uint8Array` objects; best effort, copies
  may exist).
- In browsers, the page's own JS and extensions can read keys; libsodium does
  not change the trust model of web crypto. Consider Web Crypto
  non-extractable keys where they fit.
- Bundle size: the sumo build is larger than the standard one; lazy-load it if you need it.

## Verify

- [ ] All calls happen after `await sodium.ready`.
- [ ] Ciphertexts interoperate with the server's libsodium (same nonce/AD encoding).
- [ ] pwhash parameters benchmarked in the target browsers.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed against the libsodium.js README and sodium-native README: ready promise, standard versus sumo contents, pwhash only in sumo, Uint8Array and UTF-8 string handling, multi-output objects, sodium.free for streaming states, memzero, supported runtimes (browsers, NodeJS, Bun), sodium_malloc secure buffers and caller-allocated outputs. Removed unconfirmed claims about decryption error text, WASM speed ratios, ristretto255 in sumo, Deno and other packages, and the output-format argument.

Method: documentation only; no commands were run.
