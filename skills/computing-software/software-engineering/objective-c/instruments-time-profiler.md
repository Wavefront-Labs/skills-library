---
id: computing-software.software-engineering.objective-c.instruments-time-profiler
name: instruments-time-profiler
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-profiling, instruments-time-profiler]
level: practitioner
status: draft
description: "Find CPU hot spots with Instruments Time Profiler and automate captures with xcrun xctrace in Release builds."
sources:
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Time Profiler
**Goal:** locate where CPU time goes.

- Profile Release-like builds on a real device (Product > Profile, or `xcrun xctrace`).
```bash
xcrun xctrace list templates
xcrun xctrace record --template 'Time Profiler' --time-limit 30s --launch -- /path/to/App.app
xcrun xctrace export --input trace.trace --toc
```
- In the call tree: invert the call tree, hide system libraries, and use "Separate by Thread" to find heavy leaf functions.
- Common Objective-C costs: excessive `objc_msgSend` in tight loops (use C structs/arrays or `objc_direct`), autorelease traffic (add `@autoreleasepool`), `NSDateFormatter`/`NSRegularExpression` creation, KVO/KVC overhead, main-thread I/O.
- Add `os_signpost` intervals to label phases and view them in the Instruments signpost lane.
- Measure before/after with `XCTest measureBlock:` for regression tracking.

## Gotchas
- Debug builds distort hotspots; use `-O` builds with symbols.
- Simulators run on the host CPU and do not represent device performance.

## Self-check
Record twice with the same scenario to confirm the hotspot is stable.
