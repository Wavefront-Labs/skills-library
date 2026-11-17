---
id: mathematics.cryptographic-theory.symmetric-cryptography-theory.modes-of-operation-and-mac-constructions
name: modes-of-operation-and-mac-constructions
category: mathematics
field: cryptographic-theory
product: symmetric-cryptography-theory
tags: [symmetric-cryptography-theory, cryptography, block-cipher, prp, prf, pseudorandom-permutation, modes-of-operation, ecb, cbc, ctr, gcm, nonce, iv, birthday-bound, mac, cbc-mac, cmac, hmac, merkle-damgard, length-extension, sponge, sha-3, encrypt-then-mac, authenticated-encryption, aead, ind-cpa, euf-cma, cryptographic-theory]
level: advanced
status: gated
description: "Reason about block-cipher modes and MAC/hash constructions as mathematics: what each mode assumes of the cipher and IV, birthday bounds, length extension, and generic composition."
sources: ["Katz & Lindell, Introduction to Modern Cryptography (CRC)", "Boneh & Shoup, A Graduate Course in Applied Cryptography (online draft)", "NIST SP 800-38A/38D"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modes of operation and MAC constructions

**Goal:** given a symmetric construction, say what it assumes, what security it
achieves, and where its bound runs out. (For choosing a library primitive in code, see
`computing-software.cryptography-implementation.applied-cryptography.choosing-primitives-and-modes`.)

## 1. The abstraction: block ciphers as PRPs
Model a block cipher E_k on n-bit blocks as a **pseudorandom permutation**: no efficient
adversary distinguishes E_k from a random permutation. The **PRP/PRF switching lemma**
says a PRP is also a PRF with an extra distinguishing advantage ≤ q²/2^{n+1} for q
queries — the root of every birthday bound below.

## 2. Modes, as theorems
| Mode | Requirement | Security | Breaks when |
|---|---|---|---|
| ECB | none | not IND-CPA (deterministic, equal blocks leak) | always — never "secure" |
| CBC | **unpredictable** random IV | IND-CPA up to ~q·ℓ ≈ 2^{n/2} blocks | IV predictable (BEAST-style chosen-plaintext) |
| CTR | **unique** nonce/counter blocks | IND-CPA, advantage ≈ σ²/2^n | any counter block reused → `C1 ⊕ C2 = P1 ⊕ P2` |
| GCM | unique 96-bit nonce | AEAD (IND-CCA + integrity) | nonce reuse leaks the GHASH key H → forgeries (gated: unconfirmed, source is paywalled or blocked) |

Key points:
- **Unique ≠ random ≠ unpredictable.** CTR needs uniqueness; CBC needs unpredictability.
- Birthday bound: with a 64-bit block (3DES, Blowfish) 2^32 blocks ≈ 32 GB is enough
  for collisions (Sweet32). For AES-GCM, NIST SP 800-38D caps total invocations at 2^32 per key with random (RBG-based) 96-bit IVs and recommends 96-bit IVs (confirmed in the text). Sweet32 states the 64-bit-block birthday bound is about 32 GB (confirmed).
- None of CBC/CTR give integrity: IND-CPA only. Padding-oracle attacks on CBC are what
  happens when you ignore that.

## 3. MACs
Security goal: **EUF-CMA** — existentially unforgeable under chosen-message attack.
- **CBC-MAC** (zero IV, last block): secure only for **fixed-length** messages. For
  variable length, given tags t1 on m1 and t2 on m2, forge on m1‖(m2's first block ⊕ t1)‖… .
  Fixes: **CMAC** (subkey-masked final block), or encrypt the tag with a second key (ECBC).
- **Hash-based:** `H(k‖m)` with a Merkle-Damgård hash (SHA-256) is broken by
  **length extension** — from H(k‖m) and |k‖m| compute H(k‖m‖pad‖m'). **HMAC**
  `H((k⊕opad) ‖ H((k⊕ipad) ‖ m))` is a PRF if the compression function is (Bellare 2006 (gated: unconfirmed, source is paywalled or blocked)).
  SHA-3/Keccak (sponge) and truncated SHA-512/256 resist length extension.
- Tag length t: forgery by guessing succeeds w.p. 2^{−t} per attempt. 64+ bits for most uses.

## 4. Generic composition (Bellare-Namprempre 2000)
- **Encrypt-then-MAC** (MAC over ciphertext, separate keys): IND-CCA + INT-CTXT from
  IND-CPA + strongly unforgeable MAC. Always safe.
- MAC-then-Encrypt (TLS ≤1.2): not generically secure; specific instances survive.
- Encrypt-and-MAC (SSH): MAC may leak plaintext equality; not generically secure.

## 5. Hash design principles (for proofs)
Merkle-Damgård: collision-resistant compression function + length-strengthening padding
⇒ collision-resistant hash. It does **not** give PRF or random-oracle behaviour — hence
length extension. Generic collision cost 2^{n/2}; preimage 2^n.

## Uncertainty notes
Bounds are stated to leading order; exact constants differ by text. Practical data
limits per key are guidance from NIST/IETF discussions, not proofs — consult the
current standard for a deployed system.

## Verify
- [ ] For each mode you name its IV/nonce requirement (unique vs unpredictable).
- [ ] You can state the birthday bound for the block size in use.
- [ ] CBC-MAC is only used for fixed-length inputs (or CMAC is used).
- [ ] No `H(key‖message)` with an MD hash; HMAC or a sponge instead.
- [ ] Composition is encrypt-then-MAC (or a proven AEAD) with independent keys.
