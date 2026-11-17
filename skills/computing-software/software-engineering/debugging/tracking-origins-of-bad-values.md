---
id: computing-software.software-engineering.debugging.tracking-origins-of-bad-values
name: tracking-origins-of-bad-values
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, backward-slicing, infection-chain, root-cause, data-flow, watchpoints]
level: advanced
status: draft
description: "Trace a wrong value back to where it was first infected using backward slicing, watchpoints, reverse debugging and assertions, following Zeller's infection-chain model."
sources: ["https://www.whyprogramsfail.com/", "https://www.debuggingbook.org/html/Slicer.html", "https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Watchpoints.html", "https://rr-project.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracking origins of bad values

Zeller (Why Programs Fail): a **defect** in code causes an **infection** (wrong program state), which
propagates through an **infection chain** until it becomes a visible **failure**. Debugging is
walking that chain backwards to the first infected state.

## Backward slicing (by hand or tool)
Start from the bad value at the failure point and ask "which statements could have influenced
this?":
- **Data dependencies**: the assignments that wrote the variables it was computed from.
- **Control dependencies**: the conditions that decided whether those assignments ran.
The slice is usually a small fraction of the program; only it needs inspecting. The debuggingbook
`Slicer` (Python) computes dynamic slices automatically for small programs; IDEs offer "Analyze
data flow to here" (IntelliJ) and "Find all references/writes" (VS, Rider).

## Find the infection point
For each value in the slice, check whether it is already wrong (compare with what it should be):
- **Watchpoints**: break when a variable or memory changes. gdb `watch obj->balance`, `rwatch`,
  `awatch`; lldb `watchpoint set variable x`; IntelliJ field watchpoints; Visual Studio data
  breakpoints; Python has none built in (use a property setter or `sys.settrace` temporarily).
- **Reverse/time-travel debugging**: `rr record ./app` then `rr replay`, set a watchpoint and
  `reverse-continue` to land on the last write. WinDbg TTD, UndoDB, Chrome DevTools for some JS
  cases. Best tool for "who set this to null?".
- **Assertions** (invariant checks) placed earlier in the chain narrow the region by bisection.
- Logging with object ids/values at each hop when the chain crosses processes or services.

## Repeat until
You find a statement whose inputs are all correct but whose output is wrong: that's the defect.
If the inputs come from outside (config, data, another service), the chain continues there.

## Pitfalls
- Fixing where the failure appears (adding a null check at the crash) instead of where the
  infection starts: symptoms move elsewhere.
- Multiple infection origins: verify the fix by re-running with the original failing input.
