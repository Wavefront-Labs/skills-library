---
id: computing-software.software-engineering.nim.link-time-and-size-optimization
name: link-time-and-size-optimization
category: computing-software
field: software-engineering
product: nim
tags: [link-time-and-size-optimization, build-optimization-flags, lto, pgo, strip, binary-size, opt-size, upx, static-linking, embedded, flto, nim]
level: advanced
status: docs-checked
description: "Shrink and tune Nim binaries with the documented flags -d:lto, -d:strip, --opt:size, --mm:arc, -d:useMalloc, --panics:on and --debuginfo."
sources:
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTO, stripping and small binaries

Goal: tune the output binary.

- The compiler guide's embedded-systems section suggests, when targeting a gcc compiler: `--opt:size -d:lto -d:strip`. `--opt:size` asks the C compiler to optimise for size, `-d:lto` enables link-time optimisation in the compiler and linker, `-d:strip` strips debug symbols from the executable. `-d:lto_incremental` additionally enables incremental linking (currently clang and vcc only).
- `--debuginfo:on|off` controls debug information; `--panics:on|off` turns panics into process terminations (default off).
- For small targets the guide uses `nim c --os:any --mm:arc -d:useMalloc x.nim`: `--mm:arc` is reference counting, `--os:any` avoids OS-specific primitives, and `-d:useMalloc` makes Nim use the C `malloc`/`free`/`realloc` (only with `--mm:none`, `arc` or `orc`).
- Extra options go to the C compiler/linker via `--passC:` / `--passL:`; the guide cites `--passC:-ffast-math` as a more aggressive release option (with a pointer to an open issue).
- Optimisation order from the guide: switch off the embedded debugger, turn on the optimizer and turn off runtime checks (`-d:release` / `-d:danger`), profile, find a better algorithm, then low-level work.

Gotchas:
- `-d:lto`, `-d:strip` and `-d:lto_incremental` are command-line defines; they cannot be set from NimScript config files.
- `-d:danger` removes all runtime checks.

Verify: compare the binary size before and after applying the flags.

## Checked

2026-11-03. Confirmed in the Nim compiler guide (embedded systems, additional compilation switches, optimizing sections) and the NimScript page (lto/strip restriction). Removed: PGO recipe, `--passL:-s`, `strip`, UPX, `std/re`/`httpclient` size advice, float `echo` claim, `--passL:-static`, `-march=native`, `size`/`ls` commands (none in the pages).
Method: documentation only; no commands were run.
