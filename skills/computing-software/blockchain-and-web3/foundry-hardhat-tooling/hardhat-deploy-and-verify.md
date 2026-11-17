---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.hardhat-deploy-and-verify
name: hardhat-deploy-and-verify
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [hardhat-ignition, contract-verification-hardhat, hardhat-verify]
level: practitioner
status: draft
description: "Deploy with Ignition or scripts and verify source on a block explorer."
sources:
  - https://hardhat.org/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deploy and verify
- Ignition: declarative modules in `ignition/modules/*.ts`; run `npx hardhat ignition deploy ignition/modules/Vault.ts --network sepolia`. It tracks deployments and can resume.
- Verify: `npx hardhat verify --network sepolia <address> <constructor args>`; needs an explorer API key in config.
- Verification fails if the compiler version, optimizer settings, or libraries differ from the deployment; match them exactly.
- Keep deployed addresses in a committed deployments file per chain.

## Verify
- [ ] Explorer shows a green "verified" source tab matching your repo commit.
