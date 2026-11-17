---
id: computing-software.software-engineering.objective-c.kvo-observing
name: kvo-observing
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-kvc-kvo, kvo-observing]
level: practitioner
status: docs-checked
description: "Register observers with addObserverForKeyPath:options:context:, implement observeValueForKeyPath, and unregister reliably."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/KeyValueObserving.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/Articles/KVOBasics.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/Articles/KVOCompliance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KVO observing
**Goal:** react to property changes on other objects.

```objc
static void *kCtx = &kCtx;
[model addObserver:self forKeyPath:@"progress"
           options:NSKeyValueObservingOptionNew | NSKeyValueObservingOptionInitial
           context:kCtx];

- (void)observeValueForKeyPath:(NSString *)kp ofObject:(id)obj change:(NSDictionary *)change context:(void *)ctx {
    if (ctx != kCtx) { [super observeValueForKeyPath:kp ofObject:obj change:change context:ctx]; return; }
    NSNumber *v = change[NSKeyValueChangeNewKey];
}
- (void)dealloc { [model removeObserver:self forKeyPath:@"progress" context:kCtx]; }
```
- Observed property must be KVO-compliant: KVC-compliant for the property; NSObject then emits automatic notifications for changes made through compliant accessors and KVC methods. Apple-framework properties are compliant only if documented as such.
- Use a unique `context` pointer per class or key path (the address of a static variable); call super for any context you do not recognise, because a superclass may also be observing.
- Pair each `addObserver` with one `removeObserver:forKeyPath:context:`. Removing an observer that is not registered raises `NSRangeException`. An observer is not removed automatically on dealloc, and a notification sent to a released observer triggers a memory access exception.
- Typical pattern: register in `init` or `viewDidLoad`, unregister in `dealloc`.
- Options: `New`, `Old`, `Initial` (immediate notification before `addObserver` returns), `Prior` (extra notification before the change, flagged by `NSKeyValueChangeNotificationIsPriorKey`).

## Gotchas
- `addObserver:forKeyPath:options:context:` does not retain the observer, the observed object or the context; keep them alive yourself.
- If a notification reaches NSObject's implementation (no subclass consumed it), NSObject throws `NSInternalInconsistencyException`.
- For to-many properties the change dictionary also carries `NSKeyValueChangeKindKey` (insertion, removal, replacement) and `NSKeyValueChangeIndexesKey`.

## Self-check
Observe and release the observer without removing; confirm the crash, then fix.

## Checked
2026-11-08. Confirmed against the Apple archive KVO guide: Introduction, Registering for Key-Value Observing (options, context, observeValueForKeyPath, removeObserver rules, NSRangeException, no retain, NSInternalInconsistencyException) and KVO Compliance (automatic notification). Removed the Swift NSKeyValueObservation remark, the double-registration claim, the thread claim and the quoted deallocation message, which those pages do not state.
Method: documentation only; no commands were run.
