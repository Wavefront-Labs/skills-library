---
id: computing-software.blockchain-and-web3.solidity.receive-fallback-and-payable
name: receive-fallback-and-payable
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [receive-fallback, send-ether, payable-functions]
level: practitioner
status: docs-checked
description: "Define receive/fallback correctly and send ETH with call rather than transfer."
sources:
  - https://docs.soliditylang.org/en/latest/contracts.html#receive-ether-function
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# receive and fallback
- A contract has at most one `receive() external payable { ... }` (no `function` keyword, no arguments, no return). It runs on a call with empty calldata, such as a plain ETH transfer.
- `fallback()` (optionally `payable`, optionally taking `bytes calldata` and returning `bytes memory`) runs when no function matches, or when calldata is empty and there is no `receive`. A `payable` fallback also takes plain ETH transfers if no `receive` exists, so define both to tell transfers from interface mix-ups.
- A contract with neither a `receive` nor a payable fallback throws on a plain ETH transfer, but it can still be sent ETH as a coinbase (block reward) recipient or as a `selfdestruct` target and cannot react. So `address(this).balance` can exceed your own accounting; do not rely on it.
- Send ETH with `(bool ok,) = to.call{value: amt}(""); require(ok);`. `send` and `transfer` are deprecated and forward only a 2300 gas stipend, so a receiver that writes to storage, creates a contract, calls out or sends ETH will fail.
- Update state before sending, or use a reentrancy guard.

## Verify
- [ ] A test sends ETH to a contract whose `receive` writes to storage and the payout still succeeds.

## Checked

Confirmed against the Solidity docs sources (contracts/functions.rst, control-structures.rst): receive and fallback rules, 2300 gas stipend and the operations that exceed it, send/transfer deprecation, coinbase and selfdestruct inflows, and the call-with-value example. Corrected: fallback also runs on empty calldata when no receive exists (earlier wording said non-empty calldata). Removed the specific call-heavy-hook Foundry wording.

Method: docs-checked 2026-11-09 against Solidity docs contracts/functions.rst and control-structures.rst (raw rst on GitHub).
