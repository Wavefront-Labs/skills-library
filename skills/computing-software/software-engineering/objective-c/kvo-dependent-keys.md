---
id: computing-software.software-engineering.objective-c.kvo-dependent-keys
name: kvo-dependent-keys
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-kvc-kvo, kvo-dependent-keys]
level: advanced
status: docs-checked
description: "Register dependent keys with keyPathsForValuesAffecting<Key> and control notifications with automaticallyNotifiesObserversForKey: and willChange/didChangeValueForKey:."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/Articles/KVODependentKeys.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/Articles/KVOCompliance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KVO dependent keys and manual notification
**Goal:** notify observers of computed properties and of changes you announce yourself.

```objc
+ (NSSet *)keyPathsForValuesAffectingFullName {
    return [NSSet setWithObjects:@"lastName", @"firstName", nil];
}
+ (BOOL)automaticallyNotifiesObserversForKey:(NSString *)theKey {
    BOOL automatic = NO;
    if ([theKey isEqualToString:@"balance"]) {
        automatic = NO;
    } else {
        automatic = [super automaticallyNotifiesObserversForKey:theKey];
    }
    return automatic;
}
- (void)setTotalSalary:(NSNumber *)newTotalSalary {
    if (totalSalary != newTotalSalary) {
        [self willChangeValueForKey:@"totalSalary"];
        _totalSalary = newTotalSalary;
        [self didChangeValueForKey:@"totalSalary"];
    }
}
```
- To-one dependents: override `keyPathsForValuesAffectingValueForKey:` (call `super` and add to its set) or implement a class method named `keyPathsForValuesAffecting<Key>`, with the key's first letter capitalized. In a category you cannot override methods, so use the named class method.
- `keyPathsForValuesAffectingValueForKey:` does not support key paths through a to-many relationship (for example `employees.salary`). Instead observe the attribute on each child and update the dependent value yourself, or with Core Data observe the managed object context's change notifications.
- NSObject provides automatic notification for changes made through KVC-compliant accessors, `setValue:forKey:`, key paths and collection proxies such as `mutableArrayValueForKey:`.
- To control notifications for a key, override `automaticallyNotifiesObserversForKey:` and return `NO` for it; then bracket the change with `willChangeValueForKey:` and `didChangeValueForKey:`. Automatic and manual notification can coexist.
- Manual notification lets you skip unnecessary notifications (as the `!=` check above does) or group several changes into one.

## Gotchas
- The ivar assignment is only announced if you bracket it yourself when automatic notification is off for that key.

## Self-check
Change `firstName` and confirm an observer of `fullName` is notified.

## Checked
2026-11-03. Confirmed against Apple's Key-Value Observing Programming Guide, "Registering Dependent Keys" and "KVO Compliance" (keyPathsForValuesAffecting, to-many limitation, automatic vs manual notification, automaticallyNotifiesObserversForKey:). Removed: `willChange:valuesAtIndexes:forKey:`, the `@count` observability claim, "exactly once" and mismatched will/did claims (not on those pages).
Method: documentation only; no commands were run.
