---
id: computing-software.blockchain-and-web3.solidity.erc20-implementation
name: erc20-implementation
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [erc20-token, approve-allowance, token-decimals, bc-sol-erc]
level: practitioner
status: docs-checked
description: "Implement or integrate ERC-20 correctly: decimals, allowances, return values and non-standard tokens."
sources:
  - https://eips.ethereum.org/EIPS/eip-20
  - https://docs.openzeppelin.com/contracts/5.x/erc20
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ERC-20
- Required by EIP-20: `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve`, `allowance`; events `Transfer`, `Approval`. `name`, `symbol` and `decimals` are optional and other contracts must not expect them.
- `decimals` is only a display hint (OpenZeppelin docs): all contract arithmetic is on integers, so never hard-code a token's decimals; read them.
- EIP-20: callers must handle a `false` return from `transfer`/`transferFrom` and must not assume `false` never happens.
- Approval race: EIP-20 says clients should set an allowance to 0 before setting it to another value.
- OpenZeppelin's `ERC20` is the documented base implementation to start from.

## Verify
- [ ] Test suite includes transfer to self, zero amounts and exceeding allowance.

## Checked

2026-11-02. Confirmed against EIP-20 (function list, optional metadata, false-return rule, allowance-reset note) and the OpenZeppelin 5.x ERC20 page (decimals display only). Removed as not stated on those pages: USDC decimals, SafeERC20.safeTransfer, increaseAllowance, fee-on-transfer and rebasing token advice. The "Verify" item is a test suggestion, not a claim.
Method: documentation only; no commands were run.
