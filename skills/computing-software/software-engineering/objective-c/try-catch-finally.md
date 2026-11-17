---
id: computing-software.software-engineering.objective-c.try-catch-finally
name: try-catch-finally
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-exceptions, try-catch-finally]
level: practitioner
status: docs-checked
description: "Use @try, @catch, @finally and @throw to handle exceptions, rethrow with a bare @throw, and put cleanup in @finally."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Exceptions/Tasks/HandlingExceptions.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/ErrorHandling/ErrorHandling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @try / @catch / @finally
**Goal:** handle exceptions only where handling them makes sense.

```objc
@try {
    [treeController setValue:[predicateEditorView predicate] forKeyPath:@"selection.predicate"];
}
@catch (NSException *e) {
    [treeController setValue:nil forKeyPath:@"selection.predicate"];
    // @throw;   // a bare @throw rethrows the caught exception
}
@finally {
    [NSApp endSheet:sheet];
}
```
- `@try` defines the exception handling domain, `@catch()` the handler for the object thrown (usually `NSException`), `@finally` code that runs whether or not an exception was thrown, and `@throw` throws an exception, almost identically to `NSException`'s `raise`.
- Throw `NSException` objects only: Cocoa handlers might only catch `NSException` for some conditions, so other thrown types can run into undefined behaviour.
- Inside a `@catch` block a bare `@throw;` rethrows the exception so it is handled at a higher level.
- Put cleanup such as a `release` in `@finally` so it still runs when a called method throws; otherwise it can leak.
- If you release a local autorelease pool in `@finally`, the exception object it holds can be released too early. Either leave deeper pools to take care of it or retain the exception, rethrow, and release the pool and autorelease the exception in `@finally`.
- Cocoa uses exceptions for programmer errors (out-of-bounds access, invalid arguments), which you should fix during testing; use `NSError` for other failures.

## Gotchas
- Throwing non-`NSException` objects may bypass or confuse Cocoa's own handlers.

## Self-check
Throw from inside `@try` and confirm the `@finally` block ran.

## Checked
2026-11-03. Confirmed against Apple's Exception Programming Topics, "Handling Exceptions" (directives, NSException recommendation, rethrow, release in @finally, autorelease pool caveat) and Programming with Objective-C, "Dealing with Errors". Removed: `-fobjc-arc-exceptions` and ARC unwinding claims, zero-cost exceptions, `NSAssert` exception names, the `callStackSymbols` logging, C++ and Swift interoperability remarks and the `NSRangeException` self-check (not on those pages).
Method: documentation only; no commands were run.
