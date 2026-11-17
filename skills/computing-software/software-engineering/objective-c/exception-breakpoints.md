---
id: computing-software.software-engineering.objective-c.exception-breakpoints
name: exception-breakpoints
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-debugging, exception-breakpoints]
level: practitioner
status: draft
description: "Stop on thrown Objective-C exceptions and unrecognized selectors with exception breakpoints and symbolic breakpoints."
sources:
  - https://lldb.llvm.org/
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exception breakpoints
**Goal:** stop at the throw site, not in the crash handler.

```
(lldb) breakpoint set -E objc                    # all Objective-C exceptions
(lldb) breakpoint set -E objc -O NSRangeException # a specific exception class name
(lldb) breakpoint set -n objc_exception_throw
(lldb) breakpoint set -n '-[NSObject(NSObject) doesNotRecognizeSelector:]'
(lldb) breakpoint set -n malloc_error_break
```
- In Xcode: Breakpoint navigator > + > Exception Breakpoint, choose Objective-C.
- When a crash prints `*** Terminating app due to uncaught exception`, the throw stack is gone at `abort`; an exception breakpoint preserves it.
- `-[NSException callStackSymbols]` and `callStackReturnAddresses` give the throw stack for logging.
- `malloc_error_break`/`MallocStackLogging` help find double frees and heap corruption.
- Use symbolic breakpoints on `UIViewAlertForUnsatisfiableConstraints` to debug Auto Layout conflicts.
- Breakpoint actions can log a message and auto-continue to avoid editing code.

## Gotchas
- Some frameworks throw and catch internally; filter with conditions or you stop constantly.
- Symbolic names of private methods can change between OS releases.

## Self-check
Trigger `[@[] objectAtIndex:1]` and confirm the debugger stops at the throw.
