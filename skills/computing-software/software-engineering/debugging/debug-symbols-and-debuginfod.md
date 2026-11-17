---
id: computing-software.software-engineering.debugging.debug-symbols-and-debuginfod
name: debug-symbols-and-debuginfod
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, debug-symbols, debuginfod, dwarf, split-dwarf, build-id, symbolication]
level: advanced
status: docs-checked
description: "Manage debug symbols: separate debug files by build-id or debuglink, split DWARF, debuginfod servers, and Windows symbol stores."
sources: ["https://sourceware.org/elfutils/Debuginfod.html", "https://sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html", "https://gcc.gnu.org/wiki/DebugFission", "https://learn.microsoft.com/en-us/windows/win32/debug/symbol-servers-and-symbol-stores"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug symbols, split DWARF and debuginfod

## Build with symbols, ship without
The GDB manual's recipe for separating debug info from an executable `foo`:
```
objcopy --only-keep-debug foo foo.debug
strip -g foo
objcopy --add-gnu-debuglink=foo.debug foo      # optional: leave a debug link in foo
```
GDB supports two ways to find the separate file:
- **Debug link**: a `.gnu_debuglink` section holds the file name and a CRC-32 that GDB uses to check the
  executable and debug file came from the same build. GDB looks beside the executable, then in its `.debug`
  subdirectory, then under the global debug directories.
- **Build ID**: a unique bit string (section often `.note.gnu.build-id`) present in the original binary, its
  stripped variant and the debug file. Embed it with `ld --build-id` or `gcc -Wl,--build-id`. GDB looks for
  `.build-id/nn/nnnn....debug` under each global debug directory (`nn` is the first two hex characters).
  Default algorithm SHA1 gives 40 hex characters.

Example from the manual: for `/usr/bin/ls` with build ID `abcdef1234` and `/usr/lib/debug` as a global debug
directory, GDB tries `/usr/lib/debug/.build-id/ab/cdef1234.debug` first, then the debug-link locations. Set
the directories with `set debug-file-directory`. If the file is still missing and debuginfod is enabled, GDB
tries to download it. Store each build's debug file keyed by build ID.

## Split DWARF (DebugFission)
Compile with `-gsplit-dwarf` (with `-c`; not in the same step as linking) to write most debug info to a
parallel `.dwo` file, shrinking the object files the linker processes. The motivation on the project page is
slow link times, link-time out-of-memory conditions, slow GDB startup and storage cost for large
applications. The `.dwo` files must stay available as long as the binary needs debugging; the page also
describes packaging them and using the gold linker's `--gdb-index` option.

## debuginfod
elfutils 0.178+ includes a client/server that distributes ELF/DWARF/source over HTTP by build ID. Add server
URLs (space-separated) to `$DEBUGINFOD_URLS`. Public servers exist for several distributions (the page lists
`https://debuginfod.elfutils.org/` as a federating server, plus distro servers such as Debian, Fedora, Arch,
openSUSE, CentOS and Ubuntu). To run your own:
```
export DEBUGINFOD_URLS=https://foo.bar/    # optional federated upstream servers
debuginfod [-F $files] [-R $rpms] [-U $debs] &
export DEBUGINFOD_URLS=http://localhost:8002/    # then point clients at it
```
Client support: gdb from 10.1, binutils from 2.34, valgrind from 3.17.0, perf from Linux 5.10, bpftrace from
0.21.0, WinDbg from 1.2104.13002.0, VS Code via gdb (the page's table, dated 2025-01; distros may lag).
Smoke tests from the page: `eu-stack -v -p $$` for a live stack with source lines, and
`debuginfod-find debuginfo <BUILD_ID>`-style fetches (`debuginfod-find source <BUILD_ID> <path>`).

## Windows
Debugging Tools for Windows includes the SymSrv symbol server and the SymStore tool. A symbol store is a
collection of symbol files with an index, keyed by parameters such as time stamp and image size, so the
debugger fetches the right symbols when a module loads. It is activated by a string in the symbol path. See
the Microsoft pages "Using SymSrv" and "Using SymStore" for exact syntax.

## Gotchas
Use the exact build's symbols: the build ID or debug-link CRC exists so a mismatched file is detected.

## Checked
2026-11-09. Confirmed against the GDB manual "Debugging Information in Separate Files" (objcopy/strip
commands, debug link vs build ID lookup, example paths, SHA1/40 hex, `set debug-file-directory`), the
elfutils debuginfod page (versions, `DEBUGINFOD_URLS`, `debuginfod -F/-R/-U`, public servers, client table)
and the GCC DebugFission page (`-gsplit-dwarf`, `.dwo`, link-time motivation). The Microsoft symbol-store
page was read (SymSrv, SymStore, index keys). Removed: gcc `-O2 -g` claims, readelf/addr2line/dump_syms/
dwarfdump/symstore command lines, Rust and Go flags, PIE load-base advice, Sentry/Crashpad/Breakpad and
macOS dSYM notes, and `-Og` advice, none stated in the cited pages.
Method: documentation only; no commands were run.
