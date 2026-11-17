---
id: computing-software.blockchain-and-web3.ethereum-evm.evm-stack-memory-storage
name: evm-stack-memory-storage
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [evm-data-areas, stack-machine, calldata, bc-evm-execution]
level: practitioner
status: draft
description: "Distinguish the EVM's stack, memory, storage, calldata, code and returndata and their cost and persistence."
sources:
  - https://ethereum.org/en/developers/docs/evm/
  - https://www.evm.codes/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EVM data areas
- Stack: up to 1024 items of 32 bytes, accessed by DUP/SWAP; only the top 16 are reachable (the "stack too deep" error source).
- Memory: byte-addressed, cleared per call frame, cost grows quadratically with size.
- Storage: persistent key-value of 32-byte slots per contract; most expensive.
- Calldata: read-only input; cheaper than memory copies.
- Code, returndata (`RETURNDATASIZE`/`RETURNDATACOPY`) and transient storage (`TLOAD`/`TSTORE`, EIP-1153, on recent forks) complete the list.
- Inspect: `cast disassemble <bytecode>` or `forge inspect <Contract> assembly`.

## Verify
- [ ] You can map a Solidity variable (local, memory, storage, calldata) to its EVM area.
