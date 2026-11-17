---
id: computing-software.software-engineering.csharp-dotnet.operator-overloading-and-conversions
name: operator-overloading-and-conversions
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-oop, operator-overloading, implicit-explicit-conversion, checked-operators, ca2225]
level: practitioner
status: docs-checked
description: "Overload C# operators and define implicit and explicit conversions: declaration rules, paired comparison operators, non-overloadable operators, checked and C# 14 compound forms."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/operator-overloading", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/user-defined-conversion-operators", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/arithmetic-operators", "https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2225"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator overloading and conversions

```csharp
public readonly record struct Money(decimal Amount, string Currency)
{
    public static Money operator +(Money a, Money b) =>
        a.Currency == b.Currency ? new(a.Amount + b.Amount, a.Currency)
                                 : throw new InvalidOperationException("Currency mismatch");
    public static Money operator -(Money a) => a with { Amount = -a.Amount };
    public static bool operator >(Money a, Money b) => Compare(a, b) > 0;      // pair with <
    public static bool operator <(Money a, Money b) => Compare(a, b) < 0;
    private static int Compare(Money a, Money b) => a.Currency == b.Currency
        ? a.Amount.CompareTo(b.Amount) : throw new InvalidOperationException();
}

public readonly struct Meters
{
    public double Value { get; }
    public Meters(double v) => Value = v;
    public static implicit operator double(Meters m) => m.Value;       // cannot throw or lose information
    public static explicit operator Meters(double d) => new(d);        // explicit
}
```

## Declaration rules
- An operator declaration is `public` and `static` (compound assignment operators are the exception: instance, no `static`).
- At least one parameter must have type `T` or `T?`, where `T` is the type that contains the declaration.
- Comparison operators are overloaded in pairs: `==` with `!=`, `<` with `>`, `<=` with `>=`. `true` and `false` are overloaded together.
- Overloading a binary operator (before C# 14) implicitly provides the matching compound assignment (`+=`).
- Cannot be overloaded: `&&` and `||` (overload `true`/`false` plus `&` or `|`), the indexer `a[i]` (define an indexer), the cast `(T)x` (define a conversion), and others such as `=`, `?.`, `??`, `new`, `is`, `as`, `typeof`.
- C# 14: compound assignment operators (`+=` and so on) can be overloaded as `public` instance members with return type `void` and one parameter for the right-hand side; `++`/`--` may be instance members that are `void` with no parameters. Instance operators can avoid creating a new instance. When `x` is a variable, the instance operator is preferred over a static one.
- A user-defined `checked` operator requires also defining the operator without `checked`; checked contexts call the checked one, which throws `OverflowException` on overflow.

## Conversions
Predefined implicit conversions always succeed and never throw; user-defined implicit conversions should behave the same way. If a conversion can throw or lose information, make it explicit. The type defining a conversion must be its source or target type. `is` and `as` do not consider user-defined conversions; use a cast to invoke a user-defined explicit one.

## Rules of thumb
1. Provide named alternates (`Add`) for operator overloads; analyzer CA2225 checks for them.
2. Keep equality, `Equals` and `GetHashCode` consistent (record structs generate value equality for you).
3. Implicit conversions between unrelated domain types erode type safety; prefer explicit.

## Verify
Tests for currency mismatch throwing, symmetric comparison, and an explicit conversion round trip.

## Checked
2026-11-03. Confirmed against dotnet/docs: operator overloading page (rules, pairs, non-overloadable table, C# 14 instance operators), user-defined conversion operators page, arithmetic operators (checked operators) and the CA2225 page title. Removed because not found: the claim that checked operators are C# 11 (no version stated in the page text read), "`++` must return the new value", the `x is null` versus overloaded `==` remark, interface operator and boxing remarks.
Method: documentation only; no commands were run.
