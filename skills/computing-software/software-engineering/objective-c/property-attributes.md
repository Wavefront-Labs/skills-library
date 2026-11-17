---
id: computing-software.software-engineering.objective-c.property-attributes
name: property-attributes
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-properties, property-attributes]
level: practitioner
status: docs-checked
description: "Choose atomicity, ownership (strong, weak, copy, assign) and access attributes for @property declarations."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/EncapsulatingData/EncapsulatingData.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocProperties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property attributes
**Goal:** pick attributes that match the ownership and threading intent.

```objc
@property (nonatomic, weak) id delegate;
@property (copy) NSString *firstName;
@property (readonly) NSString *fullName;
@property (getter=isFinished) BOOL finished;
@property (readonly, getter=isFinished) BOOL finished;
@property (unsafe_unretained) NSObject *unsafeProperty;
```
- Access: `readwrite` is the default; `readonly` synthesizes a getter only, and setting it with dot syntax is a compiler error. `getter=` / `setter=` rename accessors; Boolean getters customarily start with `is`.
- Ownership: properties and variables hold strong references by default (`strong` is the default and need not be written). `weak` does not keep the object alive and is set to `nil` when the object is deallocated. `copy` makes a copy on assignment and uses a strong reference to hold it. `unsafe_unretained` is for classes that do not support weak references; it is not set to `nil`, so it can dangle.
- `assign` means the setter uses simple assignment; `retain` sends retain on assignment (older reference-counted style).
- Atomicity: properties are atomic by default; `nonatomic` makes synthesized accessors set or return the value directly, with no thread guarantees, and is faster.
- If you write the accessors yourself, they must match the declared attributes (for example copy in the setter when `copy` is declared).

## Gotchas
- In a reference-counted environment, an atomic accessor for a `strong`, `copy` or `retain` property uses a lock and retains and autoreleases the returned value; `nonatomic` avoids this.
- A weak property can become `nil` between a test and a use on another thread; cache it in a strong local variable first.
- Strong references in a cycle keep each other alive; make one side weak (for example a delegate).

## Self-check
Compile a class with each attribute above and confirm that assigning to a `readonly` property with dot syntax is an error.

## Checked
2026-11-08. Confirmed against the archived "Programming with Objective-C" chapter on encapsulating data and the "Objective-C Programming Language" chapter on declared properties: access, getter naming, strong/weak/copy/unsafe_unretained, assign and retain, atomic default and cost. Removed: `nullable`/`nonnull` annotations, class properties, block-copy advice, `-Wall` warning self-check, "conventional on iOS" claim (not on the pages). The pages are marked retired documents.
Method: documentation only; no commands were run.
