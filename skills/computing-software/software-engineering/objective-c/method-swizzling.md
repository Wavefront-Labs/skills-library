---
id: computing-software.software-engineering.objective-c.method-swizzling
name: method-swizzling
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-runtime, method-swizzling]
level: sme
status: docs-checked
description: "Swap implementations safely with class_addMethod, class_replaceMethod and method_exchangeImplementations."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Introduction/Introduction.html
  - https://raw.githubusercontent.com/apple-oss-distributions/objc4/main/runtime/runtime.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Method swizzling
**Goal:** replace or wrap an existing method at runtime with minimal risk.

```objc
#import <objc/runtime.h>
@implementation UIViewController (ABCTrack)
+ (void)abc_swizzle {                           // call once, early at launch
    Class c = self;
    SEL orig = @selector(viewWillAppear:), repl = @selector(abc_viewWillAppear:);
    Method om = class_getInstanceMethod(c, orig), rm = class_getInstanceMethod(c, repl);
    if (class_addMethod(c, orig, method_getImplementation(rm), method_getTypeEncoding(rm)))
        class_replaceMethod(c, repl, method_getImplementation(om), method_getTypeEncoding(om));
    else
        method_exchangeImplementations(om, rm);
}
- (void)abc_viewWillAppear:(BOOL)animated {
    [self abc_viewWillAppear:animated];         // calls the ORIGINAL (implementations are swapped)
    NSLog(@"appear %@", self);
}
@end
```
- `class_addMethod` returns YES if it added the method and NO if the class already has an implementation with that name. It adds an override of a superclass's implementation but never replaces an existing implementation in that class.
- `class_replaceMethod` adds the method if it does not exist, otherwise replaces its IMP (the type encoding is then ignored) and returns the previous implementation.
- `method_exchangeImplementations(m1, m2)` is an atomic version of reading both IMPs and setting each on the other method.
- The add-first pattern means that when the class only inherits the method, the swap happens on this class and not on the superclass.
- An implementation function must take at least `self` and `_cmd`; the type string's second and third characters must be `@:` (the first is the return type).
- Give the new selector a prefix of your own so it cannot collide with an existing method.

## Gotchas
- After the exchange the two selectors point at each other's implementations, so the new method calls its own selector to reach the original.
- The sources read do not discuss App Store policy or interplay between two libraries swizzling the same method; check current rules and test.

## Self-check
Log from the swizzled method, run the app, and confirm the original behaviour is preserved.

## Checked
2026-11-08. Confirmed against the objc4 `runtime.h` header: class_addMethod and class_replaceMethod semantics and return values, method_exchangeImplementations, the `self`/`_cmd`/`@:` rule, and method_getImplementation and method_getTypeEncoding. The Runtime Programming Guide introduction page was read only for its scope (the chapters were not read). Removed the claims about doing the swizzle in `+load` under `dispatch_once`, preserving `_cmd`, preferring alternatives such as subclassing, and the multi-library chaining statement, which no readable source states; the example now just calls a one-time setup method.
Method: documentation only; no commands were run.
