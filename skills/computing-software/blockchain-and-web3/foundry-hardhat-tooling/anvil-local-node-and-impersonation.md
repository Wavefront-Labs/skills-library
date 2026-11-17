---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.anvil-local-node-and-impersonation
name: anvil-local-node-and-impersonation
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [anvil-node, anvil-fork, anvil-mine]
level: practitioner
status: draft
description: "Run a local dev chain or fork with anvil, control mining and time, and use dev accounts safely."
sources:
  - https://book.getfoundry.sh/reference/anvil/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# anvil
- `anvil` starts at `127.0.0.1:8545` with funded dev accounts (well-known mnemonic; never use those keys elsewhere).
- Fork: `anvil --fork-url $RPC --fork-block-number N`.
- Control: `anvil_mine`, `evm_increaseTime`, `evm_setNextBlockTimestamp`, `anvil_setBalance`, `anvil_impersonateAccount`, `evm_snapshot`/`evm_revert`.
- `--block-time 2` for interval mining; default is mine-on-transaction.
- Bind to localhost; exposing anvil publicly with impersonation enabled is unsafe.

## Verify
- [ ] After `evm_increaseTime` + mine, `cast block latest` shows the new timestamp.
