---
id: computing-software.software-engineering.csharp-dotnet.pattern-matching-and-switch-expressions
name: pattern-matching-and-switch-expressions
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, csharp-pattern-matching, switch-expressions, property-patterns, list-patterns, relational-patterns, exhaustiveness, discriminated-unions, csharp-pattern-matching-records]
level: practitioner
status: docs-checked
description: "Write clear C# with switch expressions and patterns: type, property, relational, logical and list patterns, exhaustiveness warnings and closed hierarchies."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/patterns", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/functional/pattern-matching"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Pattern matching and switch expressions

**Goal:** replace nested if/else and type-check-then-cast chains with declarative,
compiler-checked matching.

## Pattern kinds
```csharp
decimal Fee(Order o) => o switch
{
    { Total: <= 0 }                              => throw new ArgumentException("empty"),
    { Customer.Tier: Tier.Gold }                 => 0m,                 // extended property pattern
    { Total: >= 100 and < 500, Express: false }  => 2.50m,              // relational + logical
    { Express: true }                            => 9.99m,
    _                                            => 4.99m,
};

string Describe(object x) => x switch
{
    null                => "null",
    int n when n < 0    => "negative",
    int                 => "int",
    string { Length: 0 } => "empty string",
    IEnumerable<int> e  => $"{e.Count()} ints",
    _                   => x.GetType().Name,
};

// list patterns (C# 11)
var cmd = args switch
{
    []                    => Help(),
    ["add", var name]     => Add(name),
    ["rm", .. var names]  => Remove(names),
    _                     => Unknown(),
};
```
`is` patterns in conditions: `if (shape is Circle { Radius: > 10 } c) ...`,
`if (value is not null)`.

## Exhaustiveness
- A switch expression without a matching arm throws `SwitchExpressionException` at
  runtime; the compiler warns CS8509 when it can see a gap. Treat CS8509 as an error.
- For enums the compiler cannot prove exhaustiveness (any int is a valid enum value),
  so you need `_` anyway; throw `UnreachableException` (NET 7+) there.
- The compiler cannot prove exhaustiveness over an open class hierarchy: add a discard arm that throws.
- List patterns do not produce the CS8509 warning when inputs are unhandled, so add a discard arm
  yourself.

## Ordering
Arms evaluate top to bottom; the compiler errors on an arm made unreachable by an
earlier one, which catches many mistakes.

## Style
- Keep arms to one expression; call a method for complex logic.
- Prefer property patterns over `when` clauses when possible: they participate in
  subsumption analysis.

## Checked
2026-10-28: Confirmed in the patterns reference and switch expression page: property, relational, logical and list patterns; CS8509 for unhandled values and the note that list patterns do not warn; SwitchExpressionException. Replaced the claim that C# has no closed hierarchies (the docs now mention union types) with a statement about open hierarchies; removed the CS8510 code.
Method: documentation only; no commands were run.

## Verify
- [ ] CS8509 treated as an error in the project (`<WarningsAsErrors>CS8509</WarningsAsErrors>`).
- [ ] Tests cover each arm including the discard.
