---
id: computing-software.blockchain-and-web3.ethereum-evm.eoa-vs-contract-accounts
name: eoa-vs-contract-accounts
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [eoa-vs-contract, externally-owned-account, contract-account, bc-eth-accounts]
level: intro
status: draft
description: "Tell externally owned accounts from contract accounts and know what fields each has (nonce, balance, code, storage root)."
sources:
  - https://ethereum.org/en/developers/docs/accounts/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EOA versus contract accounts
- An EOA is controlled by a private key; it has `nonce` and `balance`. It is the only account type that can start a transaction.
- A contract account has `nonce`, `balance`, `codeHash` and `storageRoot`; it runs code only when called.
- Tell them apart: `cast code <addr>` (Foundry) or JSON-RPC `eth_getCode`. `0x` means no code (EOA, or a contract not deployed yet).
- Gotcha: `eth_getCode` returns `0x` during a contract's own constructor, so `address.code.length == 0` is not a safe "is this an EOA" test in Solidity.
- Gotcha: an address can receive ETH before any contract exists there (CREATE2 addresses are predictable).

## Verify
- [ ] `cast code <known token address>` returns non-empty bytecode; `cast code <your wallet>` returns `0x`.
