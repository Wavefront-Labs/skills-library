---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.hardhat-project-config
name: hardhat-project-config
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [hardhat-config, hardhat-networks, hardhat-compile, bc-tool-hardhat]
level: intro
status: draft
description: "Set up a Hardhat project: config file, compiler settings, networks and secrets via environment."
sources:
  - https://hardhat.org/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardhat config
```ts
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";
const config: HardhatUserConfig = {
  solidity: { version: "0.8.24", settings: { optimizer: { enabled: true, runs: 200 } } },
  networks: { sepolia: { url: process.env.SEPOLIA_RPC_URL, accounts: process.env.DEPLOYER_KEY ? [process.env.DEPLOYER_KEY] : [] } },
};
export default config;
```
- Commands: `npx hardhat compile`, `npx hardhat test`, `npx hardhat node`, `npx hardhat run scripts/deploy.ts --network sepolia`.
- Keep keys in env or a keystore plugin and out of git (`.env` in `.gitignore`).
- The config API differs between Hardhat 2 and 3; check the docs for your installed version.

## Verify
- [ ] `npx hardhat compile` emits artifacts and `npx hardhat test` passes.
