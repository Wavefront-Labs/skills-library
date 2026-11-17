---
id: computing-software.software-engineering.objective-c.message-syntax
name: message-syntax
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-messaging, message-syntax]
level: intro
status: docs-checked
description: "Read and write Objective-C message expressions, keyword method names, nested sends and class messages."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocObjectsClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message syntax
**Goal:** read `[receiver message]` fluently.

```objc
[myRectangle display];                          // no parameters
[myRectangle setWidth:20.0];                    // one parameter: colon then value
[myRectangle setOriginX: 30.0 y: 50.0];         // interleaved name parts
BOOL isFilled = [myRectangle isFilled];         // returns a value
[myRectangle setPrimaryColor:[otherRect primaryColor]];   // nested send
```
- Message expressions are enclosed in brackets: `[receiver message]`. The method name in a message is often called a selector.
- A selector name includes all parts of the name including the colons: `setOriginX:y:` has two colons because it takes two parameters. It does not include return or parameter types.
- The subparts of a selector name are not optional and their order cannot vary; Objective-C parameters are not keyword or named parameters in the Python sense.
- `[myRectangle setOrigin:30.0 :50.0]` (method `setOrigin::`) is syntactically legal but the second parameter is effectively unlabeled, so it is a bad style.
- A variable number of parameters is possible but rare; extra parameters follow the method name, separated by commas that are not part of the name: `[receiver makeGroup:group, memberOne, memberTwo, memberThree];`.
- A variable and a method can have the same name.
- One message expression can be nested inside another.
- The dot operator is a compact syntax for accessor methods, usually with declared properties.

## Self-check
For each message expression in a file, write down its full selector including colons and count the arguments.

## Checked
2026-11-08. Confirmed against the archived "Objective-C Programming Language" chapter on objects, classes and messaging (Message Syntax): bracket syntax, selector naming, interleaved parameters, unlabeled-parameter warning, variadic form, nesting, dot syntax. Removed: method declaration syntax, `super` lookup, `NS_REQUIRES_NIL_TERMINATION`, `void *` receiver error, compiler warning flags and class-message example with `stringWithFormat:` (not on the page). Page is marked a retired document.
Method: documentation only; no commands were run.
