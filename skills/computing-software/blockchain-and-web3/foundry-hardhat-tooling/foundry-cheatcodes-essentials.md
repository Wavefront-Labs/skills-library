---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.foundry-cheatcodes-essentials
name: foundry-cheatcodes-essentials
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [foundry-cheatcodes, vm-prank, vm-deal]
level: practitioner
status: draft
description: "Use prank, deal, warp, roll, expectRevert, expectEmit, mockCall and label cheatcodes correctly."
sources:
  - https://book.getfoundry.sh/cheatcodes/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cheatcodes
- `vm.prank(addr)` next call only; `vm.startPrank`/`stopPrank` for several. `vm.prank(addr, origin)` also sets tx.origin.
- `vm.deal(addr, amt)` sets ETH balance; `deal(token, addr, amt)` (forge-std) sets ERC-20 balance.
- `vm.warp(ts)`, `vm.roll(n)` change timestamp and block number.
- `vm.expectRevert(bytes)` applies to the next external call; place it right before.
- `vm.mockCall(target, data, ret)`; `vm.label(addr, "Alice")` readable traces.
- `makeAddr("alice")` and `vm.sign(pk, digest)` for actors and signatures.
- Gotcha: `vm.expectRevert` followed by an internal call or a cheatcode consumes the expectation on the wrong call.

## Verify
- [ ] Each privileged function has a test using prank with a non-owner.
