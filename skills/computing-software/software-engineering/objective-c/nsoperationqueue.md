---
id: computing-software.software-engineering.objective-c.nsoperationqueue
name: nsoperationqueue
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-operations, nsoperationqueue]
level: practitioner
status: draft
description: "Run work on NSOperationQueue with maxConcurrentOperationCount, QoS, block operations and cancellation."
sources:
  - https://developer.apple.com/documentation/foundation
  - https://developer.apple.com/documentation/dispatch
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSOperationQueue
**Goal:** object-oriented, cancelable task queues.

```objc
NSOperationQueue *q = [NSOperationQueue new];
q.name = @"com.example.parse";
q.maxConcurrentOperationCount = 2;
q.qualityOfService = NSQualityOfServiceUtility;
[q addOperationWithBlock:^{ /* work */ }];
NSBlockOperation *op = [NSBlockOperation blockOperationWithBlock:^{ ... }];
[q addOperation:op];
[q cancelAllOperations];
[q waitUntilAllOperationsAreFinished];     // not on the main thread
NSOperationQueue.mainQueue addOperationWithBlock:...   // UI updates
```
- Operations are one-shot; cancel is cooperative: the work must check `isCancelled`.
- `maxConcurrentOperationCount = 1` gives a serial queue (not strictly the same thread each time).
- Queue is built on GCD but adds dependencies, KVO-observable state, priorities and cancel.
- `addOperations:waitUntilFinished:YES` blocks the caller.
- Set `underlyingQueue` to a dispatch queue only for serial scenarios (must be a serial queue, per docs).

## Gotchas
- Cancelled operations still go through to finished state; dependencies on them still unblock.
- Blocking on `waitUntilAllOperationsAreFinished` on the main thread freezes UI.

## Self-check
Cancel a long block operation and confirm it returns early by checking `isCancelled` in its loop.
