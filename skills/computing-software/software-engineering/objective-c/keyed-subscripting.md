---
id: computing-software.software-engineering.objective-c.keyed-subscripting
name: keyed-subscripting
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-subscripting, keyed-subscripting]
level: practitioner
status: docs-checked
description: "Support obj[key] reads and writes by implementing objectForKeyedSubscript: and setObject:forKeyedSubscript:."
sources:
  - https://clang.llvm.org/docs/ObjectiveCLiterals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Keyed subscripting
**Goal:** make `container[key]` work on your own class.

```objc
@interface ABCSettings : NSObject
- (id)objectForKeyedSubscript:(id)key;
- (void)setObject:(id)obj forKeyedSubscript:(id)key;
@end
settings[@"theme"] = @"dark";    // [settings setObject:@"dark" forKeyedSubscript:@"theme"]
id t = settings[@"theme"];       // [settings objectForKeyedSubscript:@"theme"]
```
- When the subscript has an Objective-C object pointer type, a read becomes `objectForKeyedSubscript:` and a write becomes `setObject:forKeyedSubscript:`.
- The behaviour of the setter is class specific; in general it should replace an existing value for the key, otherwise add one. The page provides no syntax for removing elements.
- The compiler picks keyed or indexed form from the subscript type (object pointer vs integer), so a class may support both.
- A class need not declare both methods.
- Subscript expressions are l-values; compound assignment is ill-formed.
- Under `id`, normal dynamic send rules apply: the compiler must see some declaration of the methods and takes the first seen.

## Self-check
Subscript a custom class with an object key and with an integer index; check each picks the matching method.

## Checked
2026-11-02. Confirmed against the Clang "Objective-C Literals" page (Dictionary-Style Subscripting and Discussion). Removed: nil-removes-key claim (the page says no removal syntax), `id<NSCopying>` parameter type, NSDictionary/NSMutableDictionary capability list.
Method: documentation only; no commands were run.
