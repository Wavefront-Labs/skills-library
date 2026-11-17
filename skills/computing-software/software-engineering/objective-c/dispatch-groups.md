---
id: computing-software.software-engineering.objective-c.dispatch-groups
name: dispatch-groups
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-gcd, dispatch-groups]
level: practitioner
status: draft
description: "Coordinate multiple async tasks with dispatch_group_enter/leave/notify and throttle with dispatch_semaphore."
sources:
  - https://developer.apple.com/documentation/dispatch
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dispatch groups and semaphores
**Goal:** wait for several async operations.

```objc
dispatch_group_t g = dispatch_group_create();
for (NSURL *u in urls) {
    dispatch_group_enter(g);
    [self fetch:u completion:^(NSData *d) { /* store */ dispatch_group_leave(g); }];
}
dispatch_group_notify(g, dispatch_get_main_queue(), ^{ NSLog(@"all done"); });

dispatch_semaphore_t sem = dispatch_semaphore_create(3);     // at most 3 concurrent
dispatch_semaphore_wait(sem, DISPATCH_TIME_FOREVER);
/* work */
dispatch_semaphore_signal(sem);
```
- Every `enter` must be balanced by exactly one `leave`; an extra `leave` crashes, a missing one never fires notify.
- `dispatch_group_async(g, queue, block)` handles enter/leave automatically for synchronous blocks.
- Prefer `dispatch_group_notify` to `dispatch_group_wait`, which blocks a thread and must not be used on the main thread.
- Semaphore initial value 0 is used for signaling; do not release a semaphore whose value is lower than its initial value (it crashes).
- `dispatch_apply(n, queue, ^(size_t i){})` runs iterations concurrently and waits.

## Gotchas
- Blocking the main thread on a semaphore signaled from a main-queue block deadlocks.
- Error handling needs explicit shared state with synchronization.

## Self-check
Run three async fetches and assert the notify block runs exactly once after all complete.
