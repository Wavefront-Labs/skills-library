---
id: computing-software.software-engineering.csharp-dotnet.virtual-override-new-and-sealed
name: virtual-override-new-and-sealed
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-oop, virtual, override, method-hiding, sealed, polymorphism]
level: practitioner
status: docs-checked
description: "How C# virtual, override, new and sealed differ: runtime dispatch versus compile-time hiding, what can be overridden, sealed overrides, covariant returns and calling base."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/polymorphism", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/override", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/new-modifier", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/sealed"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# virtual, override, new, sealed

```csharp
class Shape {
    public virtual string Name() => "shape";
    public string Describe() => $"I am {Name()}";
}
class Circle : Shape {
    public override string Name() => "circle";          // participates in virtual dispatch
}
class Hidden : Shape {
    public new string Name() => "hidden";               // hides; no dispatch
}

Shape a = new Circle(); a.Name();  // "circle": the run-time type decides
Shape b = new Hidden(); b.Name();  // "shape": the compile-time type decides
((Hidden)b).Name();                // "hidden"
b.Describe();                      // "I am shape"
```

## Rules
- A derived class can override a base member only if the base member is `virtual`, `abstract` or itself `override`; you cannot override a non-virtual or static method. The derived member must use `override`.
- Only methods, properties, events and indexers can be virtual, not fields.
- An override has the same signature as the base method. Overrides support covariant return types: the return type may derive from the base method's return type. An overriding property must use exactly the same access modifier, type and name.
- `new` hides a base member: the member called depends on the compile-time type of the variable. Using `new` on a declaration that hides nothing produces a warning, and omitting it when hiding also warns.
- Virtual members stay virtual through the chain: a class two levels down can still override even if the middle class did not. `sealed override` stops further overriding: the method is still virtual for instances of that class (even when cast to a base type) but no longer virtual for classes derived from it; a derived class can replace it with `new`.
- A sealed class cannot be inherited and cannot be `abstract`.
- Microsoft recommends that overrides call `base.Method()` so the base behaviour still happens; if you do not call it, make your behaviour compatible with the base.

## Verify
A test using a base-typed reference to assert override behaviour, and a build that treats the hiding warning as an error to catch accidental hiding.

## Checked
2026-11-03. Confirmed against dotnet/docs: polymorphism article (virtual, override, new, sealed override, base), the `override`, `new` modifier and `sealed` keyword pages. Removed because not found there: warning and analyzer numbers (CS0108, CS0659, CA1033, CA1061), JIT devirtualisation claims, "calling virtual methods from constructors" advice, Liskov remarks, interface re-implementation notes, and the `new virtual` comment.
Method: documentation only; no commands were run.
