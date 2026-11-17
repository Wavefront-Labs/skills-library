---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.forge-test-structure-and-assertions
name: forge-test-structure-and-assertions
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [forge-test, test-setup, forge-std-assertions, bc-tool-forge-test]
level: intro
status: draft
description: "Structure Foundry tests with setUp, naming conventions, assertions and filters."
sources:
  - https://book.getfoundry.sh/forge/tests
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# forge tests
```solidity
import {Test} from "forge-std/Test.sol";
contract VaultTest is Test {
    Vault v;
    function setUp() public { v = new Vault(); }
    function test_Deposit() public { v.deposit{value: 1 ether}(); assertEq(v.total(), 1 ether); }
    function testFuzz_Deposit(uint96 x) public { vm.assume(x > 0); /* ... */ }
    function test_RevertWhen_ZeroDeposit() public { vm.expectRevert(); v.deposit(); }
}
```
- Run: `forge test`, `-vvv` shows traces for failures, `--match-contract`, `--match-test`, `-vvvv` includes setup traces.
- Names beginning `test` run; `testFail` is deprecated, use `vm.expectRevert`.
- Config in `foundry.toml`.

## Verify
- [ ] `forge test -vvv` passes; a deliberately broken assertion shows a readable trace.
