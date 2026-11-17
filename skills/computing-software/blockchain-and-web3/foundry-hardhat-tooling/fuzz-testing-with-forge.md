---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.fuzz-testing-with-forge
name: fuzz-testing-with-forge
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [forge-fuzz, vm-assume, bound-helper]
level: practitioner
status: draft
description: "Write fuzz tests with bound(), assume and runs configuration, and reproduce failures with seeds."
sources:
  - https://book.getfoundry.sh/forge/fuzz-testing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fuzzing
- Any test with parameters is fuzzed: `function testFuzz_X(uint256 a, address who)`.
- Constrain: `a = bound(a, 1, 1e24);` (preferred) or `vm.assume(cond)` (rejects inputs; too many rejects aborts).
- Config: `[fuzz] runs = 1000`, `seed`, or per-test `/// forge-config: default.fuzz.runs = 5000`.
- A failure prints a counterexample; failed cases persist in `cache/fuzz` and re-run first.
- Use `forge test --fuzz-seed 0x1` for reproducibility.

## Verify
- [ ] Counterexample from a deliberately wrong property is printed and re-runs deterministically.
