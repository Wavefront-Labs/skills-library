---
id: computing-software.blockchain-and-web3.wallets-and-keys.multisig-wallet-design
name: multisig-wallet-design
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [multisig-custody, safe-wallet, signer-diversity]
level: advanced
status: draft
description: "Design an m-of-n custody scheme with signer diversity, recovery procedure and tested restore."
sources:
  - https://docs.safe.global/
  - https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multisig custody
- Choose m-of-n so that losing (n - m) keys is survivable and compromising (m - 1) keys is not enough (e.g. 2-of-3).
- Diversity: different device vendors, locations and people; avoid all keys sharing one failure mode.
- Ethereum: Safe smart accounts (signer set, threshold, modules, guards); keep the module list minimal and audited.
- Bitcoin: descriptor-based multisig; store descriptors and all cosigner xpubs.
- Document: signing ceremony, how to add/replace a signer, and an emergency procedure.
- Test recovery annually with a small balance.

## Verify
- [ ] Tabletop: restore access using only documented materials and n-1 original keys.
