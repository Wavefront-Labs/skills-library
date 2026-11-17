---
id: computing-software.software-engineering.objective-c.protocol-declaration
name: protocol-declaration
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-protocols, protocol-declaration]
level: practitioner
status: docs-checked
description: "Declare a formal @protocol with @required and @optional sections, make it adopt NSObject, call optional methods after respondsToSelector:, and forward declare it."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingWithProtocols/WorkingWithProtocols.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocProtocols.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protocol declaration
**Goal:** define an interface independent of class hierarchy.

```objc
@protocol XYZPieChartViewDataSource <NSObject>
- (NSUInteger)numberOfSegments;              // required by default
@optional
- (NSString *)titleForSegmentAtIndex:(NSUInteger)segmentIndex;
@required
- (CGFloat)valueForSegmentAtIndex:(NSUInteger)segmentIndex;
@end

if ([self.dataSource respondsToSelector:@selector(titleForSegmentAtIndex:)]) {
    // safe to call the optional method
}
```
- Declare with `@protocol Name ... @end`. If you give no keyword, methods are `@required`; `@optional` and `@required` partition the protocol and each applies until the end or the next directive.
- Once an `id` is qualified with a protocol, static type-checking applies: calling `respondsToSelector:` on `id<Protocol>` is a compile error unless the protocol adopts the `NSObject` protocol (`@protocol MyProtocol <NSObject>`).
- One protocol can incorporate others with the class adoption syntax: `@protocol Paging <Formatting>`.
- To break a circular import, forward-declare with `@protocol B;` instead of importing the header that defines it. This only tells the compiler B is a protocol defined later.
- A protocol name outside `@protocol()` is not an object; `@protocol(MyXMLSupport)` gives the `Protocol` object.
- Informal protocols (a category on `NSObject`) get no compile-time or runtime conformance checking; prefer a formal protocol with optional methods.

## Gotchas
- A class that adopts a protocol but omits a required method gets a compiler warning, not an error.
- Repeat the `respondsToSelector:` check at each call site of an optional method.

## Self-check
Remove a required method from a conforming class and confirm the compiler warns.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Working with Protocols" and The Objective-C Programming Language, "Protocols" (required/optional, NSObject adoption, respondsToSelector:, protocols within protocols, forward declaration, informal protocols). Removed: properties and class methods in protocols, caching advice and the `ABCDownloader` sample (not on those pages).
Method: documentation only; no commands were run.
