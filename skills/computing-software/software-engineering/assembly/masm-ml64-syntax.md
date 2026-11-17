---
id: computing-software.software-engineering.assembly.masm-ml64-syntax
name: masm-ml64-syntax
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, masm-ml64-syntax, asm-masm]
level: practitioner
status: draft
description: "MASM (ml64) x64 syntax: segments, PROC/ENDP, data types, PTR sizes, EXTERN, and building a console program that calls ExitProcess."
sources:
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/microsoft-macro-assembler-reference
  - https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MASM ml64 syntax
**Goal:** write and build x64 assembly with Microsoft's assembler.

```masm
option casemap:none
EXTERN ExitProcess:PROC

.data
msg   BYTE "Hello", 0
count DWORD 5

.code
main PROC
    sub  rsp, 40                 ; shadow space + alignment
    mov  eax, count
    xor  ecx, ecx
    call ExitProcess
main ENDP
END
```
Build: `ml64 hello.asm /link /subsystem:console /entry:main kernel32.lib`
- Segments: `.code`, `.data`, `.data?` (uninitialised), `.const`. There is no `.model` or `.386` in ml64.
- Types: `BYTE WORD DWORD QWORD REAL4 REAL8`; sizes in operands with `BYTE PTR`, `DWORD PTR`, ...
- `INVOKE`, `ADDR` and the high-level `.IF`/`.WHILE` flow directives are not available in 64-bit ml64 (check the MASM reference for exact support).
- Names are case-insensitive unless `option casemap:none`.
- Comments start with `;`.

## Gotchas
- Memory references to labels are RIP-relative automatically; no `[rel sym]` is needed.
- Follow the Win64 shadow-space rules before every call.

## Self-check
Add a call to `WriteConsoleA` with five arguments, remembering the fifth goes on the stack.
