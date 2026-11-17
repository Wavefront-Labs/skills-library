---
id: computing-software.cryptography-implementation.applied-cryptography.merkle-tree-hashing-with-domain-separation
name: merkle-tree-hashing-with-domain-separation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, merkle-tree-hashing, merkle-tree, rfc-6962, rfc-9162, inclusion-proof, consistency-proof, second-preimage, transparency-log]
level: advanced
status: verified
description: "Build Merkle trees safely: RFC 6962 leaf/node prefixes, unbalanced-tree splitting, inclusion and consistency proofs, and the second-preimage pitfalls."
sources: ["https://www.rfc-editor.org/rfc/rfc6962#section-2.1", "https://www.rfc-editor.org/rfc/rfc9162"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merkle tree hashing with domain separation

## RFC 6962 / 9162 definition
```
MTH({})      = SHA-256()                          # empty tree
MTH({d0})    = SHA-256(0x00 || d0)                # leaf hash
MTH(D[n])    = SHA-256(0x01 || MTH(D[0:k]) || MTH(D[k:n]))  # k = largest power of two < n
```
- The 0x00 / 0x01 prefixes separate leaves from interior nodes. without them, an interior node value can be
  presented as a leaf, giving a second preimage for a different tree (run: with no prefixes,
  the 2-leaf tree [a, b] and the 1-leaf tree [H(a)||H(b)] share a root).
- Unbalanced trees split at the largest power of two below n. Do **not** duplicate the last node to fill the level
  (Bitcoin-style duplication gives the same root for [1,2,3] and [1,2,3,3]; RFC 6962 roots differ; both run).

## Proofs
- **Inclusion (audit path):** leaf index, tree size, and the sibling hashes from leaf to root. The verifier must use
  the index and tree size to know at each level whether the sibling is left or right; RFC 9162 2.1.3.2 gives the
  exact algorithm.
- **Consistency:** proves tree of size m is a prefix of tree of size n; required for append-only logs so clients
  can detect a forked or rewritten log.

## Implementation checklist
- Hash the leaf content's canonical encoding, not a re-serialised object.
- Fix the hash function per tree and record it; mixing SHA-256 and SHA-512/256 across versions needs a version tag.
- Bind the tree size into whatever you sign (signed tree head = size, root, timestamp, signature).
- Use an existing implementation for proofs (Trillian, Tessera, `transparency-dev/merkle` in Go);
  off-by-one errors in proof verification are common.

## Gotchas
- Sorting sibling pairs before hashing (some smart-contract libraries) loses position information; only acceptable if
  the protocol is designed for it.
- An empty or single-leaf tree is a special case; test it.

## Verify
- [ ] RFC 9162 test vectors for roots and proofs pass. Reference values (run): empty tree root is SHA-256 of the empty string,
  `e3b0c442...b855`; the leaf hash of the empty string is `6e340b9c...a01d`; a 7-leaf tree's inclusion proofs for all
  indices verify with the RFC 9162 2.1.3.2 algorithm, and swapping two proof hashes fails.
- [ ] A proof with a swapped sibling order fails.
- [ ] Leaf and node hashing use different prefixes.
