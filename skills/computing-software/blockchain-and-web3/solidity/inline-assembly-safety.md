---
id: computing-software.blockchain-and-web3.solidity.inline-assembly-safety
name: inline-assembly-safety
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [inline-assembly, memory-safe-assembly, free-memory-pointer, bc-sol-assembly]
level: sme
status: docs-checked
description: "Write small inline assembly blocks without corrupting the free memory pointer or layout."
sources:
  - https://docs.soliditylang.org/en/latest/assembly.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inline assembly
- Solidity keeps a free memory pointer at memory offset 0x40; allocatable memory starts at 0x80. Allocate by reading the pointer, using memory from there, and storing the updated pointer. Memory may hold old data, so do not assume zeros. Nothing is ever freed.
- The first 64 bytes (0x00-0x3f) are scratch space for short-term use. The 32 bytes at 0x60 must stay zero: they are the initial value for empty dynamic memory arrays.
- `assembly ("memory-safe") { ... }` promises the block only touches: memory you allocated yourself, memory Solidity allocated (within the bounds of an array you reference), the scratch space, or temporary memory after the free pointer's value at the block start (without updating the pointer). Zero-length memory operations may use any offset. Assigning Solidity memory variables inside assembly must also respect these ranges.
- Without the annotation, any assembly block containing a memory operation (or assigning to memory variables) disables the compiler's stack-to-memory moves and extra memory optimisations globally, for the via-IR pipeline.
- The restrictions apply even if the block reverts or terminates. Copying `returndatasize()` bytes to offset 0 is not memory-safe; copy to the free pointer instead.
- Claiming memory-safety wrongly causes incorrect, undefined behaviour that testing may not reveal. The `/// @solidity memory-safe-assembly` comment is deprecated; use the block annotation.
- Using up to 0x80 as scratch is allowed only if the free pointer is restored to a sane value and the word at 0x60 is restored to zero by the end of the block, or the block always terminates (for example ends in `revert`).

## Verify
- [ ] Review each annotated block against the allowed memory ranges above; add a differential test against an equivalent Solidity implementation where one exists.

## Checked

Confirmed against Solidity docs assembly.rst, Memory Management and Memory Safety sections (read in full). Removed: list of recommended uses (chainid, hashing, slot access), "everything the compiler checks is your job" and the fuzzing requirement, none of which are on the page.

Method: docs-checked 2026-11-09 against Solidity docs assembly.rst (raw rst on GitHub), Memory Management and Memory Safety sections.
