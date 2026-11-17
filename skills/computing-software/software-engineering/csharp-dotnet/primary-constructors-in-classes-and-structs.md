---
id: computing-software.software-engineering.csharp-dotnet.primary-constructors-in-classes-and-structs
name: primary-constructors-in-classes-and-structs
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-oop, primary-constructors, csharp-12, dependency-injection, captured-parameters]
level: practitioner
status: docs-checked
description: "Use C# 12 primary constructors on classes and structs: parameter scope, capture into hidden fields, not properties, validation, chaining other constructors and base calls."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/tutorials/primary-constructors", "https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/instance-constructors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Primary constructors (C# 12)

```csharp
public class OrderService(IOrderRepository repo, IClock clock)
{
    public Order Place(NewOrder n)
    {
        var order = new Order(n, clock.Now());
        repo.Add(order);
        return order;
    }
}
```
Parameters in parentheses after the type name are in scope for the whole body of the class or struct. They can initialise fields or properties, be used in methods and local functions, and be passed to a base constructor.

## Semantics
- They are parameters, not members: `this.param` does not compile, they can be assigned to (so they are not read-only), and they do not become properties. Only `record` types get a synthesised public property per parameter.
- Storage: if a parameter is only used in initialisers and constructor calls it is not captured. A use in any other member makes the compiler capture it in a hidden private field (one per such parameter).
- To get an immutable member, copy it: `private readonly IOrderRepository _repo = repo;` or expose `public string Name { get; } = name;`.
- Validate when assigning: `private readonly string _name = name ?? throw new ArgumentNullException(nameof(name));`.
- Every other constructor of the type must call the primary constructor, directly or indirectly, with `this(...)`. A parameterless constructor on a struct must do the same.
- Base class: pass arguments up with `class Child(int id) : Base(id)`.
- Attributes can target the synthesised constructor with the `method:` target.

## Verify
A unit test asserts that the null guard throws on construction and that other constructors reach the primary one.

## Checked
2026-11-03. Confirmed against dotnet/docs: the primary constructors tutorial and the instance constructors article. Removed because not found there: compiler warning and analyzer codes (CS9113, CS9124, IDE0290), the claim that structs keep an implicit `new()`, serializer and ORM binding remarks, and size advice for captured large structs.
Method: documentation only; no commands were run.
