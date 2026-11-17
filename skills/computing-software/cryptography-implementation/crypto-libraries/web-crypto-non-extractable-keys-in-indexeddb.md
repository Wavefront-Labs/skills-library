---
id: computing-software.cryptography-implementation.crypto-libraries.web-crypto-non-extractable-keys-in-indexeddb
name: web-crypto-non-extractable-keys-in-indexeddb
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, web-crypto, subtle-crypto, non-extractable-cryptokey, indexeddb, dpop, device-binding]
level: advanced
status: gated
description: "Keep browser keys non-extractable: store CryptoKey objects in IndexedDB, what XSS can still do, storage eviction and ITP limits, DPoP-style device keys and recovery."
sources: ["https://www.w3.org/TR/WebCryptoAPI/#cryptokey-interface", "https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API", "https://www.rfc-editor.org/rfc/rfc9449", "https://webkit.org/tracking-prevention/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-extractable CryptoKeys in IndexedDB

A `CryptoKey` created with `extractable: false` can be used by script but its bytes can't be read
by script. It's the browser equivalent of a non-exportable HSM key, with weaker guarantees.

## Create and store
```js
const kp = await crypto.subtle.generateKey(
  { name: "ECDSA", namedCurve: "P-256" }, false, ["sign", "verify"]);
const db = await new Promise((res, rej) => {
  const r = indexedDB.open("keys", 1);
  r.onupgradeneeded = () => r.result.createObjectStore("k");
  r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
});
db.transaction("k", "readwrite").objectStore("k").put(kp, "device");
```
CryptoKey objects are structured-cloneable (checked: `structuredClone` of a non-extractable key pair kept `extractable: false`), so IndexedDB stores them directly and keeps the
non-extractable property (gated: unconfirmed, no browser available to run IndexedDB). `localStorage`/`sessionStorage` hold strings only and would require an
extractable key, so they're the wrong place.

## What this does and does not protect
- Protects against exfiltration: XSS, malicious extensions reading storage, or a stolen disk image
  read by script can't copy the raw key off the device.
- Doesn't protect against use: XSS running in your origin can call `sign`/`decrypt` with the key
  while it runs. Keep CSP strict and treat signatures as proof of "this browser profile", not of the user.
- The browser stores the key material on disk in its profile; malware with OS access can read it.
  It's not hardware-backed (WebAuthn/passkeys are the hardware-backed option).

## Typical uses
- **DPoP (RFC 9449)**: a non-extractable P-256 key signs per-request proofs, binding OAuth access
  tokens to the browser so a stolen token alone is useless.
- Device binding for sessions, signing local data, wrapping keys for client-side encryption.

## Storage lifetime
- Clearing site data, private windows and storage pressure delete the key. Request
  `navigator.storage.persist()` and handle loss.
- Safari's ITP deletes all script-writeable storage, IndexedDB included, after 7 days of no user interaction with the site (WebKit tracking-prevention page); design for re-enrolment.
- Keys are per origin; subdomains don't share them.

## Wrap and recovery
- `wrapKey` requires the key being wrapped to be extractable (checked in Node: wrapping a non-extractable key threw), so a non-extractable key can never
  be backed up. That's the point. Design recovery as "enrol a new key", with the server revoking
  the old public key.
- If you need recoverable client-side encryption keys, generate an extractable data key, wrap it
  under a non-extractable KEK and also under a recovery key, then store only wrapped forms.

## Verify
- [ ] `crypto.subtle.exportKey("jwk", kp.privateKey)` throws (browsers: `InvalidAccessError`; Node 20 reports "key is not extractable" under a different name). The public key still exports (checked).
- [ ] The app recovers cleanly when the stored key is missing (new enrolment flow).
- [ ] CSP blocks inline and third-party script that could use the key.
