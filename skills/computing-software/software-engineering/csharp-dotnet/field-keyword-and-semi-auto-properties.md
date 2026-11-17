---
id: computing-software.software-engineering.csharp-dotnet.field-keyword-and-semi-auto-properties
name: field-keyword-and-semi-auto-properties
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-properties, field-keyword, auto-properties, csharp-14, lazy-initialization]
level: practitioner
status: docs-checked
description: "Use the C# 14 field keyword to write one property accessor body over the compiler-generated backing field, with null checks, trimming, lazy init and the field identifier clash."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/field", "https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# field keyword (C# 14) and semi-auto properties

`field`, introduced in C# 14 (which ships with .NET 10), is a contextual keyword inside a property accessor that stands for the compiler-synthesized backing field. You write the body of one or both accessors and the compiler generates the other as in an automatically implemented property. It gives a smooth path to add range checking or null checks to an auto property without declaring a backing field by hand.

```csharp
public string Name
{
    get;
    set => field = value ?? throw new ArgumentNullException(nameof(value));
}

public SqlConnection Connection { get => field ??= new SqlConnection("connection-string"); }   // lazy init

public string Slug
{
    get;
    set => field = value?.Trim()?.ToLowerInvariant() ?? string.Empty;
}
```
Microsoft's C# 14 page shows these patterns: null rejection, lazy initialisation with `field ??=`, change-notification checks (`if (field == value) return;`) and normalising a string in the setter.

## Requirements
- Needs C# 14: the latest Visual Studio 2026 or the .NET 10 SDK (C# 14 is supported on .NET 10). Libraries built with older SDKs or language versions cannot use it.

## Trap
- If a type already has a symbol named `field`, reading the code becomes confusing and the change can be breaking. Disambiguate with `@field` or `this.field`, or rename the existing symbol.

## Verify
Build with a .NET 10 SDK and add unit tests for the null rejection and the normalisation your setter performs. Note that a setter that normalises (for example trimming) means the value read back can differ from the value assigned; document it.

## Checked
2026-11-03. Confirmed against dotnet/docs: "The field contextual keyword" and "What's new in C# 14" (definition, examples, version, `@field` / `this.field`). Removed because not found in the pages read: `required`/`init` notes, warning CS9258, atomicity of `field ??=`, serialiser and EF Core binding remarks, preview history, the `-warnaserror` verification step.
Method: documentation only; no commands were run.
