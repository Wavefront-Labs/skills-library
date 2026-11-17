---
id: computing-software.software-engineering.objective-c.category-methods
name: category-methods
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-categories, category-methods]
level: practitioner
status: docs-checked
description: "Extend existing classes with category methods, prefix method names on framework classes, and know that categories cannot add instance variables."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/CustomizingExistingClasses/CustomizingExistingClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Category methods
**Goal:** add behaviour to a class you do not own without subclassing.

```objc
// XYZPerson+XYZPersonNameDisplayAdditions.h
@interface XYZPerson (XYZPersonNameDisplayAdditions)
- (NSString *)lastNameFirstNameString;
@end

// XYZPerson+XYZPersonNameDisplayAdditions.m
#import "XYZPerson+XYZPersonNameDisplayAdditions.h"
@implementation XYZPerson (XYZPersonNameDisplayAdditions)
- (NSString *)lastNameFirstNameString {
    return [NSString stringWithFormat:@"%@, %@", self.lastName, self.firstName];
}
@end
```
- A category can be declared for any class, even without its source (Cocoa classes included). Its methods are available to all instances and subclasses; at runtime there is no difference from a method in the original class.
- Declare a category in its own header and implement it in its own file, for example `XYZPerson+XYZPersonNameDisplayAdditions.h`; import that header wherever you use the methods or you get compiler warnings and errors.
- Categories can declare instance or class methods and can split a complex class across several files.
- A category cannot add an instance variable. A property declared there is valid syntax but the compiler synthesizes no ivar and no accessors; you would have to write accessors and have somewhere to store the value. A traditional property needs a class extension, or associative references via the runtime for framework classes.
- Prefix category methods on framework classes: lowercase class prefix, underscore, then the name, for example `xyz_sortDescriptorWithKey:ascending:` on `NSSortDescriptor`.

## Gotchas
- If a category method has the same name as one in the original class, another category, or a superclass, which implementation runs is undefined.
- A method you add may later be added by the framework itself (the guide's example is `sortDescriptorWithKey:ascending:`), which is the reason to prefix.

## Self-check
Grep your categories on framework classes for methods without a prefix.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective C, "Customizing Existing Classes" (category syntax, file naming, import requirement, no ivars or synthesis, name clashes, prefix convention). Removed: the `-ObjC` linker flag claim, the class-cluster remark and the `abc_slug` example (not on the page).
Method: documentation only; no commands were run.
