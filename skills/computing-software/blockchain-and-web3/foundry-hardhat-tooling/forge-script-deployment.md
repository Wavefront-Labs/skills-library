---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.forge-script-deployment
name: forge-script-deployment
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [forge-script, broadcast-deploy, vm-startbroadcast, bc-tool-forge-ops]
level: practitioner
status: draft
description: "Write and run a Foundry deploy script with simulation, broadcast and verification."
sources:
  - https://book.getfoundry.sh/tutorials/solidity-scripting
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# forge script
```solidity
contract Deploy is Script {
    function run() external {
        vm.startBroadcast();          // uses --account / --private-key / --ledger
        new Vault();
        vm.stopBroadcast();
    }
}
```
- Dry run first: `forge script script/Deploy.s.sol --rpc-url $RPC` (simulation only).
- Broadcast: add `--broadcast --verify --etherscan-api-key $KEY`; use a keystore (`--account name`) or hardware wallet, not raw keys on the command line.
- Output lands in `broadcast/`; keep it for records (it holds addresses and tx hashes, no secrets).
- `--resume` retries pending transactions.

## Verify
- [ ] Simulation succeeds; after broadcast the receipt addresses match `broadcast/*/run-latest.json`.
