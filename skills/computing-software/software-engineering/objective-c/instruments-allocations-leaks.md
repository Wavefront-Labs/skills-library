---
id: computing-software.software-engineering.objective-c.instruments-allocations-leaks
name: instruments-allocations-leaks
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-profiling, instruments-allocations-leaks]
level: practitioner
status: draft
description: "Track memory growth with Instruments Allocations generations, Leaks, and the Xcode Memory Graph Debugger to find retain cycles."
sources:
  - https://developer.apple.com/documentation/xcode
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Allocations and leaks
**Goal:** diagnose growth and leaks.

- Instruments > Allocations: use "Mark Generation" before and after repeating an action (open and close a screen) three times; objects persisting in later generations indicate leaks or cycles.
- Instruments > Leaks finds unreachable allocations; it does not find reachable growth ("abandoned" memory such as unbounded caches).
- Xcode Memory Graph Debugger (Debug bar button): lists live instances; purple exclamation marks flag leaks; select an object to view the retaining paths. Enable "Malloc Stack Logging" in the scheme to see allocation backtraces.
- Environment: `MallocStackLogging=1` and the `leaks` CLI: `leaks --atExit -- ./app` or `leaks <pid>`.
- Find retain cycles by following strong edges from a leaked object back to itself: usual suspects are blocks capturing self, NSTimer targets, delegates declared strong.
- Autoreleased temporaries create a sawtooth; add `@autoreleasepool` inside loops.

## Gotchas
- Cached images and `NSCache` look like growth until memory warnings purge them.
- Leaks reports for system frameworks are often false alarms.

## Self-check
Open and close a view controller five times and confirm its instance count returns to zero.
