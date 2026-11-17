---
id: computing-software.software-engineering.csharp-dotnet.default-interface-members-and-static-abstracts
name: default-interface-members-and-static-abstracts
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-oop, default-interface-members, static-abstract-members, generic-math, interface-evolution, diamond-problem]
level: advanced
status: docs-checked
description: "Evolve C# interfaces with default implementations and use static abstract or static virtual interface members for generic math; interface-typed calls, diamond conflict CS8705."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interface-implementation/default-interface-methods-versions", "https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interface-implementation/static-virtual-interface-members", "https://learn.microsoft.com/en-us/dotnet/standard/generics/math", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/interface-implementation-errors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default interface members and static abstracts

## Default implementations
An interface member can carry a body. The main use is adding members to an interface that has already shipped without breaking implementers, who may accept the default or override it.
```csharp
public interface ILogger2 {
    void Log(string msg);
    void LogError(string msg) => Log("ERROR: " + msg);
}
class Console2 : ILogger2 { public void Log(string m) => Console.WriteLine(m); }

ILogger2 l = new Console2();
l.LogError("x");                 // OK: variable has the interface type
```
- A class does not inherit members from its interfaces. To call a member implemented in the interface, the variable must have the interface type (`new Console2().LogError(...)` does not compile).
- Interfaces can also hold static members (fields and methods) with access modifiers, so a default implementation can be parameterised through a static setter or shared through a `protected static` helper that overriding implementations call.
- Diamond: if two interfaces give a default for the same member and the class implements both, the compiler reports CS8705 (no most specific implementation). Provide an explicit implementation in the class, or restructure the interfaces.
- Design interfaces to express one functional idea so they are easy to upgrade later.

## Static abstract and static virtual members
`static abstract` members have no body and each implementing type must supply one; `static virtual` members have a default body that implementers may override. They are called through a type parameter in a generic method, resolved at compile time.
```csharp
static T MidPoint<T>(T left, T right) where T : INumber<T>
    => (left + right) / T.CreateChecked(2);
```
- `INumber<T>` requires `operator +` and `operator /`; `T.CreateChecked(2)` builds the constant in type `T` and throws `OverflowException` when the value is not representable.
- Generic math is built on interfaces in the .NET 7 base class library, such as `IAdditionOperators<TSelf, TOther, TResult>` (left operand, right operand, result) and `IAdditiveIdentity<TSelf, TResult>` (`T.AdditiveIdentity` gives the zero of `T`). Constrain with the narrowest interface your algorithm needs, for example `where T : IAdditionOperators<T, T, T>`.
- Use `static abstract` when every type must provide its own implementation and `static virtual` when a sensible default exists.

## Verify
Compile `MidPoint` with `int`, `double` and `decimal`; test that a class overriding a default member takes precedence when called through the interface.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Update interfaces with default interface methods" tutorial, "Explore static virtual members in interfaces" tutorial, the interface implementation errors page (CS8705 diamond) and the generic math page (INumber). Removed because not found in the pages read: version numbers for C# and .NET gates, the claim about .NET Framework runtime support, JIT size, DI and mocking caveats, the `IParsable` and `ISpanParsable` list and the self-referencing constraint requirement.
Method: documentation only; no commands were run.
