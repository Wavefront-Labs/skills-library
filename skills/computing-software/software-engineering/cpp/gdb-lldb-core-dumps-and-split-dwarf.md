---
id: computing-software.software-engineering.cpp.gdb-lldb-core-dumps-and-split-dwarf
name: gdb-lldb-core-dumps-and-split-dwarf
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-debugging, cpp-db-gdb, cpp-db-lldb, cpp-db-dwarf, gdb, lldb, core-dump, split-dwarf, debug-symbols, gdb-core-dumps, lldb-debugging, split-dwarf-debug-info]
level: practitioner
status: draft
description: "Debug C++ crashes with gdb or lldb: core dumps, backtraces, breakpoints and watchpoints, pretty printers, separate debug info, -gsplit-dwarf and symbol servers."
sources: ["https://sourceware.org/gdb/current/onlinedocs/gdb.html/", "https://lldb.llvm.org/use/tutorial.html", "https://gcc.gnu.org/wiki/DebugFission"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# gdb, lldb, core dumps and split DWARF

## Build for debugging
```
g++ -std=c++20 -g -Og -fno-omit-frame-pointer main.cpp -o app          # -g debug info; -Og or -O0 keeps variables visible
g++ -g -gsplit-dwarf -c big.cpp                                          # debug info in big.dwo: faster links, smaller objects
objcopy --only-keep-debug app app.debug && strip app && objcopy --add-gnu-debuglink=app.debug app   # ship stripped, keep symbols
```
Use `-gz` to compress sections and `-fdebug-prefix-map=/build/path=.` for reproducible paths. Keep `.debug` files per release (match the build-id: `readelf -n app`).

## gdb essentials
```
gdb ./app                       (gdb) run --arg1 | start | bt | bt full | frame 2 | info locals | p *ptr | p vec | ptype T
(gdb) break file.cpp:42 if i == 5     (gdb) tbreak main     (gdb) watch counter     (gdb) catch throw
(gdb) thread apply all bt       (gdb) info threads     (gdb) x/16xb ptr     (gdb) finish / next / step / until
gdb -batch -ex "bt full" ./app core
```
`catch throw` stops at C++ exceptions; libstdc++ pretty printers make `std::vector`/`map` readable (usually auto-loaded from the distro's package). `set print pretty on`, `set debuginfod enabled on` fetches symbols via debuginfod.

## lldb equivalents
```
lldb ./app -- args     (lldb) b file.cpp:42   (lldb) r   (lldb) bt   (lldb) frame variable   (lldb) p expr   (lldb) watchpoint set variable counter
(lldb) breakpoint set -E c++      # exception breakpoint        (lldb) thread backtrace all
```

## Core dumps
```
ulimit -c unlimited
cat /proc/sys/kernel/core_pattern        # on systemd: coredumpctl list ; coredumpctl gdb <pid>
gdb ./app core
```
On macOS cores go to `/cores` (enable with care); on Windows use WinDbg/procdump minidumps with PDBs (`/Zi`).

## Gotchas
- Optimised builds show `<optimized out>`; debug with `-Og` or reproduce at `-O0`.
- Binary and core must match exactly; use `coredumpctl` or keep the build-id-indexed symbol store.
- Split DWARF needs the `.dwo` files next to objects (or `.dwp` package via `dwp`); gdb needs `-gdwarf-5`-compatible versions and `gdb-index` to start quickly.
- ASLR affects addresses; gdb disables it by default (`set disable-randomization`).
- Stripped system libraries lack symbols; enable debuginfod.

## Verify
- [ ] Reproduce a deliberate `abort()`, load the core, `bt` shows file:line for each frame.
- [ ] `readelf --debug-dump=info app | head` (or `llvm-dwarfdump --verify`) confirms the debug info present or linked.
