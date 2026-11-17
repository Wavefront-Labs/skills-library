---
id: computing-software.software-engineering.csharp-dotnet.roslyn-analyzers-and-editorconfig-severity
name: roslyn-analyzers-and-editorconfig-severity
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, dotnet-testing, roslyn-analyzers, editorconfig, code-analysis, code-style, warnings-as-errors, dotnet-format, dotnet-code-analysis]
level: practitioner
status: docs-checked
description: "Configure .NET code analysis: built-in CA/IDE analyzers, AnalysisLevel, .editorconfig severities, enforcing code style in build, third-party analyzers and suppressions."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/configuration-options
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/code-style-rule-options
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/suppress-warnings
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Roslyn analyzers and .editorconfig severity

**Goal:** quality and style rules enforced at compile time in the IDE and CI, with severities owned by the repo.

## 1. Turn analysis on
```xml
<!-- Directory.Build.props -->
<PropertyGroup>
  <AnalysisLevel>latest-recommended</AnalysisLevel>   <!-- none | default | minimum | recommended | all -->
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>   <!-- IDExxxx rules in dotnet build -->
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  <CodeAnalysisTreatWarningsAsErrors>true</CodeAnalysisTreatWarningsAsErrors>
</PropertyGroup>
```
- CA rules (quality: CA2007 ConfigureAwait, CA1062 null args, CA2000 dispose) ship with the SDK (`Microsoft.CodeAnalysis.NetAnalyzers`).
- IDE rules (style: IDE0005 unused usings, IDE0090 `new()`) need `EnforceCodeStyleInBuild` to run outside the editor.

## 2. .editorconfig severities
```ini
root = true

[*.cs]
# style preferences
csharp_style_namespace_declarations = file_scoped:warning
csharp_style_var_for_built_in_types = true:suggestion
dotnet_style_qualification_for_field = false:warning

# analyzer severities
dotnet_diagnostic.CA2007.severity = none          # no ConfigureAwait in ASP.NET Core apps
dotnet_diagnostic.CA1848.severity = warning       # use LoggerMessage delegates
dotnet_diagnostic.IDE0005.severity = warning
dotnet_analyzer_diagnostic.category-Security.severity = error

[tests/**.cs]
dotnet_diagnostic.CA1707.severity = none          # underscores in test names
```
Severities: `error`, `warning`, `suggestion`, `silent`, `none`. Rules are configured per glob section; see the precedence rules on the configuration options page.

## 3. Third-party analyzers
Add third-party analyzer packages one at a time and tune noise before adding the next.

## 4. Suppressions
- Code: `#pragma warning disable CA1031 // justification` ... `restore`, smallest scope.
- Attribute: `[SuppressMessage("Design", "CA1031", Justification = "top-level handler logs and rethrows")]`.
- Repo-wide decisions belong in `.editorconfig`, not scattered in project-file properties (less discoverable).

## 5. Formatting
`dotnet format` applies style and analyzer fixes; `dotnet format --verify-no-changes` in CI. `dotnet format --diagnostics CA1822` limits the run to one rule ID.

## Gotchas
- Bumping SDK with `AnalysisLevel=latest` brings new rules; with warnings-as-errors this breaks the build on upgrade. Pin `AnalysisLevel` to a number (`9.0-recommended`) for predictability.
- Generated code: mark with `[GeneratedCode]` or `generated_code = true` in editorconfig so rules skip it.
- IDE-only behaviour differences: rules at `suggestion` show in the editor but never fail builds.
- Global AnalyzerConfig files (`.globalconfig`) apply by project, not path; useful for shipping rule sets as NuGet packages.

## Verify
- The warnings-as-errors build passes on CI and `dotnet format --verify-no-changes` is clean.

## Checked

- Date: 2026-10-28
- Confirmed on Microsoft Learn (code analysis overview, configuration options, dotnet format pages): EnforceCodeStyleInBuild, AnalysisLevel, dotnet_analyzer_diagnostic.category-*.severity, generated_code, dotnet format --verify-no-changes and --diagnostics.
- Removed: GenerateDocumentationFile requirement for IDE0005, third-party package list, dotnet format analyzers subcommand, most-specific-wins wording, async void build-failure claim.
Method: documentation only; no commands were run.
