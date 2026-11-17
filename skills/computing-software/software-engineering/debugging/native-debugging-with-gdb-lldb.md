---
id: computing-software.software-engineering.debugging.native-debugging-with-gdb-lldb
name: native-debugging-with-gdb-lldb
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, gdb, lldb, breakpoints, watchpoints, core-dump, backtrace, segfault, coredump, native-debugging, c, cpp, rust, asan, ptrace]
level: advanced
status: docs-checked
description: "Debug compiled programs with gdb/lldb: breakpoints, watchpoints, conditional breaks, core dumps, and reading a segfault backtrace."
sources: ["https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Breaks.html", "https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Watchpoints.html", "https://sourceware.org/gdb/current/onlinedocs/gdb.html/Core-File-Generation.html", "https://sourceware.org/gdb/current/onlinedocs/gdb.html/Threads.html", "https://sourceware.org/gdb/current/onlinedocs/gdb.html/Attach.html", "https://lldb.llvm.org/use/map.html", "https://clang.llvm.org/docs/AddressSanitizer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native debugging with gdb/lldb — from a segfault to a root cause

**Goal:** go from "it crashed" to the exact line and bad value, using a debugger
instead of println-driven guessing, for C/C++/Rust/Go-cgo binaries.

## 1. Get symbols first
Build with debug info (`-g`) so frames show file:line instead of `??`.

## 2. Breakpoints beyond "stop at a line"
```
(gdb) break file.c:42
(gdb) break my_function
(gdb) break file.c:42 if x > 100          # conditional: essential in a hot loop
(gdb) watch global_counter                 # stop when the value changes
(gdb) rwatch some_var                      # stop when the value is read
(gdb) tbreak file.c:42                     # temporary breakpoint, deleted once hit
```
lldb spells these `breakpoint set --file foo.c --line 12` and `breakpoint set
--name foo`; for watchpoints see `watchpoint set` in the lldb command map.

A watchpoint is the right tool for "this value changes somewhere I can't find by
reading code": it stops where the value is written, which grep for assignments
cannot do when the write is through a pointer alias.

## 3. Core dumps: debug the crash after the fact
A core file records the memory image and process status of a process. Its main use is
post-mortem debugging of a program that crashed outside a debugger. Load the core
together with the executable and take a backtrace:
```
(gdb) bt                                  # backtrace at the moment of the crash
(gdb) frame 3                             # jump to a frame, inspect its locals
(gdb) print some_var
```
To snapshot a live process without killing it, gdb has `gcore [file]` (default
file name `core.<pid>`). Whether crashes write core files at all depends on your
system's core-dump settings; check them if no file appears.

## 4. Reading a backtrace that isn't your code
A crash deep inside a library often means memory was corrupted earlier; the
backtrace shows where it was detected, not where it happened. Rebuild with
AddressSanitizer (`-fsanitize=address`, together with `-g`): it reports errors such
as heap-use-after-free with the stack of the faulting access, which is quicker than
stepping by hand.

## 5. Attaching to a running or hung process
```
gdb -p <pid>                              # attach live
(gdb) bt                                  # see what it's doing right now
```
For a hung process, take a backtrace of every thread: `thread apply all bt` in gdb,
`thread backtrace all` in lldb. Use `info threads` to list threads. This usually
shows a lock wait or a loop directly, faster than adding logging and redeploying.

## 6. Scripting repetitive inspection
```
(gdb) commands
> print x
> continue
> end
```
`commands` attaches a command list to a breakpoint (see the gdb Break Commands page).

## Gotchas
- Multi-threaded crashes: check `info threads` and inspect the other threads before
  deciding which one caused the crash.
- A program that crashes produces a core file automatically unless the user has
  disabled that (gdb manual); if none appears, check your system's core-dump setting.

## Verify
- [ ] The binary has `-g` symbols and backtrace shows real file:line, not `??`.
- [ ] `bt` was captured either live (attach) or from a core dump, not reconstructed
      from memory of what probably happened.
- [ ] If the crash is inside a system library, AddressSanitizer was run to find the
      real corruption site before concluding the library is at fault.
- [ ] A watchpoint (not a grep for assignments) was used for "value changes
      unexpectedly through a pointer/alias."

## Checked
2026-11-01. Confirmed against the gdb manual (Setting Breakpoints incl. `break ... if cond`
and `tbreak`; Setting Watchpoints incl. `watch`, `rwatch`; How to Produce a Core File incl.
`gcore`, `core.pid` default, post-mortem purpose; Threads incl. `info threads`,
`thread apply all`; Attach), the lldb GDB-to-LLDB command map (`thread backtrace all`,
`watchpoint set`) and the lldb tutorial (`breakpoint set`), and the Clang AddressSanitizer
page (`-fsanitize=address`, heap-use-after-free reports). Removed unconfirmed claims:
optimisation flag names, `file` stripped check, systemd-coredump/coredumpctl, `ulimit -c`
and `LimitCORE`, `lldb -c`, Valgrind, `.gdbinit` and STL pretty-printers, rust-gdb/rust-lldb,
macOS SIP, and malloc error strings.
Method: documentation only; no commands were run.

Related: computing-software.software-engineering.debugging.systematic-debugging,
computing-software.software-engineering.cpp.raii-and-smart-pointers
