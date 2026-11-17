---
id: computing-software.software-engineering.objective-c.nullability-annotations
name: nullability-annotations
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-generics, nullability-annotations]
level: practitioner
status: gated
description: "Annotate headers with NS_ASSUME_NONNULL, nullable, _Nullable and null_resettable so Swift and the compiler see accurate optionality."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Introduction/introObjectiveC.html
  - https://developer.apple.com/documentation/swift
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nullability annotations
**Goal:** declare which pointers may be nil.

```objc
NS_ASSUME_NONNULL_BEGIN
@interface ABCUser : NSObject
@property (nonatomic, copy) NSString *name;                     // nonnull
@property (nonatomic, copy, nullable) NSString *nickname;
- (nullable ABCUser *)friendNamed:(NSString *)name;
- (void)fetchWithCompletion:(void (^)(NSData * _Nullable data, NSError * _Nullable error))done;
@end
NS_ASSUME_NONNULL_END
```
- Keywords: `nonnull`/`_Nonnull`, `nullable`/`_Nullable`, `null_unspecified`/`_Null_unspecified`, `null_resettable` (property whose getter never returns nil but setter accepts nil). (gated: unconfirmed, source is paywalled or blocked)
- Property/method form uses unprefixed keywords; plain pointer, block and typedef positions use `_Nullable` after the `*`.
- `NS_ASSUME_NONNULL_BEGIN/END` makes unannotated simple pointers nonnull; double pointers like `NSError **` still need explicit annotations (e.g. `NSError * _Nullable * _Nullable`).
- Swift maps nonnull to non-optional, nullable to Optional, unspecified to implicitly unwrapped.
- Warning flags: `-Wnullability`, `-Wnullable-to-nonnull-conversion`; the analyzer also checks.

## Gotchas
- Annotations are promises; clang does not insert runtime checks.
- Initializers should be `nullable` only if they can fail.

## Self-check
Pass `nil` to a nonnull parameter and confirm a warning appears.

## Checked
2026-11-02. Not confirmed: Apple pages were not readable; only the Clang `_Nullable`/`_Nonnull` attribute text was read, not the Objective-C keyword forms or NS_ASSUME_NONNULL. Claims left in place are unchecked; the first bullet carries the gate marker.
Method: documentation only; no commands were run.
