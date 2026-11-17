---
id: computing-software.cryptography-implementation.protocol-implementation.signed-and-one-time-prekey-management
name: signed-and-one-time-prekey-management
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, prekey-bundle, x3dh, pqxdh, signed-prekey, one-time-prekey, e2ee]
level: advanced
status: docs-checked
description: "Manage X3DH and PQXDH prekey bundles: signed prekey rotation, one-time prekey replenishment, last-resort keys, server distribution rules and key exhaustion attacks."
sources: ["https://signal.org/docs/specifications/x3dh/", "https://signal.org/docs/specifications/pqxdh/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signed and one-time prekey management

## Bundle contents
- Identity key (long-term).
- Signed prekey (SPK): replaced periodically, signed by the identity key.
- One-time prekeys (OPK): a set of keys, each used in a single protocol run. All curve keys in a run are X25519 or
  all X448.
- PQXDH adds post-quantum KEM (pqkem) prekeys: a set of signed one-time pqkem prekeys plus a signed last-resort pqkem
  prekey, each with an identifier; the last-resort key is used only when one-time pqkem prekeys run out.

## Client duties
- Upload a new signed prekey and signature at some interval (the specs give once a week or once a month as examples;
  the new one replaces the old). The old private key may be kept for some period to handle delayed messages, then
  deleted for forward secrecy. In PQXDH the signed last-resort pqkem prekey rotates the same way.
- Upload new OPKs when the server reports its store is getting low.
- Delete an OPK private key once a message using it has been received and decrypted (forward secrecy for the
  initial message).
- Verify the prekey signature on bundles fetched for others and abort the protocol if verification fails.

## Server duties
- Provide one of the recipient's OPKs if one exists, then delete it.
- When OPKs are exhausted, serve the bundle without an OPK; the initial message then lacks the extra DH, so forward
  secrecy depends on the signed prekey's lifetime and the message can be replayed to the recipient. In PQXDH the
  last-resort pqkem prekey covers exhausted one-time pqkem prekeys.
- Rate-limit prekey fetches: a party draining another's OPKs reduces initial forward secrecy, and the X3DH spec says
  the server should try to prevent this.

## Pitfalls
- Handing out the same OPK twice because two fetches raced on the server.
- Initial messages without an OPK can be replayed; the X3DH spec suggests the post-X3DH protocol quickly negotiate
  fresh keys so replays do not matter.

## Verify
- [ ] Concurrency test shows unique OPK per fetch; SPK rotation leaves the old key usable only for a bounded period.

## Checked

2026-11-01. Confirmed against the X3DH and PQXDH specifications (bundle contents, signed prekey replacement
"once a week or once a month", keeping then deleting the old private key, OPK upload when low, server provides then
deletes an OPK, bundle without OPK, replay of OPK-less messages, rate limits against draining, signature check and
abort, last-resort pqkem prekey purpose). Removed: batch size 100, low-count threshold 10, "a few days" grace, the
"Kyber/ML-KEM" naming and the "Signal" rotation claim (not stated in the specs).
Method: documentation only; no commands were run.
