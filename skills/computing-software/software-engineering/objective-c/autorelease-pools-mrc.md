---
id: computing-software.software-engineering.objective-c.autorelease-pools-mrc
name: autorelease-pools-mrc
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-mrc, autorelease-pools-mrc]
level: advanced
status: docs-checked
description: "Use @autoreleasepool blocks to cap memory in loops and on secondary threads, and extend an object's lifetime past a pool with retain then autorelease."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmAutoreleasePools.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/mmRules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autorelease pools under MRC
**Goal:** return objects without owning them and keep peak memory down.

```objc
for (NSURL *url in urls) {
    @autoreleasepool {
        NSError *error;
        NSString *fileContents = [NSString stringWithContentsOfURL:url
                                         encoding:NSUTF8StringEncoding error:&error];
        /* Process the string, creating and autoreleasing more objects. */
    }
}
```
- `autorelease` is a deferred `release`: at the end of the `@autoreleasepool` block, each object that received `autorelease` inside it is sent one `release` per `autorelease`.
- Pool blocks nest; the matching `release` goes out at the end of the block in which `autorelease` was sent.
- Cocoa expects code to run inside a pool; an `autorelease` outside one logs an error and the object leaks. AppKit and UIKit wrap each event-loop iteration in a pool.
- You create your own pool for a program with no UI framework (a command-line tool), for a loop that creates many temporaries, and as soon as a secondary thread starts executing. Each thread keeps its own stack of pools.
- After the block, treat anything autoreleased inside as disposed of: do not message it or return it. To keep an object, send `retain` inside the block and `autorelease` after it.

```objc
- (id)findMatchingObject:(id)anObject {
    id match;
    while (match == nil) {
        @autoreleasepool {
            match = [self expensiveSearchForObject:anObject];
            if (match != nil) { [match retain]; }
        }
    }
    return [match autorelease];
}
```

## Gotchas
- A detached thread that makes no Cocoa calls does not need a pool.
- Using the POSIX thread APIs instead of `NSThread` requires Cocoa to be in multithreading mode before you use it.

## Self-check
Log `dealloc` for a temporary created inside a looped pool and confirm it fires on each iteration.

## Checked
2026-11-03. Confirmed against Apple's Advanced Memory Management Programming Guide, "Using Autorelease Pool Blocks" (pool semantics, nesting, when to create one, threads, retain-then-autorelease) and "Memory Management Policy". Removed: `NSAutoreleasePool` / `drain` claims, per-run-loop-iteration and "equivalent drain/release" remarks, and out-of-order pool release error (not on those pages).
Method: documentation only; no commands were run.
