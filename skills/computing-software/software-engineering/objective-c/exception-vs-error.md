---
id: computing-software.software-engineering.objective-c.exception-vs-error
name: exception-vs-error
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-exceptions, exception-vs-error]
level: advanced
status: docs-checked
description: "Use NSException only for programmer errors and NSError for all other failures, and convert exceptions to errors where a method has an error parameter."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/ErrorHandling/ErrorHandling.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Exceptions/Tasks/HandlingExceptions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions versus errors
**Goal:** pick the right failure channel.

- In Objective-C exceptions are used solely for programmer errors, such as out-of-bounds array access or invalid method arguments. These are problems to find and fix during testing before shipping.
- All other errors are `NSError` instances: no network connectivity, a remote service that is inaccessible or cannot serve the request, data that does not match what you expected, running out of disk space, invalid user input.
- Methods report recoverable failures with an `NSError **` parameter and a `BOOL` or object return value; delegate methods deliver errors to the delegate.
- Exceptions are objects (`NSException`). Handle them with `@try` / `@catch` / `@finally`; most exceptions go uncaught until they reach the top-level handler installed by `NSApplication` or `UIApplication`.
- One way to handle an exception is to promote it to an `NSError`: catch it and return error information through a method's error parameter, or show it to the user.
- Prefer throwing `NSException` objects only: Cocoa handlers may not handle other object types, with undefined results.

## Gotchas
- Do not treat exceptions as the general error channel the way other languages do; use `NSError` for expected failures.

## Self-check
List each public method and mark which failures return `NSError` and which are programmer errors; check the tests cover both.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Dealing with Errors" and the Exception Programming Topics, "Handling Exceptions" (programmer errors vs NSError, top-level handler, promoting exceptions to errors, throw NSException). Removed: `NSAssert` / `NSParameterAssert` and `NS_BLOCK_ASSERTIONS`, `NSSetUncaughtExceptionHandler`, AppKit event-handler catching, cost-of-throwing and cross-thread claims (not on those pages).
Method: documentation only; no commands were run.
