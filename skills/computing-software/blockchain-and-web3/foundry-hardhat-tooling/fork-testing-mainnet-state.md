---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.fork-testing-mainnet-state
name: fork-testing-mainnet-state
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [forge-fork-test, create-select-fork, fork-block-pinning]
level: practitioner
status: draft
description: "Test against a fork of a live chain with pinned block numbers and RPC aliases."
sources:
  - https://book.getfoundry.sh/forge/fork-testing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fork testing
- `forge test --fork-url $RPC --fork-block-number N` or in tests `vm.createSelectFork("mainnet", N)`.
- Define aliases in `foundry.toml`: `[rpc_endpoints] mainnet = "${MAINNET_RPC_URL}"`.
- Pin a block so results are deterministic and RPC responses can be cached.
- Use `deal` and `vm.prank` to impersonate whales, but only in tests.
- Never put keys or full RPC URLs with tokens into committed config.

## Verify
- [ ] The same test passes twice in a row (cached) and fails if the pinned block is changed to a state before the target contract exists.
