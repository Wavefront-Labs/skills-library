---
id: computing-software.cryptography-implementation.protocol-implementation.safety-numbers-and-key-transparency
name: safety-numbers-and-key-transparency
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, end-to-end-encryption, e2ee, key-transparency, safety-numbers, key-verification, akd, merkle-tree, identity-key-change]
level: sme
status: docs-checked
description: "Authenticate E2EE identity keys: safety numbers and QR verification, key-change warnings, and key transparency logs (WhatsApp AKD) that audit the key server."
sources: ["https://signal.org/blog/safety-number-updates/", "https://engineering.fb.com/2023/04/13/security/whatsapp-key-transparency/", "https://github.com/facebook/akd", "https://datatracker.ietf.org/wg/keytrans/about/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safety numbers and key transparency

End-to-end encryption is only end-to-end if you are talking to the right
key. The server that distributes identity keys can substitute its own
(man-in-the-middle) unless users or clients can check.

## Manual verification: safety numbers

- Show one value derived from both parties' keys, comparable by number or by a
  single QR scan, instead of separate per-party fingerprints. Signal's redesign
  reduced two comparisons to one and two scans to one after user studies found
  the old comparisons caused false positives, false negatives and confusion.
  WhatsApp's equivalent is a QR code and a 60-digit number, a hash of both
  parties' public keys, checked outside the app.
- Do not put phone numbers or other identifiers in the QR contents: Signal
  removed them after users unknowingly published them in screenshots.
- Stale published fingerprints (after a reinstall or new phone) make people
  conclude their communication is intercepted, then that verification is
  unreliable, so key-change messaging must be clear.
- Manual verification needs out-of-band coordination between two people, which
  is why automatic methods matter.

## Key transparency (automatic auditing)

The server maintains an append-only record of the mapping between an account
and its public identity key, as in WhatsApp's Auditable Key Directory (AKD):

1. Clients can get inclusion proofs that a given key mapping exists in the
   directory at the time of the request, and key history proofs.
2. Each directory change is accompanied by an audit proof placed in public
   storage, so anyone can verify the directory only grew (append-only), and
   third parties can act as public auditors.
3. Directory updates are batched into epochs; the publishing frequency is a
   tunable parameter.
4. Key transparency complements rather than replaces QR verification: a
   single client can run a check without a second person, and it helps when
   manual verification is impractical, for example in large groups.

AKD is open source Rust code (github.com/facebook/akd, now under the meta
organisation); WhatsApp's design builds on CONIKS and SEEMless with extensions
from Parakeet. The IETF KEYTRANS working group is working on a standardised
verifiability mechanism that has to be integrated into end-to-end protocols.

## Implementation notes

- Clients should not trust keys that come without proofs they can verify.
- Run self-monitoring (checking your own key history) in the background, with
  a clear alert path.
- Transparency detects substitution after the fact; combine it with key-change
  notices.

## Verify

- [ ] Safety number/QR verification implemented; key change warnings tested.
- [ ] If KT is used: inclusion and audit proofs verified by clients.
- [ ] Threat model states what the server can still do (for example withhold or delay).

## Checked

2026-11-01. Confirmed against Signal's safety number update post (single
comparison and scan, user-study problems, identifiers removed from QR codes,
stale fingerprints), the WhatsApp key transparency post (QR and 60-digit
number, append-only directory, inclusion and key history proofs, audit proofs
in public storage, epochs and tunable frequency, complements QR verification,
CONIKS, SEEMless, Parakeet), the AKD repository and the IETF KEYTRANS about
page. Removed: Signal's SHA-512 iteration detail, the deployments list (Apple,
Google, Cloudflare as auditor), VRF privacy claim and the epoch-trust advice
(not in the sources).
Method: documentation only; no commands were run.
