---
id: computing-software.software-engineering.objective-c.class-interface-implementation
name: class-interface-implementation
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-classes, class-interface-implementation]
level: intro
status: docs-checked
description: "Split a class into a public @interface in a header and an @implementation in a source file, using #import and @class forward declarations."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/DefiningClasses/DefiningClasses.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocDefiningClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class interface and implementation
**Goal:** declare a class's public API in a header and define it in a source file.

```objc
// Person.h
@class Address;                       // forward declaration, no import needed
@interface Person : NSObject
- (void)sayHello;                     // instance method: minus sign
+ (Person *)person;                   // class method: plus sign
@end

// Person.m
#import "Person.h"
@implementation Person
- (void)sayHello { NSLog(@"Hello, world!"); }
@end
```
- The public properties and behaviour are declared in `@interface`; at a minimum a class inherits from `NSObject`, the root class, or from a Cocoa class closer to the behaviour you need.
- Class methods (usable by the class object) are preceded by a plus sign, instance methods by a minus sign.
- `#import` is like C `#include` but includes a file only once. The interface file must be imported into any source module that creates instances, sends messages to the class or mentions its ivars.
- If an interface mentions classes outside its own hierarchy it must import them or declare them with `@class`. `@class` is the simplest forward declaration and avoids problems when two interface files import each other.

## Gotchas
- Declaring a method without implementing it produces an "Incomplete implementation" compiler warning.

## Self-check
Compile the class and check no incomplete-implementation warning appears.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Defining Classes" and The Objective-C Programming Language, "Defining a Class" (interface/implementation, plus/minus, `#import`, `@class`, incomplete implementation warning). Removed: `NS_ASSUME_NONNULL`, `NS_DESIGNATED_INITIALIZER`, the later-method-without-declaration remark, the unrecognized-selector runtime claim and the clang flags self-check (not on those pages).
Method: documentation only; no commands were run.
