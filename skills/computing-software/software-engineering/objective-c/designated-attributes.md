---
id: computing-software.software-engineering.objective-c.designated-attributes
name: designated-attributes
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-attributes, designated-attributes]
level: practitioner
status: draft
description: "Use clang attribute macros to enforce subclass contracts: NS_REQUIRES_SUPER, NS_UNAVAILABLE, NS_DESIGNATED_INITIALIZER and NS_NOESCAPE."
sources:
  - https://clang.llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contract attributes
**Goal:** let the compiler enforce API contracts.

```objc
- (void)reset NS_REQUIRES_SUPER;                         // overrides must call [super reset]
- (instancetype)init NS_UNAVAILABLE;                      // calling it is a compile error
- (instancetype)initWithID:(int)i NS_DESIGNATED_INITIALIZER;
- (void)run:(void (NS_NOESCAPE ^)(void))work;             // block does not outlive the call
+ (void)setup NS_SWIFT_UNAVAILABLE("Use init");
- (void)refresh NS_REFINED_FOR_SWIFT;
```
- These macros wrap clang `__attribute__((objc_requires_super))`, `((unavailable))`, `((objc_designated_initializer))`, `((noescape))`.
- Subclass override missing the super call yields a warning (`-Wobjc-missing-super-calls`).
- `NS_NOESCAPE` documents that a block parameter is not stored, allowing Swift to treat it as non-escaping.
- `NS_RETURNS_INNER_POINTER` flags that a returned pointer is valid only while the object lives.
- `NS_ERROR_ENUM`, `NS_CLOSED_ENUM`, `NS_TYPED_ENUM` apply to enums and constants.

## Gotchas
- Attributes do not change runtime behaviour, only diagnostics.
- Macro names are defined by Foundation headers; the underlying attribute spellings are clang-defined.

## Self-check
Override a `NS_REQUIRES_SUPER` method without calling super and confirm the warning.
