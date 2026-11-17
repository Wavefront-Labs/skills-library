---
id: computing-software.cryptography-implementation.crypto-libraries.web-crypto-aes-gcm-encrypt-and-decrypt
name: web-crypto-aes-gcm-encrypt-and-decrypt
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, web-crypto, subtle-crypto, subtle-encrypt, aes-gcm, browser-crypto, secure-context]
level: practitioner
status: verified
description: "Encrypt and decrypt with SubtleCrypto AES-GCM in browsers and Node: key generation, 12-byte IVs, additionalData, the ct-plus-tag layout, OperationError and secure contexts."
sources: ["https://www.w3.org/TR/WebCryptoAPI/", "https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/encrypt", "https://nodejs.org/api/webcrypto.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SubtleCrypto AES-GCM encrypt and decrypt

## Code
```js
const enc = new TextEncoder(), dec = new TextDecoder();

const key = await crypto.subtle.generateKey(
  { name: "AES-GCM", length: 256 }, false /* non-extractable */, ["encrypt", "decrypt"]);

async function seal(key, text, aadText) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = new Uint8Array(await crypto.subtle.encrypt(
    { name: "AES-GCM", iv, additionalData: enc.encode(aadText), tagLength: 128 },
    key, enc.encode(text)));
  const out = new Uint8Array(12 + ct.length); out.set(iv); out.set(ct, 12);
  return out;                                      // iv || ciphertext || tag
}

async function open(key, blob, aadText) {
  if (blob.length < 12 + 16) throw new Error("decrypt failed");
  try {
    const pt = await crypto.subtle.decrypt(
      { name: "AES-GCM", iv: blob.subarray(0, 12), additionalData: enc.encode(aadText) },
      key, blob.subarray(12));
    return dec.decode(pt);
  } catch { throw new Error("decrypt failed"); }   // OperationError, no detail by design
}
```

## Rules
- **Secure context only.** `crypto.subtle` is `undefined` on plain-HTTP pages (localhost excepted).
  `crypto.getRandomValues` works everywhere and is the right RNG.
- Node.js: the same API is `globalThis.crypto.subtle` (present on Node 20, checked; `require("node:crypto").webcrypto` also works).
- IV: 12 random bytes per message; the same key/IV pair twice breaks confidentiality and
  authenticity. NIST SP 800-38D limits random-IV use to at most 2^32 invocations per key.
- Output is `ciphertext || tag` (16 bytes) as one buffer (checked: 2 bytes in, 18 out), the same layout as Python's `AESGCM` and Go's `Seal`.
  Node's `createCipheriv` returns the tag separately; join them when interoperating (a `createCipheriv` blob with tag appended decrypted in `subtle`).
- `additionalData` must be identical on decrypt; use it to bind record ID, user ID or version.
- Whole-buffer only: no streaming. Chunk large files with a per-chunk IV/counter and index in AAD
  (or use libsodium's secretstream via WASM).

## Where the key comes from
- Generated and kept non-extractable (stored in IndexedDB, see that skill).
- Derived from a password with PBKDF2 or from a shared secret with HKDF (see `deriveKey`).
- Unwrapped from a server-provided wrapped key with `unwrapKey`.
Never put a raw key in `localStorage` or in the page source.

## Threat model reminder
Browser-side encryption protects data from the server/storage only if the code itself is trusted.
The server that ships the JavaScript can ship code that leaks the key. Use it for end-to-end
designs with code integrity (extensions, SRI, signed apps), or as defence in depth.

## Verify
- [ ] Round trip works; modified IV, ciphertext, tag or AAD each throws `OperationError` (checked; inputs shorter than the tag also throw).
- [ ] Ciphertext decrypts in the server-side language with the same layout.
- [ ] Page is served over HTTPS; `crypto.subtle` is defined in production.
