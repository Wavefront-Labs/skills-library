---
id: computing-software.software-engineering.objective-c.dispatch-queues
name: dispatch-queues
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-gcd, dispatch-queues]
level: practitioner
status: draft
description: "Create serial and concurrent queues, use global and main queues with QoS, and choose async over sync to avoid deadlocks."
sources:
  - https://developer.apple.com/documentation/dispatch
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dispatch queues
**Goal:** run work asynchronously with the right queue type.

```objc
dispatch_queue_t q = dispatch_queue_create("com.example.work", DISPATCH_QUEUE_SERIAL);
dispatch_queue_t conc = dispatch_queue_create("com.example.conc", DISPATCH_QUEUE_CONCURRENT);
dispatch_queue_t bg = dispatch_get_global_queue(QOS_CLASS_UTILITY, 0);
dispatch_async(bg, ^{
    NSData *d = [self load];
    dispatch_async(dispatch_get_main_queue(), ^{ self.data = d; });
});
dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{ ... });
```
- A serial queue runs one block at a time in FIFO order; the main queue is serial and bound to the main thread.
- `dispatch_sync` onto the current serial queue (or main from main) deadlocks.
- QoS classes: user-interactive, user-initiated, default, utility, background; set on queue attributes via `dispatch_queue_attr_make_with_qos_class`.
- Under ARC, dispatch objects are managed as Objective-C objects when the deployment target supports it (OS_OBJECT_USE_OBJC); otherwise `dispatch_retain/release`.
- Use `dispatch_queue_set_specific` / `dispatch_get_specific` to detect "am I on my queue".
- Concurrent queues do not guarantee parallelism, just permit it.

## Gotchas
- Avoid `dispatch_sync` for thread safety inside a method invoked from the same queue.
- Never use `dispatch_get_current_queue` (deprecated).

## Self-check
Intentionally `dispatch_sync` to the main queue from main in a test harness and observe the hang; remove it.
