---
id: computing-software.cryptography-implementation.protocol-implementation.x3dh-and-pqxdh-key-agreement
name: x3dh-and-pqxdh-key-agreement
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, end-to-end-encryption, e2ee, pqxdh, x3dh, prekeys, ml-kem, signal-protocol, asynchronous-key-agreement]
level: sme
status: docs-checked
description: "Implement asynchronous E2EE session setup with X3DH and post-quantum PQXDH: prekey bundles, signed and one-time prekeys, the KEM step, server handling."
sources: ["https://signal.org/docs/specifications/x3dh/", "https://signal.org/docs/specifications/pqxdh/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X3DH and PQXDH key agreement

Messaging needs to start an encrypted session with someone who is offline.
X3DH (Signal) does this with prekeys published to a server; PQXDH (Signal)
adds a post-quantum KEM so recorded sessions resist future quantum
decryption.

## Keys Bob publishes (prekey bundle)

- Identity key IK_B (long-term, curve25519 or curve448, signatures via XEdDSA).
- Signed prekey SPK_B (same curve, replaced periodically, e.g. once a week or month) + signature by IK_B.
- One-time prekeys OPK_B (X25519, many, each used once).
- PQXDH adds: signed last-resort PQ prekey PQSPK_B and optional one-time PQ
  prekeys (the spec's example KEM is CRYSTALS-Kyber-1024), each signed by IK_B.

## Alice's computation (X3DH)

```
DH1 = DH(IK_A, SPK_B)   DH2 = DH(EK_A, IK_B)
DH3 = DH(EK_A, SPK_B)   DH4 = DH(EK_A, OPK_B)   # if a one-time prekey was available
SK  = KDF(DH1 || DH2 || DH3 [|| DH4])
```

PQXDH additionally encapsulates to Bob's PQ prekey: `(CT, SS) = KEM.Encaps(PQPK_B)`,
and `SK = KDF(DH1 || DH2 || DH3 [|| DH4] || SS)`. Alice sends IK_A, EK_A,
prekey identifiers and CT with her first message (AEAD-encrypted under SK or a
key derived from SK). Associated data AD = Encode(IK_A) || Encode(IK_B).

## Implementation rules

- **Verify signatures** on SPK and PQ prekeys before use; otherwise a
  malicious server substitutes its own keys.
- **One-time prekeys** must be deleted by Bob after use and handed out by the
  server only once; when they run out, sessions fall back to the signed
  prekey (weaker replay and forward-secrecy properties) - alert clients to
  upload more.
- Delete EK_A, the DH outputs and (PQXDH) SS after computing SK.
- PQXDH's KEM must be IND-CCA secure. If the KEM does not incorporate the
  public key into its ciphertext, append EncodeKEM(PQPKB) to AD to prevent
  KEM re-encapsulation attacks (spec section 4.12).
- Authentication still depends on users verifying identity keys (safety
  numbers) or key transparency; X3DH/PQXDH alone only authenticate "whoever
  owns IK_B".

## Use a library

Prefer a maintained, reviewed implementation over reimplementing; subtle
errors in prekey handling and KDF inputs are easy to make.

## Verify

- [ ] Prekey signatures verified; invalid bundle rejected.
- [ ] One-time prekeys single-use end to end (server and client).
- [ ] PQ component present in session setup (KEM ciphertext in the initial message).

## Checked

2026-10-31. Confirmed against the Signal X3DH and PQXDH specifications: prekey
bundle contents, signature verification and abort, last-resort PQ prekey, DH1-DH4
and KDF input order, AD = EncodeEC(IK_A) || EncodeEC(IK_B), deletion of one-time
prekeys, replay and forward-secrecy fallback without one-time prekeys, Kyber-1024
as the example KEM, KEM re-encapsulation note. Removed: ML-KEM naming of the
deployment, the libsignal and MLS claims, the 2023 date, the eprint source.

Method: documentation only; no commands were run.
