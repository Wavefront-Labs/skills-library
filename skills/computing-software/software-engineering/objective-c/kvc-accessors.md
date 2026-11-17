---
id: computing-software.software-engineering.objective-c.kvc-accessors
name: kvc-accessors
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-kvc-kvo, kvc-accessors]
level: practitioner
status: docs-checked
description: "Read and write properties by string with valueForKey:, setValue:forKey:, key paths and the lookup order including ivar access."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueCoding/index.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueCoding/BasicPrinciples.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueCoding/SearchImplementation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key-Value Coding
**Goal:** access properties indirectly by name.

```objc
[person setValue:@"Ada" forKey:@"name"];
NSString *n = [person valueForKey:@"name"];
NSNumber *zip = [person valueForKeyPath:@"address.zipCode"];
[person setValuesForKeysWithDictionary:@{ @"name": @"Ada", @"age": @36 }];
NSDictionary *d = [person dictionaryWithValuesForKeys:@[@"name", @"age"]];
```
- Getter lookup order for `valueForKey:`: first accessor found among `get<Key>`, `<key>`, `is<Key>`, `_<key>`; then the collection forms (`countOf<Key>` with `objectIn<Key>AtIndex:` or `<key>AtIndexes:`); then, if `+accessInstanceVariablesDirectly` returns YES, the ivars `_<key>`, `_is<Key>`, `<key>`, `is<Key>`; otherwise `valueForUndefinedKey:`, which raises `NSUndefinedKeyException` by default.
- Setter order: `set<Key>:`, then `_set<Key>`, then ivars `_<key>`, `_is<Key>`, `<key>`, `is<Key>` when direct access is allowed; otherwise `setValue:forUndefinedKey:`.
- Scalars and structs are wrapped as NSNumber/NSValue; setting nil on a non-object property calls `setNilValueForKey:`, which raises `NSInvalidArgumentException` by default.
- Collections: `mutableArrayValueForKey:` returns a mutable proxy array; a key path with a to-many key before the last key returns a collection of the values (for example `transactions.payee` returns an array).
- Override `+accessInstanceVariablesDirectly` to return NO to stop ivar access.
- Keys are ASCII strings with no whitespace, usually starting lowercase; a key path is dot-separated keys.

## Gotchas
- A typo in a key string is a runtime exception, not a compile error.
- `dictionaryWithValuesForKeys:` and `setValuesForKeysWithDictionary:` translate between `NSNull` in the dictionary and nil in the property.

## Self-check
Call `valueForKey:@"missing"` in a test and assert the `NSUndefinedKeyException`.

## Checked
2026-11-08. Confirmed against the Apple archive KVC guide: About Key-Value Coding, Accessing Object Properties (valueForKey:, valueForKeyPath:, dictionaryWithValuesForKeys:, setValue:forKey:, setValuesForKeysWithDictionary:, setNilValueForKey:, NSNull translation, to-many key paths, key rules) and Accessor Search Patterns (getter and setter order, accessInstanceVariablesDirectly, undefined-key methods). Corrected the exception name (NSUndefinedKeyException, not NSUnknownKeyException) and the setter order. Removed the claim that direct access is on by default, the NSStringFromSelector tip and the private-ivar remark, which those pages do not state.
Method: documentation only; no commands were run.
