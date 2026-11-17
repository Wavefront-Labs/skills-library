---
id: computing-software.software-engineering.objective-c.property-copy-semantics
name: property-copy-semantics
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-properties, property-copy-semantics]
level: practitioner
status: docs-checked
description: "Use the copy property attribute so a mutable value assigned to a property is captured, and copy by hand when setting the ivar."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/EncapsulatingData/EncapsulatingData.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# copy semantics
**Goal:** prevent aliasing bugs when a mutable object is assigned to a property.

```objc
@property (copy) NSString *firstName;
@property (copy) NSString *lastName;
```
- With the default strong attribute a property keeps a reference to the very object assigned, so later mutation of that object (for example an `NSMutableString`) changes the property's value.
- The `copy` attribute captures the object at the time the property is set: the property holds an unaffected copy of the original.
- `copy` uses a strong reference, because it must hold on to the new object it creates.
- Any object set for a `copy` property must support `NSCopying`, that is conform to the `NSCopying` protocol.
- When you set the instance variable of a copy property directly, for example in an initializer, set a copy yourself:
```objc
_instanceVariableForCopyProperty = [aString copy];
```

## Self-check
Set a mutable string as the property value, mutate that string, and confirm the property value did not change.

## Checked
2026-11-08. Confirmed against the archived "Programming with Objective-C" chapter on encapsulating data (Copy Properties Maintain Their Own Copies): strong aliasing, copy capture, strong reference, `NSCopying` requirement, direct ivar copy. Removed: claims about `copy` on immutable objects, `mutableCopy` and `NSMutableArray` properties, `copyWithZone:` example, shallow-copy gotcha, block and collection property advice, Memory Management guide source (not read). The page is a retired document.
Method: documentation only; no commands were run.
