---
id: computing-software.software-engineering.objective-c.category-collisions
name: category-collisions
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-categories, category-collisions]
level: advanced
status: docs-checked
description: "Avoid duplicate category method names, whose winner at runtime is undefined, by prefixing category methods on framework classes."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/CustomizingExistingClasses/CustomizingExistingClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Category collisions
**Goal:** prevent two categories from silently shadowing each other.

- If a category method has the same name as a method in the original class, in another category on the same class, or even in a superclass, the behaviour is undefined as to which implementation is used at runtime.
- The risk is small with your own classes and real with Cocoa classes: two frameworks can each add `base64EncodedString` to `NSString`, and only one wins.
- A later OS release can add a method you had added yourself. The guide's example is `NSSortDescriptor`, which gained `sortDescriptorWithKey:ascending:` in Mac OS X 10.6 and iOS 4.0, clashing with a category that supplied it.
- Best practice is a prefix on every category method added to a framework class: the lowercase class-prefix letters, an underscore, then the name.

```objc
@interface NSSortDescriptor (XYZAdditions)
+ (id)xyz_sortDescriptorWithKey:(NSString *)key ascending:(BOOL)ascending;
@end
```

## Gotchas
- A symptom of a clash is behaviour that changes with the framework version or link order; rename to a prefixed selector rather than relying on either winning.

## Self-check
List the methods your categories add to framework classes and confirm every one carries your prefix.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Customizing Existing Classes" (avoid category method name clashes, prefix convention, NSSortDescriptor example). Removed: clang warning names, `-Wobjc-protocol-method-implementation`, `class_copyMethodList`, `+load` ordering, `nm` / `otool` inspection and the link-order symptom (not on the page).
Method: documentation only; no commands were run.
