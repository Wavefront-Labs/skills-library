---
id: computing-software.software-engineering.objective-c.delegate-pattern
name: delegate-pattern
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-protocols, delegate-pattern]
level: practitioner
status: docs-checked
description: "Implement delegates and data sources as weak, protocol-typed id properties with optional methods guarded by respondsToSelector:."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingWithProtocols/WorkingWithProtocols.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/CustomizingExistingClasses/CustomizingExistingClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegate pattern
**Goal:** hand decisions to another object without retain cycles.

```objc
@protocol XYZPieChartViewDataSource <NSObject>
- (NSUInteger)numberOfSegments;
@optional
- (NSString *)titleForSegmentAtIndex:(NSUInteger)segmentIndex;
@end

@interface XYZPieChartView : NSObject
@property (weak) id <XYZPieChartViewDataSource> dataSource;
@end

if ([self.dataSource respondsToSelector:@selector(titleForSegmentAtIndex:)]) {
    // ask the data source for a title
}
```
- The object that needs the information keeps a property typed `id` plus the protocol, because the delegate can be of any class and only its conformance matters.
- Delegate and data source properties are usually `weak` to avoid strong reference cycles with the owner.
- Declaring the protocol on the property gives a compiler warning when you set it to an object that does not conform.
- Mark methods the delegate may skip `@optional` and check with `respondsToSelector:` before calling; make the protocol adopt `NSObject` so that check compiles on `id <Protocol>`.
- A table view is the guide's model: `NSTableView` and `UITableView` leave decisions about content to another object at runtime. Use delegation as an alternative to subclassing when a class should stay reusable.

## Gotchas
- A delegate need not implement `@optional` methods, so check each before calling it.

## Self-check
Search for calls to `@optional` delegate methods that are not guarded.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Working with Protocols" (data source / delegate property, weak, optional methods, respondsToSelector:) and "Customizing Existing Classes" (delegation as an alternative). Removed: `should`/`will`/`did` naming rules, bit-field caching, threading advice and the BOOL-on-nil default claim (not on those pages).
Method: documentation only; no commands were run.
