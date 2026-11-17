---
id: computing-software.software-engineering.refactoring.encapsulate-global-references
name: encapsulate-global-references
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, legacy-code, encapsulate-global-references, global-data, static-dependencies, singletons]
level: advanced
status: draft
description: "Break static and global dependencies in legacy code: encapsulate global references in a class, replace global function calls with instance calls, and introduce static setters."
sources: ["https://www.oreilly.com/library/view/working-effectively-with/0131177052/", "https://refactoring.com/catalog/encapsulateVariable.html", "https://martinfowler.com/bliki/LegacySeam.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Breaking static and global dependencies

Global variables, static methods and singletons create hidden coupling: tests can't substitute
them and state leaks between tests. Feathers' techniques, from least to most invasive:

## Encapsulate Global References
Globals used together (C/C++ globals, static fields) become members of a class:
1. Create a class holding the related globals as fields (or with getters wrapping them initially).
2. Create one global instance of the class.
3. Replace each reference `AVAILABLE_ACCOUNTS` with `globals.availableAccounts` (compile, test).
4. Now code can be changed to receive the object (parameter, constructor) and tests can create their
   own instance.

## Replace Global Reference with Getter
Add a virtual getter `protected Config getConfig() { return Config.INSTANCE; }` and replace
direct uses, then override in a testing subclass.

## Static methods: Introduce Instance Delegator
```java
class BankingServices {
    public static void updateAccountBalance(int id, Money m) { ... }
    public void updateBalance(int id, Money m) { updateAccountBalance(id, m); }   // new instance delegator
}
```
Callers switch to an injected `BankingServices` instance; tests pass a subclass/fake. Eventually move
the logic into the instance method and delete the static.

## Wrap static library calls
`File.ReadAllText`, `DateTime.Now`, `System.currentTimeMillis()`: introduce a small interface/
wrapper (`IFileSystem`, `Clock`) and inject it. In .NET, `TimeProvider` (8.0+) and
System.IO.Abstractions exist; Java has `java.time.Clock`.

## Introduce Static Setter (singletons)
Allow tests to replace the singleton instance (`setTestingInstance`) and reset after each test.
Make the constructor protected so a fake subclass can be created.

## Link and preprocessing seams (C/C++)
Link against a test object file providing fake versions of global functions; or `#define` swaps in
test builds. Powerful but obscure; document it.

## Afterwards
Test for order dependence (`pytest -p randomly`, JUnit random method order) to catch remaining
shared state.
