---
id: computing-software.software-engineering.objective-c.ns-swift-annotations
name: ns-swift-annotations
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-swift-interop, ns-swift-annotations]
level: advanced
status: draft
description: "Shape the Swift API of Objective-C code with NS_SWIFT_NAME, NS_ENUM, NS_OPTIONS, NS_REFINED_FOR_SWIFT and NS_SWIFT_UNAVAILABLE."
sources:
  - https://developer.apple.com/documentation/swift
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Introduction/introObjectiveC.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Swift-facing annotations
**Goal:** make Objective-C APIs import into Swift idiomatically.

```objc
typedef NS_ENUM(NSInteger, ABCState) { ABCStateIdle, ABCStateRunning };           // Swift enum
typedef NS_OPTIONS(NSUInteger, ABCFlags) { ABCFlagA = 1 << 0, ABCFlagB = 1 << 1 }; // OptionSet
typedef NSString *ABCKey NS_TYPED_ENUM;                                            // struct-like constants
NS_SWIFT_NAME(Widget) @interface ABCWidget : NSObject
- (void)fetchWithID:(NSString *)i NS_SWIFT_NAME(fetch(id:));
- (void)internalThing NS_REFINED_FOR_SWIFT;       // imported with a leading double underscore
- (void)unsafe NS_SWIFT_UNAVAILABLE("Use the Swift API");
@end
```
- `NS_ENUM` and `NS_OPTIONS` (not plain `enum`) are imported as proper Swift types; `NS_CLOSED_ENUM` marks exhaustive ones.
- Swift strips redundant prefixes: `ABCStateIdle` becomes `.idle`.
- Add `NS_SWIFT_NAME` to factory methods to import as initializers: `+ (instancetype)widgetWithID:(NSString *)i NS_SWIFT_NAME(init(id:));`.
- Method with `NSError **` last parameter imports as `throws`; completion handler methods import as `async` in modern Swift.
- Nullability and lightweight generics shape optionality and element types.

## Gotchas
- Unannotated pointers import as implicitly unwrapped optionals.
- `NS_SWIFT_NAME` mistakes surface only in Swift code.

## Self-check
View the generated Swift interface in Xcode (Jump to Definition) and confirm names.
