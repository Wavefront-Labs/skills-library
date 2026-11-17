---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.hardhat-testing-and-fixtures
name: hardhat-testing-and-fixtures
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [hardhat-test, loadfixture, hardhat-network-helpers]
level: practitioner
status: draft
description: "Write Mocha/Chai tests with loadFixture snapshots, time helpers and revert matchers."
sources:
  - https://hardhat.org/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardhat tests
```ts
import { loadFixture, time } from "@nomicfoundation/hardhat-network-helpers";
async function deploy() { const v = await ethers.deployContract("Vault"); return { v }; }
it("deposits", async () => { const { v } = await loadFixture(deploy); await expect(v.deposit({ value: 1n })).to.emit(v, "Deposit"); });
```
- `loadFixture` snapshots and reverts the in-process chain, faster than redeploying.
- Helpers: `time.increase`, `time.latest`, `mine`, `setBalance`, `impersonateAccount`.
- Matchers (`hardhat-chai-matchers`): `.to.be.revertedWithCustomError(contract, "Err").withArgs(...)`, `.to.changeEtherBalance`.
- Ethers v6 uses native `bigint`.

## Verify
- [ ] Tests run in isolation and in any order.
