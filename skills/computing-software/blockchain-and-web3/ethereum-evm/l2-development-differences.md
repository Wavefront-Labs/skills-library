---
id: computing-software.blockchain-and-web3.ethereum-evm.l2-development-differences
name: l2-development-differences
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [l2-differences, chain-id-replay, l1-data-fee]
level: practitioner
status: draft
description: "List differences that bite when deploying EVM contracts to L2s: opcode and precompile differences, fees, block.number, finality."
sources:
  - https://ethereum.org/en/developers/docs/scaling/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# L2 differences
- Fees = L2 execution + L1 data posting fee; estimate with the chain's own tooling, not only `eth_estimateGas`.
- `block.number` and `block.timestamp` semantics differ on some chains; read that chain's docs.
- Some chains lack specific opcodes or add them later (check `PUSH0`, transient storage); compile with an `evm_version` the target supports.
- Bind signatures to `chainId` (EIP-712 domain) to prevent cross-chain replay.
- Bridged token addresses differ per chain; never assume the same address.
- Sequencer downtime: oracle consumers should check the chain's sequencer-uptime feed when one is offered.

## Verify
- [ ] Deployment and a smoke test pass on the target chain's testnet.
