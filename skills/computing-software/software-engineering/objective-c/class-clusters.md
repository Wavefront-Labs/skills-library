---
id: computing-software.software-engineering.objective-c.class-clusters
name: class-clusters
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-classes, class-clusters]
level: advanced
status: docs-checked
description: "Understand class clusters like NSArray and NSNumber, subclass them correctly, and build your own abstract-factory cluster."
sources:
  - https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ClassClusters/ClassClusters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class clusters
**Goal:** know why `[NSArray alloc]` can return an instance of a private subclass and how to subclass clusters safely.

- A class cluster groups private concrete subclasses under a public abstract superclass and is based on the Abstract Factory pattern. Foundation clusters include NSData/NSMutableData, NSArray/NSMutableArray, NSDictionary/NSMutableDictionary, NSString/NSMutableString, and NSNumber.
- The abstract superclass dispenses the instance of the proper private subclass based on the creation method you call; you do not and cannot choose the class. Two NSNumber objects created with different factory methods may belong to different private subclasses.
- To extend a cluster, either create a true subclass (when you must manage storage) or a composite object that embeds a standard Foundation object and forwards to it.
- A true subclass must: subclass the cluster's abstract superclass, declare its own storage (the abstract class declares no ivars), override all initializer methods of the superclass, and override its primitive methods (for NSArray: `count` and `objectAtIndex:`). Derived methods such as `lastObject` and `containsObject:` then work unchanged.
- The abstract superclass's designated initializer is always `init`; your subclass should declare its own initializers, not rely on inherited ones, and call its superclass's designated initializer.
- A composite object is declared as a subclass of the abstract superclass and overrides its primitive methods, relaying them to the embedded object, for example `- (NSUInteger)count { return [embedded count]; }`.
- Building your own cluster: the abstract class declares the creation methods and decides which private subclass to return:
```objc
@implementation Shape
+ (instancetype)shapeWithKind:(NSString *)kind {
    if ([kind isEqualToString:@"circle"]) return [[CircleShape alloc] init];
    return [[SquareShape alloc] init];
}
@end
```

## Gotchas
- Class membership is hidden, so do not depend on the concrete class of a returned object; the Apple guide notes the trade-off that subclassing a cluster is harder than subclassing an ordinary class.
- Methods that return an immutable-typed object (for example `- (NSString *)title`) signal that the result cannot be modified; modification attempts draw a compiler warning.

## Self-check
Print `NSStringFromClass([[NSMutableArray array] class])` and confirm it differs from "NSMutableArray".

## Checked
2026-11-08. Confirmed against Apple's archive Cocoa Encyclopedia chapter Class Clusters (definition, Abstract Factory, creating instances, clusters with multiple public superclasses, true subclass requirements, primitive and derived methods, designated initializer, composite objects). Removed the private class name `__NSArrayI`, the `isKindOfClass:` versus `isMemberOfClass:` advice, the `doesNotRecognizeSelector:` abstract-method idiom and the OS-version remark about class names, which that page does not state. The final self-check line is an observation of the hidden-class behaviour the guide describes, not a verified output.
Method: documentation only; no commands were run.
