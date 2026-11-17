---
id: computing-software.blockchain-and-web3.solidity.optimizer-and-via-ir
name: optimizer-and-via-ir
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [solc-optimizer, via-ir, optimizer-runs, bc-sol-gas]
level: practitioner
status: docs-checked
description: "Configure optimizer runs and via-IR, and measure the effect on deploy size and runtime gas."
sources:
  - https://docs.soliditylang.org/en/latest/internals/optimizer.html
  - https://docs.soliditylang.org/en/latest/using-the-compiler.html
  - https://docs.soliditylang.org/en/latest/ir-breaking-changes.html
  - https://eips.ethereum.org/EIPS/eip-170
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimizer
- Command line: `solc --optimize --bin file.sol`; standard JSON: `settings.optimizer.enabled` (default false) and `settings.optimizer.runs` (default 200). The optimizer is off unless you enable it.
- `runs` estimates how often each opcode of the deployed code executes over the contract's life: it trades deploy cost (code size) against runtime cost. `runs = 1` gives short but expensive code; larger values give longer but cheaper code; the maximum is 2**32-1. It is not the number of optimizer iterations (the optimizer repeats until nothing improves).
- IR pipeline: `--via-ir` on the command line or `"viaIR": true` in standard JSON. It generates code through Yul, enabling optimisation across functions, and can move local variables to memory to avoid stack-too-deep errors, provided inline assembly respects the memory model. There are small semantic differences from the old code generator (for example state variable initialisation order under inheritance); read the IR breaking-changes page before switching.
- Contract code size is capped at 0x6000 bytes (24576) by EIP-170: creation fails if the returned runtime code is larger. Compare your compiled runtime bytecode size with it.
- Run the full test suite with the final settings, and deploy exactly the build you tested and verified.

## Verify
- [ ] Runtime bytecode size is under 24576 bytes with margin, and tests pass under the final compiler settings.

## Checked

Confirmed against Solidity docs internals/optimizer.rst (runs semantics and maximum, not iterations), using-the-compiler.rst (optimizer default off, runs default 200, viaIR option), ir-breaking-changes.rst (via-ir flag, semantic differences), assembly.rst (stack-too-deep memory moves) and the EIP-170 text (0x6000). Removed: Foundry `optimizer`, `optimizer_runs`, `via_ir` and `forge build --sizes` references and Hardhat settings (Foundry book not readable), the claim that via-IR is slower to compile, and the "optimizer bugs are rare" aside.

Method: docs-checked 2026-11-09 against Solidity docs optimizer, using-the-compiler, ir-breaking-changes, assembly (raw rst on GitHub) and EIP-170 (raw EIPs repository).
