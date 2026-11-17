---
id: computing-software.blockchain-and-web3.ethereum-evm.state-trie-and-merkle-proofs
name: state-trie-and-merkle-proofs
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [state-trie, merkle-patricia-trie, eth-getproof]
level: advanced
status: draft
description: "Explain the Merkle Patricia state trie, state root in block headers and how eth_getProof lets a light client verify account or storage values."
sources:
  - https://ethereum.org/en/developers/docs/data-structures-and-encoding/patricia-merkle-trie/
  - https://eips.ethereum.org/EIPS/eip-1186
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# State trie and proofs
- World state maps address to account (nonce, balance, storageRoot, codeHash). Each block header commits to the `stateRoot`, plus `transactionsRoot` and `receiptsRoot`.
- Every account has its own storage trie; keys are keccak-256 hashed slot numbers.
- `eth_getProof(address, [slots], block)` (EIP-1186) returns account and storage proofs that can be checked against a trusted `stateRoot`.
- Use: bridges and light clients verify a value without trusting the RPC provider.
- Gotcha: pruned nodes do not serve proofs for old blocks; archive nodes do.

## Verify
- [ ] The proof's root hash recomputes to the header `stateRoot` for the same block.
