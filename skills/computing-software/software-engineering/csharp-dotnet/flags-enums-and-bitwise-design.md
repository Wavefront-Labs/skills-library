---
id: computing-software.software-engineering.csharp-dotnet.flags-enums-and-bitwise-design
name: flags-enums-and-bitwise-design
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-type-system, flags-enum, bitwise, enum, validation]
level: practitioner
status: docs-checked
description: "Design C# flags enums: Flags attribute, power-of-two members, a zero None member, named combinations, bitwise set/clear/test, and validating untrusted numeric values."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flags enums

To represent a combination of choices, define each choice as a bit field (associated values that are powers of two), apply the `Flags` attribute, and combine with `|` or intersect with `&`. You can also include typical combinations as members.

```csharp
[Flags]
public enum Permissions : uint
{
    None   = 0,
    Read   = 1 << 0,
    Write  = 1 << 1,
    Delete = 1 << 2,
    Admin  = 1 << 3,
    ReadWrite = Read | Write,
    All = Read | Write | Delete | Admin
}

var p = Permissions.Read | Permissions.Write;
p |= Permissions.Delete;                      // set
p &= ~Permissions.Write;                      // clear
bool canRead = (p & Permissions.Read) != 0;   // test one flag
bool both = (p & Permissions.ReadWrite) == Permissions.ReadWrite;
p ^= Permissions.Admin;                       // toggle
```

## Design rules
1. Members are powers of two (`1 << n`), not `1, 2, 3`.
2. Define a member with value zero (`None`). The default value of an enum `E` is `(E)0` even when no member has that value, and the literal `0` converts implicitly to any enum type.
3. You can choose any integral underlying type (default `int`); pick one wide enough for the number of flags.
4. Apply `[Flags]`; Microsoft's enum page links to `System.FlagsAttribute` for further guidance on non-exclusive members.

## Untrusted input
Casting a number gives an enum value even if no member matches, and implicit conversion from `0` can produce an undefined value. Microsoft advises validating values converted from numeric types and notes `Enum.IsDefined` determines whether a type contains a member with a given value. For a flags enum, validate combinations with a mask:
```csharp
static bool IsValid(Permissions p) => ((uint)p & ~(uint)Permissions.All) == 0;
```

## Verify
Unit tests for set, clear and toggle round trips, and that `IsValid((Permissions)(1 << 10))` is false.

## Checked
2026-11-03. Confirmed against the dotnet/docs enumeration types page (bit flags, powers of two, `Flags`, default value, zero conversion, IsDefined, underlying types). Removed because not found in the pages read: HasFlag runtime-version performance notes, `Enum.TryParse` comma behaviour, `ToString` output for undefined bits, System.Text.Json and EF Core behaviour, `switch` matching remark, naming and renumbering guidance.
Method: documentation only; no commands were run.
