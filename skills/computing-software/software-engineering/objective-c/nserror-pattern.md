---
id: computing-software.software-engineering.objective-c.nserror-pattern
name: nserror-pattern
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-exceptions, nserror-pattern]
level: practitioner
status: docs-checked
description: "Return BOOL plus an NSError ** for recoverable failures, test the return value rather than the error, guard the NULL pointer and define your own error domain."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/ErrorHandling/ErrorHandling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NSError pattern
**Goal:** report recoverable errors the Cocoa way.

```objc
- (BOOL)doSomethingThatMayGenerateAnError:(NSError **)errorPtr {
    // ...
    if (errorPtr) {
        *errorPtr = [NSError errorWithDomain:domain code:-101 userInfo:userInfo];
    }
    return NO;
}

NSError *anyError;
BOOL success = [receivedData writeToURL:someLocalFileURL options:0 error:&anyError];
if (!success) {
    NSLog(@"Write failed with error: %@", anyError);
}
```
- Use `NSError` for all errors other than programmer errors. An `NSError` holds a numeric code, a domain, a description and a user info dictionary; Cocoa errors are divided into domains instead of unique global codes.
- For errors passed by reference, test the method's return value (`NO` here), not whether the error pointer was set. Pass `NULL` for `error:` if you do not need the object.
- When writing such a method, take an `NSError **` parameter, use the return value to signal success or failure, and check that the pointer is non-`NULL` before assigning through it.
- Define your own error domain of the form `com.companyName.appOrFrameworkName.ErrorDomain`, pick a unique code per error, and store the description under `NSLocalizedDescriptionKey` in the user info dictionary.
- Look up the description with `NSLocalizedString(@"Unable to…", @"")` so it is localized from `Localizable.strings`.
- Delegate methods such as `connection:didFailWithError:` hand you an `NSError` for asynchronous failures.
- Recover transparently where possible; otherwise present the error (on OS X, `presentError:` on an `NSResponder`).

## Gotchas
- Dereferencing a `NULL` error pointer crashes; always check it first.

## Self-check
Pass `NULL` as the error argument and confirm nothing crashes.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Dealing with Errors" (NSError contents, by-reference pattern, return value test, NULL tip, error domain format, NSLocalizedDescriptionKey, NSLocalizedString). Removed: `NS_ERROR_ENUM`, `NSErrorDomain`, nullable annotations, `NSUnderlyingErrorKey` and other user-info keys, and the Swift `throws` import and Swift-caller claims (not on the page).
Method: documentation only; no commands were run.
