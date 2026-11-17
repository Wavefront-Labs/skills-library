---
id: computing-software.cryptography-implementation.protocol-implementation.double-ratchet-e2ee-design
name: double-ratchet-e2ee-design
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, double-ratchet, x3dh, signal-protocol, end-to-end-encryption, forward-secrecy, post-compromise-security, out-of-order-messages, skipped-message-keys, e2ee]
level: sme
status: docs-checked
description: "Signal-style E2EE messaging: X3DH initial key agreement, the double ratchet's DH and symmetric chains, out-of-order delivery, and skipped-key storage bounds."
sources: ["https://signal.org/docs/specifications/doubleratchet/", "https://signal.org/docs/specifications/x3dh/", "https://signal.org/docs/specifications/xeddsa/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Double-ratchet-style end-to-end encryption design

This is the protocol class described by the Signal specifications — covered here as **design-level implementation guidance**, not
a from-scratch crypto primitive: use the published Signal specification and
an audited library rather than re-deriving this yourself. The
value of this skill is knowing the moving parts well enough to integrate
and debug correctly.

## X3DH — the asynchronous initial key agreement

Messaging apps need to establish a shared secret **without both parties
being online simultaneously** (the whole "send a message to someone
offline" use case) — a plain Diffie-Hellman exchange requires both sides
present at once. X3DH (Extended Triple Diffie-Hellman) solves this by
having the recipient publish a **prekey bundle** in advance: an identity
key, a signed prekey (rotated periodically, signed by the identity key to
prevent substitution), and optionally several one-time prekeys. The sender
fetches this bundle from a server, performs several DH operations combining
their own keys with the recipient's bundle, and derives a shared secret
without the recipient needing to be online at that moment.
- **One-time prekeys provide additional forward secrecy** for the very
  first message but are a *consumable resource* — the server must track
  which ones have been used and never hand out the same one-time prekey
  twice; running out of one-time prekeys degrades (gracefully, per spec) to
  using only the signed prekey, which is still secure but loses that
  specific extra protection for first-message forward secrecy.
- **The signed prekey needs periodic rotation** (the X3DH spec gives once a week
  or once a month as examples) — an unrotated signed prekey that's compromised exposes every
  future first-message key agreement using it until rotated.

## The double ratchet: two ratchets, two different jobs

Once an initial shared secret (the "root key") exists, the double ratchet
derives a fresh encryption key for every message, with two interacting
mechanisms:
- **DH ratchet (asymmetric/slow):** each time the conversation "turns"
  (the other party sends after you last sent), a fresh ephemeral DH
  exchange mixes new randomness into the root key. This is what provides
  **post-compromise security** — even if a past session key is
  compromised, future messages become secure again once a new DH ratchet
  step occurs, because the new root key material includes a fresh secret
  the attacker never saw.
- **Symmetric-key ratchet (fast):** within a single "turn" (sending
  multiple messages before the other party replies), each message key is
  derived from a chain key via a one-way KDF step, and the chain key is
  then advanced/discarded — this is what provides **forward secrecy per
  message**: compromising one message key doesn't expose prior or
  (without the DH ratchet's extra step) future messages in the same chain,
  because deriving backward from a one-way KDF output isn't feasible.
- **These solve different problems** — forward secrecy (past messages safe
  if a current key leaks) and post-compromise security (future messages
  become safe again after a compromise, once ratcheting continues) are not
  the same guarantee, and conflating them in documentation is a design
  mistake.

## Out-of-order delivery and skipped message keys

Real networks deliver messages out of order. The symmetric ratchet chain
is sequential by construction, so receiving message N+2 before N+1 means
the chain key must be advanced past the "skipped" message N+1's position —
the implementation must **derive and store the skipped message key** so
that if message N+1 arrives later, it can still be decrypted with the key
that was already derived and set aside, rather than failing or needing a
resend.
- **This storage must be bounded.** An attacker (or a buggy/malicious peer)
  sending a message with a far-future chain position forces the receiver
  to derive and store a potentially huge number of skipped keys — an
  unbounded skipped-key store is a memory-exhaustion DoS vector. The
  Double Ratchet spec defines a `MAX_SKIP` constant, the maximum number of
  message keys that can be skipped in a single chain, to be set high enough to
  tolerate routine lost or delayed messages but low enough that a malicious
  sender cannot trigger excessive computation; enforce an explicit limit and
  do not store skipped keys unboundedly.
- **Skipped keys that are never claimed must eventually be deleted** (both
  for the DoS-bound reason above and because an unused stored key sitting
  around indefinitely is extra material an attacker who compromises storage
  could use) — apply a time or count-based eviction policy.

## Verify

- [ ] Use an audited implementation rather than
      a from-scratch reimplementation of the ratchet math.
- [ ] One-time prekey consumption is tracked server-side with no reuse, and
      the degrade-to-signed-prekey-only path is tested, not just the
      happy path with prekeys available.
- [ ] Signed prekeys are rotated on a defined schedule.
- [ ] Skipped-message-key storage has an explicit, enforced maximum count
      and maximum chain-position jump accepted per step.
- [ ] Stored skipped keys that go unclaimed are evicted on a bounded
      schedule, not retained indefinitely.
- [ ] The distinction between forward secrecy and post-compromise security
      is reflected correctly in any documentation/claims made about the
      system's guarantees — not used interchangeably.

This skill is an orientation map, not a substitute for the full Signal
specifications or an audited library.

## Checked

2026-11-01. Confirmed against the X3DH and Double Ratchet specifications:
prekey bundle contents, signed prekey replaced at an interval such as weekly
or monthly, server deleting handed-out one-time prekeys and omitting them when
exhausted, DH ratchet versus symmetric-key chains, PN and N counters used to
store skipped message keys, `MAX_SKIP`, and deletion of used message keys.
Removed: `libsignal` and WhatsApp references, the "reference implementation
caps stored keys" claim, and the round-trip-skipping example (not in the
sources). The claim about gradually degrading to the signed prekey is the
X3DH bundle-without-OPK case.
Method: documentation only; no commands were run.
