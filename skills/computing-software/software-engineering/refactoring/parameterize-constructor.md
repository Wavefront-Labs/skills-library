---
id: computing-software.software-engineering.refactoring.parameterize-constructor
name: parameterize-constructor
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, legacy-code, parameterize-constructor, introduce-instance-setter, dependency-injection, seams]
level: practitioner
status: draft
description: "Break hidden constructor dependencies with Parameterize Constructor (keeping a delegating default constructor) or Supersede Instance Variable, then inject fakes in tests."
sources: ["https://www.oreilly.com/library/view/working-effectively-with/0131177052/", "https://martinfowler.com/articles/injection.html", "https://refactoring.com/catalog/changeFunctionDeclaration.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parameterize constructor and introduce instance setter

## Parameterize Constructor (Feathers)
A constructor creates a collaborator internally, so tests can't replace it:
```csharp
public class MailChecker {
    private readonly MailReceiver receiver;
    public MailChecker(int checkPeriod) { receiver = new MailReceiver(); ... }
}
```
Steps:
1. Copy the constructor; add a parameter for the collaborator in the copy.
2. Make the copy assign the parameter instead of `new`.
3. Make the original constructor delegate: `public MailChecker(int p) : this(new MailReceiver(), p) {}`.
4. Tests call the new constructor with a fake (extract an interface if the class can't be faked).
Existing callers are untouched; later you can migrate them and delete the default constructor.

Python: add an optional keyword argument with default `None` -> create the real one if not given.
Java: overloaded constructor; C++: default arguments or overload.

## Introduce Instance Setter / Supersede Instance Variable
When adding a constructor parameter is awkward (many constructors, C++ initialisation order):
- Add a method `supersedeReceiver(MailReceiver r)` (Feathers' naming makes test-only intent obvious)
  that replaces the field after construction; tests call it.
- Clean up the old object if needed (C++ ownership).
- Only acceptable when construction of the real collaborator has no unwanted side effects; if
  creating it connects to a server, use Extract and Override Factory Method instead.

## Introduce Static Setter
For singletons accessed globally: add `static void setTestingInstance(Config c)` and reset it in
test teardown. Use as a temporary step towards injecting the instance.

## Follow-through
These leave the default wiring in place. Once tests exist, move construction to a composition
root and remove default constructors and supersede methods so dependencies are explicit.
