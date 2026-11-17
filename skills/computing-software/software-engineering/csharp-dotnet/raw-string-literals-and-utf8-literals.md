---
id: computing-software.software-engineering.csharp-dotnet.raw-string-literals-and-utf8-literals
name: raw-string-literals-and-utf8-literals
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-strings-text, raw-string-literals, utf8-literals, interpolation, json]
level: practitioner
status: docs-checked
description: "Write C# raw string literals (triple quotes, indentation rules, multi-dollar interpolation) and u8 UTF-8 literals (ReadOnlySpan<byte>, limits with interpolation)."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/tokens/raw-string", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/tokens/interpolated", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/reference-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw string literals and UTF-8 literals

## Raw strings
```csharp
string json = """
    {
      "name": "Ada",
      "quote": "She said "hi" without escaping"
    }
    """;
```
Delimited by three or more `"`; inside, every character is literal (quotes and backslashes need no escaping, newlines are kept as written). Good for JSON, XML, SQL, regular expressions and code samples.

Multi-line rules:
- The opening quotes are the last non-whitespace on their line and the closing quotes the first non-whitespace on theirs.
- Whitespace to the left of the closing quotes is removed from every content line. Spaces and tabs are not interchangeable: the same exact whitespace must start each content line, so do not mix tabs and spaces in one literal.
- Whitespace after the opening quotes on the same line is ignored; whitespace-only lines after the opening quotes are included in the string.
- The newline right after the opening quotes and the one before the closing quotes are not part of the value.
- If the content contains `"""`, delimit with four (or more) quotes. The content must not contain a run of quotes as long as the delimiter. To start or end the value with a quote, use the multi-line form.

Interpolation: start with multiple `$` characters and braces shorter than that count are literal; interpolation expressions then need the same number of braces as `$` characters:
```csharp
var body = $$"""
    { "id": {{id}}, "tags": [ "{{tag}}" ] }
    """;
```

## UTF-8 literals
```csharp
ReadOnlySpan<byte> auth = "AUTH "u8;
byte[] arr = "AUTH "u8.ToArray();
```
- The `u8` suffix makes the compiler store the literal as a `ReadOnlySpan<byte>`; .NET strings are UTF-16, while UTF-8 is the standard for web protocols.
- They are runtime constants, not compile-time constants, so they cannot be the default of an optional parameter.
- You cannot combine `$` interpolation with `u8`. The `+` operator concatenates two UTF-8 literals (as `ReadOnlySpan<byte>`).

## Verify
Test that the raw literal deserialises as expected and that its indentation was stripped as intended; for content that contains dynamic values, serialise with a JSON library rather than splicing text.

## Checked
2026-11-03. Confirmed against dotnet/docs: raw string literal reference and fundamentals page, interpolated string reference (multiple `$`), reference types page (u8 literals) and the addition operator page. Removed because not found: compiler error numbers, `$$$` details, `StringSyntax` attribute advice, line-ending normalisation advice, `Utf8JsonReader.ValueTextEquals` usage, "null-terminated static data" claim, and the claim that whitespace-only lines are exempt from the indentation rule (the reference says whitespace-only lines after the opening quotes are included). The sample above removes the original's escaped quotes, which are unnecessary in a raw string.
Method: documentation only; no commands were run.
