---
id: computing-software.software-engineering.csharp-dotnet.regex-source-generator
name: regex-source-generator
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-strings-text, regex-source-generator, generatedregex, regexoptions, regex-timeouts, redos, nonbacktracking]
level: practitioner
status: docs-checked
description: "Use [GeneratedRegex] (.NET 7+) for compile-time regexes, set match timeouts or RegexOptions.NonBacktracking against ReDoS, and avoid common Regex construction mistakes."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-source-generators", "https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex", "https://learn.microsoft.com/en-us/dotnet/standard/base-types/backtracking-in-regular-expressions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex source generator

## Use it
```csharp
public static partial class Patterns
{
    [GeneratedRegex(@"^(?<user>[^@\s]+)@(?<host>[^@\s]+)$", RegexOptions.CultureInvariant | RegexOptions.ExplicitCapture, matchTimeoutMilliseconds: 250)]
    public static partial Regex Email();
}
var m = Patterns.Email().Match(input);
if (m.Success) Console.WriteLine(m.Groups["user"].Value);
```
- .NET 7 introduced the generator. `[GeneratedRegex]` goes on a partial method returning `Regex`; from .NET 9 (C# 13 partial properties) it can go on a partial property.
- The generated code caches a singleton `Regex`, so no extra caching is needed. The emitted C# is part of your project: viewable and debuggable, with XML comments.
- `RegexOptions.Compiled` is ignored by the generator, so it is not needed.
- Page guidance: if you can use the generator, use it. Benefits listed: Compiled-level throughput, no runtime parse/compile at startup, ahead-of-time compilation friendliness, debuggability, smaller trimmed apps. Downside: extra code emitted into the assembly; for rarely used regexes the interpreter may suffice.
- Limits: `IgnoreCase` backreferences are not supported and `RegexOptions.NonBacktracking` is not supported by the generator; in both cases it falls back to caching a normal `Regex` instance (still with caching and comments).
- A .NET 7 analyzer and fixer convert existing `Regex` use to the generator.

## Safety (ReDoS)
- Nested optional quantifiers such as `^(a+)+$` make failed matches exponential, O(2^n) (the page shows a 27-char input failing in about 5 seconds).
- Set a match timeout (`TimeSpan` constructor argument, static-method overload, or the attribute argument); `RegexMatchTimeoutException` is thrown on expiry and does not say why. Default is `Regex.InfiniteMatchTimeout`. The best-practices page recommends always setting one when not using NonBacktracking and the regex backtracks or sees untrusted input.
- `RegexOptions.NonBacktracking` runs in time proportional to input length but cannot be combined with constructs that need backtracking (lookarounds, backreferences, atomic groups).
- Other mitigations in the docs: atomic groups, lookahead/lookbehind to replace nested quantifiers, rejecting over-long input before matching.
- The engine does not protect against untrusted patterns: do not build patterns from user input; use `Regex.Escape` for user text used as a literal.

## Other mistakes
- Static `Regex` methods cache the 15 most recently used patterns by default (`Regex.CacheSize` adjusts it); otherwise store a `Regex` in a field instead of constructing repeatedly.
- Use `IsMatch` / `Count` / `EnumerateMatches` when you need less than a full `Match`; use `ExplicitCapture` or non-capturing groups to avoid needless captures.
- Diagnostics: the analyzer docs live under SYSLIB1040-1049.

## Verify
Unit-test valid, invalid and adversarial inputs (a long run of `a` then `!`); assert completion within the timeout or a controlled `RegexMatchTimeoutException`.

## Checked
Method: 2026-11-08 docs-only read of the source-generators and backtracking pages (full) and the best-practices page (searched for cache, untrusted input and escaping). Removed or demoted unsupported claims: the exact `matchTimeoutMilliseconds` named-argument form is from the attribute API, not the pages; removed the CultureInvariant/Turkish-i, `$` vs `\z`, `\p{L}`, nested-class and `Regex.Replace` notes, and the "property form needs .NET 8" claim (pages say .NET 9).
