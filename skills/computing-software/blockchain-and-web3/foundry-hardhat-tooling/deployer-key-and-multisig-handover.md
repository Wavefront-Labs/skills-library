---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.deployer-key-and-multisig-handover
name: deployer-key-and-multisig-handover
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [deployer-key-hygiene, ownership-handover, safe-multisig-deploy]
level: practitioner
status: draft
description: "Deploy with a hardware wallet or keystore, then transfer privileges to a multisig and confirm."
sources:
  - https://docs.safe.global/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key hygiene and handover
- Use a fresh deployer address; fund it just enough; use `--ledger`/`--trezor` or an encrypted keystore (`cast wallet import`) rather than `--private-key`.
- After deploy: transfer ownership/admin roles to the multisig (two-step where available), then renounce deployer roles.
- Verify with reads: `owner()`, `hasRole(DEFAULT_ADMIN_ROLE, deployer)` is false, proxy admin owner is the multisig.
- Record the multisig signers, threshold and the procedure to rotate signers.
- Shell history and CI logs can leak secrets: pass secrets by environment or prompt.

## Verify
- [ ] A script asserts the deployer holds no privileges on any deployed contract.
