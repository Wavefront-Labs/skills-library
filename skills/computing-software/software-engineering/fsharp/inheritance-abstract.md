---
id: computing-software.software-engineering.fsharp.inheritance-abstract
name: inheritance-abstract
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, inheritance-abstract, fsharp-oop, abstract-classes, virtual-members]
level: practitioner
status: docs-checked
description: "Define abstract classes, default and override members and call base implementations in F#."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/inheritance
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/abstract-classes
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/pattern-matching
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Inheritance and abstract classes
**Goal:** use class inheritance sparingly but correctly.

```fsharp
[<AbstractClass>]
type Animal(name: string) =
    member _.Name = name
    abstract Speak : unit -> string
    abstract Legs : int
    default _.Legs = 4                       // virtual with a default

type Dog(name) =
    inherit Animal(name)
    override _.Speak() = "woof"

type Bird(name) =
    inherit Animal(name)
    override _.Speak() = "tweet"
    override _.Legs = 2

let a : Animal = Dog "rex" :> Animal
match a with :? Dog as dog -> dog.Name | _ -> ""
```
- A class has at most one direct base class, given with `inherit`.
- `abstract` declares a virtual member; add `default` for an implementation. A class with undefined abstract members is abstract.
- Use `[<AbstractClass>]` only when the class has undefined abstract members.
- `:>` upcasts; `:?` tests the type at run time.
- Consider an object expression for a minor modification, and a discriminated union instead of an object hierarchy.

## Gotchas
- A new virtual member is declared with `abstract`, whether or not a `default` implementation is given.

## Self-check
`(Bird "b" :> Animal).Legs` is 2 and `(Dog "d" :> Animal).Legs` is 4.

## Checked
2026-11-02. Confirmed against Learn "Inheritance" (one base class with inherit, abstract for virtual members, default and override, no default makes the class abstract), "Abstract Classes" (AbstractClass only for undefined abstract members), "Interfaces" (:> upcast) and "Pattern matching" (type test :?). Removed: the composition advice, the override-needs-declaration claim, the base.Method claim, the Sealed-by-default claim and the downcast exception and :?> claims (not on the pages read).
Method: documentation only; no commands were run.
