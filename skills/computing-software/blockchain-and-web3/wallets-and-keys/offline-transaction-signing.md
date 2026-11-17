---
id: computing-software.blockchain-and-web3.wallets-and-keys.offline-transaction-signing
name: offline-transaction-signing
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [offline-signing, raw-transaction-broadcast, cast-mktx]
level: advanced
status: draft
description: "Build, sign offline and broadcast an Ethereum transaction (cold-signing flow)."
sources:
  - https://book.getfoundry.sh/reference/cast/cast-mktx
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offline signing
1. Online machine: gather `nonce` (`cast nonce`), `chain-id` (`cast chain-id`), fee data (`cast base-fee`, `cast gas-price`).
2. Offline machine: `cast mktx <to> --value 0.1ether --nonce N --gas-limit 21000 --max-fee-per-gas ... --priority-gas-price ... --chain 1 --private-key-or-keystore options` yields raw signed hex.
3. Online: `cast publish <rawhex>`.
- Check chain id: a transaction signed for another chain id will not be valid (EIP-155 replay protection).
- Keep the signing machine air-gapped; transfer data via QR or removable media you control.

## Verify
- [ ] `cast decode-tx <rawhex>` shows the intended recipient, value and chain id before broadcasting.
