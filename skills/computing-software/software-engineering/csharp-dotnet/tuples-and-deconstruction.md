---
id: computing-software.software-engineering.csharp-dotnet.tuples-and-deconstruction
name: tuples-and-deconstruction
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-type-system, tuples, deconstruction, valuetuple, pattern-matching, discards]
level: practitioner
status: docs-checked
description: "Use C# tuples and deconstruction: value tuple semantics, compile-time-only field names, ==, deconstructing into variables, discards, Deconstruct methods, tuple patterns."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-tuples", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/patterns/deconstruct"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuples and deconstruction

```csharp
(int Min, int Max) Range(IEnumerable<int> xs) => (xs.Min(), xs.Max());

var (lo, hi) = Range(data);                 // deconstruct into new locals
(int a, int b) = (1, 2); (a, b) = (b, a);   // swap without a temp
var (_, max) = Range(data);                 // discard
var point = (X: 3, Y: 4);
Console.WriteLine(point.X);

// your own type: a Deconstruct method with out parameters
public class Customer { public string Name = ""; public int Age;
    public void Deconstruct(out string name, out int age) => (name, age) = (Name, Age); }

// positional records get Deconstruct automatically
public readonly record struct Money(decimal Amount, string Currency);

// tuple pattern
string Classify(bool ready, bool paid) => (ready, paid) switch {
    (true, true)  => "ship",
    (true, false) => "invoice",
    (false, _)    => "wait"
};
```

## Facts
- Tuples group loosely related data in a lightweight structure. They are value types whose elements are public fields, which makes them mutable value types.
- Default element names are `Item1`, `Item2`, and so on, always usable. Explicit or inferred names are replaced by the default names at compile time, so they are not available at run time; assignment and equality ignore names (only types and arity must match).
- `==` and `!=` compare elements in order, short-circuit on the first unequal pair, and need the same number of elements, each pair comparable with `==`. All elements are evaluated before any comparison.
- Deconstruction can target new variables (`var (a, b)` or explicit types), existing variables, or a mix, and discards `_` mark values you do not need; every produced value must line up with a position on the left.
- A class, struct or interface supports deconstruction by declaring a `Deconstruct` method returning `void` with one `out` parameter per component; overloads with different numbers of `out` parameters are allowed. Positional `record` and `record struct` types get one generated for their positional parameters only. For a type you do not own, write an extension `Deconstruct` method.
- In public APIs, Microsoft advises defining a class or struct rather than returning a tuple.

## Verify
Tests that `Range` returns the named values, that the swap works and that the `Classify` switch covers every case.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Tuple types" (value type, mutable fields, names, equality) and "Deconstruct" (forms, discards, Deconstruct methods, records, extension methods). Removed because not found there: `Dictionary<(string,int),V>` key advice, System.Text.Json and reflection behaviour for tuples, `System.Tuple` legacy remarks, boxing cost, nullable per-element annotations, and the C# 7.3 equality version note.
Method: documentation only; no commands were run.
