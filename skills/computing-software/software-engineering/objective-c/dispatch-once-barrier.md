---
id: computing-software.software-engineering.objective-c.dispatch-once-barrier
name: dispatch-once-barrier
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-gcd, dispatch-once-barrier]
level: advanced
status: draft
description: "Initialize shared state once with dispatch_once, and protect data with reader-writer queues using dispatch_barrier_async."
sources:
  - https://developer.apple.com/documentation/dispatch
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# dispatch_once and barriers
**Goal:** safe lazy initialization and a reader-writer lock.

```objc
+ (instancetype)shared {
    static ABCService *inst; static dispatch_once_t once;
    dispatch_once(&once, ^{ inst = [[self alloc] init]; });
    return inst;
}

@interface ABCCache : NSObject { dispatch_queue_t _q; NSMutableDictionary *_d; }
@end
- (instancetype)init { if ((self = [super init])) { _q = dispatch_queue_create("cache", DISPATCH_QUEUE_CONCURRENT); _d = [NSMutableDictionary new]; } return self; }
- (id)objectForKey:(id)k { __block id r; dispatch_sync(_q, ^{ r = self->_d[k]; }); return r; }
- (void)setObject:(id)o forKey:(id<NSCopying>)k { dispatch_barrier_async(_q, ^{ self->_d[k] = o; }); }
```
- `dispatch_once_t` must be static or global, zero-initialized; never an ivar.
- Recursive `dispatch_once` on the same token deadlocks.
- A barrier block on a custom concurrent queue waits for earlier blocks, runs alone, then lets later blocks proceed. It has no effect on global queues (acts like normal async).
- Reads use `dispatch_sync` (they return a value); writes use `dispatch_barrier_async`.
- Newer code in Swift-bridged projects may use `os_unfair_lock` or `@synchronized` where simpler.

## Gotchas
- Calling the reader `dispatch_sync` from within a write barrier on the same queue deadlocks.
- Barriers on a serial queue are redundant.

## Self-check
Hammer the cache from 100 concurrent async blocks under Thread Sanitizer and confirm no race reports.
