---
id: computing-software.software-engineering.objective-c.nsrunloop-nstimer
name: nsrunloop-nstimer
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-runloop, nsrunloop-nstimer]
level: practitioner
status: draft
description: "Understand run loop modes, schedule NSTimer in common modes, run a loop on a background thread and avoid timer retain cycles."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Run loops and timers
**Goal:** schedule periodic work correctly.

```objc
NSTimer *t = [NSTimer timerWithTimeInterval:1.0 repeats:YES block:^(NSTimer *timer) { [weakSelf tick]; }];
[[NSRunLoop currentRunLoop] addTimer:t forMode:NSRunLoopCommonModes];   // keeps firing while scrolling
[t invalidate];     // stop; timer is released by the run loop
```
- A run loop processes sources, timers and observers in a mode; `NSDefaultRunLoopMode` timers pause during scrolling (tracking mode) unless added to `NSRunLoopCommonModes`.
- `scheduledTimerWith...` adds to the current run loop in default mode; GCD worker threads have no running run loop, so timers there never fire.
- A background thread run loop must be started: add a source/timer and call `[[NSRunLoop currentRunLoop] run]`.
- The target-based `NSTimer` retains its target until invalidated; use the block form with a weak reference, or a weak proxy.
- Timers are not precise; for accuracy use `dispatch_source_t` timers (they carry a leeway argument).
- `performSelector:afterDelay:` depends on a run loop too.

## Gotchas
- `invalidate` must be called on the thread that created the timer.
- Timers keep the run loop alive; invalidate on view disappear.

## Self-check
Start a timer in default mode, scroll a UITableView and see it pause, then fix with common modes.
