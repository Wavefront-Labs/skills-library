---
id: computing-software.software-engineering.objective-c.singleton-pattern
name: singleton-pattern
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-cocoa-patterns, singleton-pattern]
level: practitioner
status: draft
description: "Implement a thread-safe singleton with dispatch_once, restrict init, and know when to prefer dependency injection."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html
  - https://developer.apple.com/documentation/dispatch
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Singleton
**Goal:** a shared instance without race conditions.

```objc
@interface ABCSettings : NSObject
@property (class, nonatomic, readonly) ABCSettings *shared;
- (instancetype)init NS_UNAVAILABLE;
+ (instancetype)new NS_UNAVAILABLE;
@end
@implementation ABCSettings
+ (ABCSettings *)shared {
    static ABCSettings *s; static dispatch_once_t once;
    dispatch_once(&once, ^{ s = [[self alloc] initPrivate]; });
    return s;
}
- (instancetype)initPrivate { return [super init]; }
@end
```
- Use `dispatch_once`; avoid double-checked locking and `@synchronized` for init.
- Mark `init`/`new` unavailable to prevent accidental extra instances (use a private designated init).
- Cocoa examples: `NSFileManager defaultManager`, `NSNotificationCenter defaultCenter`, `UIApplication sharedApplication`.
- Downsides: hidden dependencies and test difficulty; prefer passing collaborators through initializers and keep singletons for truly process-wide resources.
- For tests, expose a protocol and inject a fake, or reset state in `setUp`.

## Gotchas
- Singletons created in `+initialize` or `+load` may run before dependencies exist.
- Mutable singleton state needs its own synchronization.

## Self-check
Call `shared` from 50 concurrent blocks and assert all return the same pointer.
