---
id: computing-software.blockchain-and-web3.ethereum-evm.opcode-reading-and-disassembly
name: opcode-reading-and-disassembly
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [opcode-reading, bytecode-disassembly, function-dispatch]
level: advanced
status: draft
description: "Disassemble deployed bytecode, recognise the function selector dispatch and metadata trailer."
sources:
  - https://www.evm.codes/
  - https://docs.soliditylang.org/en/latest/metadata.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Opcodes and bytecode
- `cast disassemble 0x<code>` prints opcodes. Solidity bytecode starts with free-memory-pointer setup (`PUSH1 0x80 PUSH1 0x40 MSTORE`).
- Dispatcher: `CALLDATALOAD`, shift right 224 bits, compare against 4-byte selectors with `EQ`/`JUMPI`.
- Creation code (runs once, returns runtime code) differs from runtime code (what `eth_getCode` shows).
- A CBOR metadata blob at the end holds a hash of the metadata and the compiler version, so it changes the bytecode hash when sources change.
- Compare `forge inspect <C> bytecode` with `deployedBytecode`.

## Verify
- [ ] Selectors found in the dispatcher match `cast sig "transfer(address,uint256)"` (0xa9059cbb).
