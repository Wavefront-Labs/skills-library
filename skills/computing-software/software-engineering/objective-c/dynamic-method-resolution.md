---
id: computing-software.software-engineering.objective-c.dynamic-method-resolution
name: dynamic-method-resolution
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-runtime, dynamic-method-resolution]
level: advanced
status: docs-checked
description: "Provide a method implementation lazily with +resolveInstanceMethod: and class_addMethod, and know how it relates to @dynamic and forwarding."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtDynamicResolution.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtForwarding.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic method resolution
**Goal:** supply an implementation when a message arrives for a method the class does not have.

```objc
void dynamicMethodIMP(id self, SEL _cmd) {
    // implementation ....
}
@implementation MyClass
+ (BOOL)resolveInstanceMethod:(SEL)aSEL {
    if (aSEL == @selector(resolveThisMethodDynamically)) {
        class_addMethod([self class], aSEL, (IMP) dynamicMethodIMP, "v@:");
        return YES;
    }
    return [super resolveInstanceMethod:aSEL];
}
@end
```
- Implement `resolveInstanceMethod:` for instance methods and `resolveClassMethod:` for class methods.
- An Objective-C method is a C function taking at least `self` and `_cmd`; `class_addMethod` adds such a function to a class. `"v@:"` is the type string used in the guide's example; in the Type Encodings table `v` is void, `@` an object and `:` a selector.
- The `@dynamic propertyName;` directive tells the compiler the property's methods will be provided dynamically.
- A class gets the chance to resolve a method dynamically before forwarding starts. If `respondsToSelector:` or `instancesRespondToSelector:` is called, the resolver also gets the first chance to supply an `IMP`.
- To have particular selectors go through forwarding anyway, return `NO` for them.

## Gotchas
- `respondsToSelector:` can trigger the resolver, so keep resolution safe to repeat.

## Self-check
Send the unimplemented message and confirm `dynamicMethodIMP` runs.

## Checked
2026-11-03. Confirmed against the Objective-C Runtime Programming Guide, "Dynamic Method Resolution" and "Message Forwarding". Removed: the exact dispatch-order list including `forwardingTargetForSelector:`, the Core Data `@dynamic` claim and the NSInvocation crash remark (not on those pages).
Method: documentation only; no commands were run.
