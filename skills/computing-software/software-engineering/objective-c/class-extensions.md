---
id: computing-software.software-engineering.objective-c.class-extensions
name: class-extensions
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-classes, class-extensions]
level: practitioner
status: docs-checked
description: "Use a class extension (anonymous category) for private properties and ivars and to redeclare a readonly property as readwrite inside the implementation file."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/CustomizingExistingClasses/CustomizingExistingClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class extensions
**Goal:** keep private state out of the public header.

```objc
// XYZPerson.h
@interface XYZPerson : NSObject
@property (readonly) NSString *uniqueIdentifier;
- (void)assignUniqueIdentifier;
@end

// XYZPerson.m
@interface XYZPerson ()                       // empty parentheses = class extension, not a category
@property (readwrite) NSString *uniqueIdentifier;
@end
@implementation XYZPerson
// ...
@end
```
- A class extension can only be added to a class whose source you compile at the same time; you cannot declare one on a framework class such as `NSString`. Methods it declares must be implemented in the class's primary `@implementation`.
- Because no name is given in the parentheses, extensions are called anonymous categories. Unlike a category, an extension can add properties and instance variables; a property declared there gets a synthesized accessor and instance variable.
- Instance variables can be declared in braces in the extension: `@interface XYZPerson () { id _someCustomInstanceVariable; }`.
- A common use is a `readonly` property in the header redeclared `readwrite` in the extension; `readwrite` is the default and optional there. The compiler then synthesizes the setter, and code outside the file that sets the property gets a compile error.
- To share "private" members with related classes, declare the extension in a separate header (for example `XYZPersonPrivate.h`) and import it only where needed; release only the public header.

## Gotchas
- The setter exists at runtime on every instance even if other files do not see the extension; `performSelector:` style calls can bypass the compiler error, which the guide says to avoid by designing the public interface properly.
- `@interface XYZPerson ()` and `@interface XYZPerson (Name)` differ: only the empty-parentheses form is an extension.

## Self-check
Assign to the redeclared property from a file that only imports the public header: it must fail to compile.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Customizing Existing Classes" (class extensions, anonymous category, ivars in braces, readonly to readwrite, private header). Removed: the copy-vs-strong redeclaration warning claim, the "friend classes in the same module" wording, generic `NSMutableArray` example (not on the page).
Method: documentation only; no commands were run.
