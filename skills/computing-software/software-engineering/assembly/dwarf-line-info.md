---
id: computing-software.software-engineering.assembly.dwarf-line-info
name: dwarf-line-info
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, dwarf-line-info, asm-debug-info]
level: advanced
status: docs-checked
description: "Give assembly sources DWARF line info: as -g/--gdwarf-N, .file/.loc directives, NASM -g/-F, checking with objdump and readelf, keeping debug data."
sources:
  - https://sourceware.org/binutils/docs/as/Overview.html
  - https://sourceware.org/binutils/docs/as/File.html
  - https://sourceware.org/binutils/docs/as/Loc.html
  - https://www.nasm.us/doc/nasm02.html
  - https://sourceware.org/binutils/docs/binutils/objdump.html
  - https://sourceware.org/binutils/docs/binutils/readelf.html
  - https://sourceware.org/binutils/docs/binutils/objcopy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DWARF line info for assembly sources
**Goal:** debug at assembly source level (source file and line for each instruction).

```sh
as -g --gdwarf-5 prog.s -o prog.o            # line table for the .s source
nasm -f elf64 -g prog.asm -o prog.o           # NASM: -g enables debug info
```
- `as -g` (`--gen-debug`) generates debugging information for each assembler source line in the target's preferred format (STABS, ECOFF or DWARF2). `--gdwarf-N` (2 to 5) asks for DWARF explicitly; it is supported only by some targets. With DWARF, `.debug_info` and `.debug_line` are only emitted when the assembly file does not generate its own.
- `--gdwarf-sections` creates `.debug_line.foo` per code section instead of one `.debug_line`.
- Hand-written tables: `.file fileno "name"` assigns a name to the `.debug_line` file table (unique positive index; the table is shared with `.debug_info`), and `.loc fileno lineno [column] [options]` adds a row for the immediately following instruction. Options include `basic_block`, `prologue_end`, `epilogue_begin`, `is_stmt value`, `isa value`, `discriminator value`, `view value`. It is an error for the input to generate a non-empty `.debug_line` and also use `.loc`. The extended `.file fileno [dirname] filename [md5 value]` form needs `-gdwarf-5`.
- NASM: `-g` enables debug output in the default format of the selected output format (silently ignored if that format has none); `-F format` selects the format and, in NASM 2.03.01 and later, implies `-g`. `nasm -h` lists the formats per output format.
- Verify: `readelf --debug-dump=decodedline prog` (or `-wL`), `objdump --dwarf=decodedline` (`-WL`), and `objdump -d -l prog` which labels the disassembly with file and line numbers.
- Keeping debug data: `objcopy --only-keep-debug foo foo.dbg` copies the debugging sections, `strip --strip-debug foo` removes them, and `objcopy --add-gnu-debuglink=foo.dbg foo` links the two. `--only-keep-debug` is meant for fully linked files, not objects.

## Gotchas
- Stripping removes debug sections; keep an unstripped copy or a separate debug file as above.
- `.loc` and a generated `.debug_line` cannot be mixed in one input.

## Self-check
Assemble with `as -g`, then run `objdump -d -l` and confirm each instruction is labelled with the right source line.

## Checked
Method: docs-checked 2026-11-09 against the GNU as pages Overview (options), File and Loc, NASM manual chapter 2 (-F and -g options), and the binutils objdump, readelf, objcopy and strip pages. Dropped unconfirmed gcc and clang usage, gdb and addr2line commands, macro line-table behaviour and the DWARF version mixing advice.
