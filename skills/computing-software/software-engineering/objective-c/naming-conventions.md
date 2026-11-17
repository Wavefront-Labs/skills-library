---
id: computing-software.software-engineering.objective-c.naming-conventions
name: naming-conventions
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-style-lint, naming-conventions]
level: practitioner
status: docs-checked
description: "Apply Apple's Coding Guidelines for Cocoa to class prefixes, method names, parameters, accessors, and notification and constant naming."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CodingGuidelines/Articles/NamingBasics.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CodingGuidelines/Articles/NamingMethods.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cocoa naming conventions
**Goal:** names that read like the platform's own APIs.

- Prefixes: two or three uppercase letters, no underscores or sub-prefixes (`NS`, `AB`, `IB`). Use them for classes, protocols, functions, constants and typedef structures; do not prefix methods or struct fields.
- Classes: a noun with the prefix (`NSString`, `NSScanner`). Protocols that group behaviour not tied to a class use a gerund (`NSLocking`, not `NSLock`); a protocol tied to a principal class takes the class name (`NSObject`).
- Methods: start lowercase, capitalise embedded words, no prefix (exceptions: a leading well-known acronym such as `TIFFRepresentation`; private-method prefixes).
- Action methods start with a verb (`selectTabViewItem:`); no "do" or "does", no adverb or adjective before the verb.
- Keywords before every argument, and the word before the argument describes it: `- (id)viewWithTag:(NSInteger)aTag`, not `taggedView:`.
- Clarity over brevity, and do not abbreviate: `insertObject:atIndex:` not `insert:at:`; `setBackgroundColor:` not `setBkgdColor:`.
- Do not use "and" to link attributes of the receiver (`runModalForDirectory:file:types:`); use it only to join two separate actions (`openFile:withApplication:andDeactivate:`).
- Accessors: noun property `title` / `setTitle:`; adjective property `isEditable` / `setEditable:`; verb property `showsAlpha` / `setShowsAlpha:`. A getter takes no `get` prefix; use `get` only for methods that return values indirectly through pointer arguments.
- Collections: `addElement:`, `removeElement:`, `elements`; return an `NSSet` when the collection is truly unordered.
- Delegate methods start with the sending class name without its prefix and with a lowercase first letter (`tableView:shouldSelectRow:`); use `did` or `will` for notifications of events, `should` to ask the delegate. Notification-based delegate methods take the notification as sole argument (`windowDidChangeScreen:`).
- Arguments: lowercase start, no "pointer" or "ptr", avoid one- and two-letter names.
- Private methods: do not use a leading underscore (Apple reserves it); a unique prefix of your own is the suggested alternative. A leading underscore on an instance variable is allowed.
- Header files: an isolated class goes in a file named after it (`NSLocale.h`); a category on another framework's class uses an `Additions` suffix.

## Gotchas
- A name can be ambiguous: `sendPort` (send it, or return it?) and `displayName`.
- Names should not be self-referential (`NSStringObject`), except for masks and notification names.

## Self-check
Compare your public API with a similar Apple class (for example NSArray methods) for style.

## Checked
2026-11-08. Confirmed against Apple's archive Coding Guidelines for Cocoa: Introduction, Code Naming Basics (prefix format, typographic conventions, class and protocol names, header files) and Naming Methods (general rules, accessors, delegate methods, collection methods, arguments, private methods). Removed the claim that Apple reserves two-letter prefixes, the factory-method, notification-name, constant (`kPrefixName`) and enum-member rules, and the category-method prefix gotcha, because the pages read do not state them.
Method: documentation only; no commands were run.
