---
id: computing-software.blockchain-and-web3.bitcoin.multisig-and-timelocks-script
name: multisig-and-timelocks-script
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [bitcoin-multisig, checklocktimeverify, miniscript]
level: advanced
status: draft
description: "Describe m-of-n multisig, CLTV/CSV timelocks and miniscript/descriptors at a conceptual and tooling level."
sources:
  - https://developer.bitcoin.org/devguide/transactions.html
  - https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multisig and timelocks
- `OP_CHECKMULTISIG` m-of-n; in segwit use P2WSH; keys sorted for deterministic addresses (`sortedmulti` in descriptors).
- `OP_CHECKLOCKTIMEVERIFY` (absolute) and `OP_CHECKSEQUENCEVERIFY` (relative) restrict when an output is spendable.
- Output descriptors express scripts and keys textually, e.g. `wsh(sortedmulti(2,<xpubA>,<xpubB>,<xpubC>))#checksum`; `bitcoin-cli getdescriptorinfo` adds the checksum and `deriveaddresses` lists addresses.
- Back up descriptors, not just seeds, for multisig: recovery requires all cosigner xpubs.

## Verify
- [ ] `deriveaddresses` gives the same first address on two independent tools.
