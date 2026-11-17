---
id: computing-software.software-engineering.objective-c.lldb-commands
name: lldb-commands
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-debugging, lldb-commands]
level: practitioner
status: draft
description: "Use po, p, expr, bt, frame, breakpoint and watchpoint commands in LLDB to inspect Objective-C objects and call methods."
sources:
  - https://lldb.llvm.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LLDB for Objective-C
**Goal:** inspect and change running state.

```
(lldb) po self                        # description of an object
(lldb) po [self.view subviews]
(lldb) p count                        # typed value
(lldb) expr -l objc -O -- [NSBundle mainBundle]
(lldb) expr self.title = @"x"         # modify state
(lldb) bt                             # backtrace; also: thread backtrace all
(lldb) frame variable                 # locals of the selected frame; frame select 2
(lldb) breakpoint set -n viewDidLoad
(lldb) breakpoint set -S setName:     # by selector
(lldb) breakpoint set --file Foo.m --line 42
(lldb) watchpoint set variable _count
(lldb) image lookup -rn 'ABCCart'     # find symbols
(lldb) continue / next / step / finish
```
- `po` prints `debugDescription`; override it for useful output.
- Casting is needed when types are unknown: `po (id)0x12345678`, `po [(NSObject *)obj class]`.
- Symbolic breakpoints and conditions: `breakpoint modify -c 'idx == 3' 1`; actions with `breakpoint command add`.
- `.lldbinit` in `~` or the project holds aliases.
- For view hierarchies, `po [view recursiveDescription]` is widely used but not documented public API.

## Gotchas
- Optimized builds hide variables ("optimized out"); debug with `-O0`.
- Calling methods with side effects from the debugger changes program state.

## Self-check
Set a breakpoint with a condition and confirm it stops only at the matching iteration.
