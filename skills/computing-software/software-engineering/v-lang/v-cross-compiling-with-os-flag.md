---
id: computing-software.software-engineering.v-lang.v-cross-compiling-with-os-flag
name: v-cross-compiling-with-os-flag
category: computing-software
field: software-engineering
product: v-lang
tags: [v-cross-compiling-with-os-flag, v-cross-compilation-and-backends, cross-compile, os-flag, windows, linux, freebsd, mingw, cc, v-lang]
level: advanced
status: docs-checked
description: "Cross-compile V with -os for Windows, Linux and FreeBSD, install MinGW-w64 for Windows targets, pick a custom compiler with -cc, and use portable -os cross C output."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-compiling with -os

Goal: produce binaries for other platforms.

- The docs state cross compilation is supported for Windows, Linux and FreeBSD: `v -os windows .`, `v -os linux .`, `v -os freebsd .`. Cross compiling for macOS is documented as temporarily not possible.
- Windows target from Linux or macOS needs the GNU C compiler for MinGW-w64 (targeting Win64) installed first: `sudo apt install gcc-mingw-w64-x86-64` (Ubuntu/Debian), `sudo pacman -S mingw-w64-gcc` (Arch), `brew install mingw-w64` (Homebrew). Without `-arch` and `-cc`, `-os windows` builds an amd64 executable with `x86_64-w64-mingw32-gcc`, also on an arm64 machine.
- On macOS, `-os linux` with the default C compiler or Clang uses a bundled amd64 Linux sysroot, and V enables `$if cross_compile ?` for it.
- With no C dependencies this works, even for GUI apps using `ui` or `gg`.
- Custom cross compiler: pass `-cc <compiler>` for one build (docs example `v -os linux -cc cosmocc .`) or set `VCROSS_COMPILER_NAME` in the environment. The docs say you then need Clang, the LLD linker and a zip of libraries and include files for Windows and Linux, and V provides a link.
- `-os cross` is not a platform: it asks for portable C, only meaningful with `-o file.c` (for example `v -os cross -o /tmp/v.c cmd/v`). `-cross` is the modifier form that combines with an explicit target.
- For iOS the docs show `v -os ios hello.v` (and `-simulator`).

Gotchas:
- Platform files such as `_windows.c.v` are chosen when compiling on Windows or with `-os windows`, and `$if windows` follows the target.
- A development build using `$embed_file` stores only the file path and panics when run where the file does not exist, for example after cross compiling; use `-prod` for anything you distribute.

## Checked

Confirmed against the "Cross compilation", "Portable C output (`-os cross`)", "Embedding" and "Conditional compilation" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: musl/zig recipes, the `-os macos` osxcross route, `-os android`/`browser` target list, `-arch` value list, and the `file app.exe` check (none stated in the docs read), and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
