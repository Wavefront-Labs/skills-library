---
id: computing-software.software-engineering.objective-c.synchronized-lock
name: synchronized-lock
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-thread-safety, synchronized-lock]
level: practitioner
status: draft
description: "Protect shared state with @synchronized, NSLock, NSRecursiveLock and os_unfair_lock, and avoid lock ordering deadlocks."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Locks and synchronization
**Goal:** pick the right mutex.

```objc
@synchronized (self.items) { [self.items addObject:x]; }      // recursive, exception-safe, slowest

NSLock *lock = [NSLock new];
[lock lock]; /* critical section */ [lock unlock];

#import <os/lock.h>
os_unfair_lock l = OS_UNFAIR_LOCK_INIT;
os_unfair_lock_lock(&l); /* tiny critical section */ os_unfair_lock_unlock(&l);
```
- `@synchronized(obj)` locks on the object's identity; use a private lock object, not `self` (external code could lock it too).
- `NSRecursiveLock` for re-entrancy; `NSCondition` for wait/signal; `NSConditionLock` for state-driven handoff.
- `os_unfair_lock` replaced `OSSpinLock` (priority inversion); it is not recursive and must live at a stable address (don't copy it).
- Lock ordering: always take multiple locks in a fixed global order.
- Serial dispatch queues are often simpler and avoid lock bugs.
- Do not call unknown code (delegates, blocks) while holding a lock.

## Gotchas
- Unlock on the same thread that locked (for `NSLock`).
- Locking in `dealloc` of an object being waited on is a bug.

## Self-check
Run a stress test with Thread Sanitizer (`-fsanitize=thread`) and confirm no data race reports.
