---
id: computing-software.software-engineering.objective-c.message-forwarding
name: message-forwarding
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-runtime, message-forwarding]
level: sme
status: docs-checked
description: "Forward unrecognized messages with forwardInvocation:, supply method signatures, and make respondsToSelector: reflect forwarding."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtForwarding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message forwarding
**Goal:** redirect messages an object does not handle to another object.

```objc
- (void)forwardInvocation:(NSInvocation *)anInvocation {
    if ([someOtherObject respondsToSelector:[anInvocation selector]])
        [anInvocation invokeWithTarget:someOtherObject];
    else
        [super forwardInvocation:anInvocation];
}
- (NSMethodSignature *)methodSignatureForSelector:(SEL)selector {
    NSMethodSignature *signature = [super methodSignatureForSelector:selector];
    if (!signature) {
        signature = [surrogate methodSignatureForSelector:selector];
    }
    return signature;
}
```
- Before announcing an error for an unhandled message, the runtime sends the receiver `forwardInvocation:` with an `NSInvocation` that holds the original message and arguments. `NSObject`'s version just calls `doesNotRecognizeSelector:`.
- A `forwardInvocation:` override determines where the message should go and sends it there with the original arguments, usually via `invokeWithTarget:`. The return value goes back to the original sender, and any return type works (objects, structures, doubles).
- It only runs for messages the receiver has no method for: if the class implements `negotiate` itself, that message never reaches `forwardInvocation:`.
- Forwarding can imitate multiple inheritance, build lightweight surrogate objects that create the real object lazily, or swallow messages.
- `respondsToSelector:` and `isKindOfClass:` look only at the inheritance hierarchy, so to make forwarding transparent re-implement them (plus `instancesRespondToSelector:`, and `conformsToProtocol:` if protocols are used) to include the forwarding chain.
- Override `methodSignatureForSelector:` so it returns accurate signatures for the methods that ultimately respond.

## Gotchas
- The guide calls forwarding an advanced technique for when no other solution is possible; it is not a replacement for inheritance.

## Self-check
Send a forwarded message and confirm the other object answers, then check `respondsToSelector:` after your override.

## Checked
2026-11-03. Confirmed against the Objective-C Runtime Programming Guide, "Message Forwarding" (forwardInvocation:, invokeWithTarget:, surrogates, respondsToSelector: and methodSignatureForSelector: overrides, advanced-technique note). Removed: `forwardingTargetForSelector:`, `NSProxy` weak-target and timer advice, `NSInvalidArgumentException` and performance claims (not on the page).
Method: documentation only; no commands were run.
