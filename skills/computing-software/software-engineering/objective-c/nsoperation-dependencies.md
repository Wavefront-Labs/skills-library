---
id: computing-software.software-engineering.objective-c.nsoperation-dependencies
name: nsoperation-dependencies
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-operations, nsoperation-dependencies]
level: advanced
status: draft
description: "Subclass NSOperation (sync and async variants), add dependencies, and manage isExecuting/isFinished KVO correctly."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSOperation dependencies and subclasses
**Goal:** express ordering between tasks and write async operations.

```objc
NSOperation *download = ..., *parse = ..., *save = ...;
[parse addDependency:download];
[save addDependency:parse];
[queue addOperations:@[download, parse, save] waitUntilFinished:NO];
```
- A dependent operation starts only after all its dependencies finish (including cancelled ones); never create cycles (deadlock).
- Synchronous subclass: override `-main` and check `self.isCancelled` periodically. A `main` wrapped in `@autoreleasepool` is recommended.
- Asynchronous subclass: override `start`, `isAsynchronous` (YES), `isExecuting`, `isFinished`, and post KVO via `willChangeValueForKey:`/`didChangeValueForKey:` for `isExecuting`/`isFinished` when state changes.
- `completionBlock` runs after finish on an unspecified thread.
- Pass results via properties of the dependency (read from the dependent's `main`).
- Priorities (`queuePriority`) only order ready operations; dependencies take precedence.

## Gotchas
- Forgetting to set `isFinished` in an async operation leaves the queue stuck.
- Add dependencies before adding to the queue.

## Self-check
Create a three-step chain and log order; reverse dependencies and confirm the order flips.
