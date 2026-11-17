---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.testnet-deployment-and-verification
name: testnet-deployment-and-verification
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [testnet-deploy, etherscan-verify, forge-verify-contract, bc-tool-deploy]
level: practitioner
status: draft
description: "Rehearse on a testnet or fork and verify source with forge verify-contract."
sources:
  - https://book.getfoundry.sh/reference/forge/forge-verify-contract
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rehearsal and verification
- Rehearse the full deploy and post-deploy configuration on a testnet (Sepolia is a long-standing Ethereum testnet; check which testnets are currently supported) and on a mainnet fork.
- `forge verify-contract <addr> src/Vault.sol:Vault --chain sepolia --etherscan-api-key $KEY --constructor-args $(cast abi-encode "constructor(address)" 0x...)`.
- `forge verify-check <guid>` polls status.
- Save: compiler version, optimizer runs, evm version, constructor args and commit hash in release notes.
- Faucets are for test ETH only; never buy "testnet ETH".

## Verify
- [ ] The explorer's ABI matches `forge inspect Vault abi`.
