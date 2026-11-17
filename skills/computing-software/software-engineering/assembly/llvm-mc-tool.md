---
id: computing-software.software-engineering.assembly.llvm-mc-tool
name: llvm-mc-tool
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, llvm-mc-tool, asm-llvm]
level: practitioner
status: draft
description: "Use llvm-mc to assemble, disassemble raw bytes and print instruction encodings for any target; the quickest way to check an encoding."
sources:
  - https://llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# llvm-mc assemble and disassemble
**Goal:** verify encodings and decode bytes without a full toolchain.

```sh
# encode: show bytes for an instruction
echo 'mov %rsp, %rbp' | llvm-mc -triple=x86_64 -show-encoding
#   movq %rsp, %rbp   # encoding: [0x48,0x89,0xe5]

# decode raw bytes
echo '0x48 0x89 0xe5' | llvm-mc -triple=x86_64 -disassemble
echo '0xc0 0x03 0x5f 0xd6' | llvm-mc -triple=aarch64 -disassemble     # ret

# Intel syntax output
echo '0x48 0x89 0xe5' | llvm-mc -triple=x86_64 -disassemble -output-asm-variant=1

# object file output with CPU feature
llvm-mc -triple=aarch64 -mattr=+sve -filetype=obj in.s -o out.o
```
- Input is read from a file or standard input; `-show-encoding` and `-show-inst` annotate output.
- Disassembly input is hex bytes (`0x..`) separated by spaces.
- `-triple=` selects the target; `-mattr=+feature` and `-mcpu=` choose extensions.
- Useful for checking whether an instruction is valid for a given architecture level: an unsupported one produces an error.

## Gotchas
- The default syntax for x86 is AT&T; use `-output-asm-variant=1` for Intel output (check `llvm-mc --help` on your version).
- Flag spelling changes across LLVM versions; run `llvm-mc --help` to confirm.

## Self-check
Decode `0xc3` and `0x00 0x00 0x80 0xd2` for both targets and explain the results.
