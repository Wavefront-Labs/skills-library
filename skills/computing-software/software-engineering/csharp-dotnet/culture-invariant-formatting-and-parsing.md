---
id: computing-software.software-engineering.csharp-dotnet.culture-invariant-formatting-and-parsing
name: culture-invariant-formatting-and-parsing
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-strings-text, culture-invariant, cultureinfo, tryparse, string-comparison, turkish-i-problem, ca1304]
level: practitioner
status: docs-checked
description: "Avoid .NET culture bugs: invariant culture for persisted data, ordinal comparison, the Turkish-I problem, invariant globalization mode, ICU load failures, CA13xx rules."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings", "https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-display-data", "https://learn.microsoft.com/en-us/dotnet/core/extensions/globalization-icu", "https://learn.microsoft.com/en-us/dotnet/core/runtime-config/globalization", "https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1307"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Culture-invariant formatting and parsing

Formatting, parsing and many string operations use the current culture unless you pass one. Data that leaves the process in string form must not depend on the machine's culture.

## Rules
1. **Persisted data** (files, protocols, keys, stored text): format and parse with `CultureInfo.InvariantCulture`. Microsoft: do not use culture-sensitive formatting to persist numeric or date-and-time data in string form.
```csharp
string s = price.ToString(CultureInfo.InvariantCulture);
bool ok = decimal.TryParse(text, NumberStyles.Number, CultureInfo.InvariantCulture, out var d);
```
2. **UI display**: use culture-sensitive formatting for numbers and dates shown to the user, and `CurrentCulture` string operations for output shown to the user.
3. **Comparison**: use overloads that take `StringComparison`. `Ordinal` or `OrdinalIgnoreCase` is the safe default for culture-agnostic matching (identifiers, paths, headers) and is faster. Avoid `InvariantCulture` string operations except for linguistically meaningful but culturally agnostic persisted data.
4. When normalising strings for comparison, Microsoft recommends `ToUpperInvariant` over `ToLowerInvariant`.
5. Use `Equals` overloads for equality; use `Compare`/`CompareTo` to sort, not to test for equality by checking for zero.
6. The Turkish-I problem is the canonical case of culture-dependent casing: under a Turkish culture, case-insensitive checks such as a "file:" URI test can return a different answer than under U.S. English, which can bypass security checks. Use ordinal or invariant operations for non-linguistic data.

## Globalization invariant mode and ICU
- Invariant mode runs without culture data. Set `System.Globalization.Invariant` in runtimeconfig.json, the `InvariantGlobalization` MSBuild property, or the environment variable `DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1`.
- In invariant mode, .NET (6 and later) by default restricts creating cultures other than the invariant culture (`PredefinedCulturesOnly`, env `DOTNET_SYSTEM_GLOBALIZATION_PREDEFINED_CULTURES_ONLY`).
- On Linux .NET loads the system ICU libraries (`libicuuc`, `libicui18n`); if neither app-local nor system ICU is found and invariant mode is off, the process terminates with "Failed to load system ICU". Install ICU or enable invariant mode.

## Analyzers
CA1304 (specify CultureInfo), CA1305 (specify IFormatProvider), CA1307 (StringComparison for clarity), CA1309 (use ordinal StringComparison) and CA1310 (StringComparison for correctness) find these call sites. Microsoft's string guidance shows enabling CA1307, CA1309 and CA1310 via `AnalysisMode` in the project file, and severity is set in `.editorconfig` as `dotnet_diagnostic.CA1305.severity = warning`.

## Verify
Run the tests with the current culture set to a Turkish culture and a German culture in a fixture; persisted formats must not change.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Best practices for comparing strings" (rules 1-6), "Best practices for displaying data" (persist with invariant culture), the globalization runtime config page (invariant mode settings, PredefinedCulturesOnly), the ICU page (load failure message) and the CA1304/CA1307/CA1310 pages. Removed because not found: specific culture sample outputs, `IndexOf(char)` ordinality (the CA1307 page lists `IndexOf(char)` as a call that should take a StringComparison), ASP.NET Core `RequestLocalization` and `DefaultThreadCurrentCulture` advice, test-fixture variable names, ICU-versus-NLS collation claims, and `libicu` container advice beyond the documented load error.
Method: documentation only; no commands were run.
