---
id: computing-software.software-engineering.refactoring.replace-constructor-with-factory-function
name: replace-constructor-with-factory-function
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-apis, replace-constructor-with-factory, factory-function, named-constructors, static-factory, fowler-catalog]
level: practitioner
status: docs-checked
description: "Replace Constructor with Factory Function to get descriptive names, subclass or cached returns, and a place for creation logic that a constructor cannot hold."
sources:
  - https://refactoring.guru/replace-constructor-with-factory-method
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Constructor with Factory Function

## Why constructors are limiting
- A constructor always creates a new instance of exactly its own class: it cannot return a subclass or an already created object.
- The name is fixed to the class; `new Employee(name, "E")` does not say what "E" means.
- Creation modes that go beyond the number and types of parameters have nowhere to live.

## Before / after
```javascript
const leadEngineer = new Employee(document.leadEngineer, "E");
// after
function createEngineer(name) { return new Employee(name, "E"); }
const leadEngineer = createEngineer(document.leadEngineer);
```

## Mechanics
1. Create a factory function and place a call to the current constructor in it.
2. Replace every constructor call with a call to the factory; test as you go.
3. Declare the constructor private (or otherwise restrict it) so new code goes through the factory.
4. Look at the constructor body: code not directly about constructing this class belongs in the factory.

## Things factories enable
- Return a subclass chosen from the arguments, which is the usual follow-on to Replace Type Code with Subclasses.
- Return an already created object instead of a new one, which is useful when changing a value to a reference.
- Give creation a name that says what it builds and how.

## Verify
- [ ] Searching for `new Employee(` outside the factory returns nothing; constructor visibility reduced.

## Checked
2026-11-01. Confirmed against the Refactoring Guru page "Replace Constructor with Factory Method": the problem and solution wording, the three benefits (subclass return, better name, return existing object), the link to Replace Type Code with Subclasses and Change Value to Reference, and the four how-to-refactor steps.
Removed: the language-library examples (Java, Python, Rust factories), the async-creation, Result-returning validation and caching claims, the naming-convention list and the serialiser note, because no page read states them.
Method: documentation only; no commands were run.
