---
id: computing-software.software-engineering.csharp-dotnet.writing-a-custom-roslyn-analyzer
name: writing-a-custom-roslyn-analyzer
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-code-analysis, custom-analyzer, roslyn, diagnosticanalyzer, code-fix, netstandard2-0]
level: advanced
status: draft
description: "Author a Roslyn DiagnosticAnalyzer and CodeFixProvider: netstandard2.0 project setup, operation actions, tests with the analyzer testing library, and NuGet packaging."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/tutorials/how-to-write-csharp-analyzer-code-fix", "https://github.com/dotnet/roslyn-analyzers/blob/main/docs/Writing%20a%20new%20analyzer.md", "https://github.com/dotnet/roslyn-sdk/tree/main/src/Microsoft.CodeAnalysis.Testing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom Roslyn analyzer

Project: class library targeting **netstandard2.0** (the compiler/IDE load it), packages `Microsoft.CodeAnalysis.CSharp` (PrivateAssets=all) and `Microsoft.CodeAnalysis.Analyzers`. Template: `dotnet new install Microsoft.CodeAnalysis.Templates`... or VS "Analyzer with Code Fix".

```csharp
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class NoDateTimeNowAnalyzer : DiagnosticAnalyzer
{
    public static readonly DiagnosticDescriptor Rule = new("ACME001", "Use TimeProvider", "Use TimeProvider instead of '{0}'",
        "Design", DiagnosticSeverity.Warning, isEnabledByDefault: true, helpLinkUri: "https://example.com/rules/ACME001");
    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics => ImmutableArray.Create(Rule);

    public override void Initialize(AnalysisContext ctx)
    {
        ctx.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
        ctx.EnableConcurrentExecution();
        ctx.RegisterOperationAction(c =>
        {
            var p = (IPropertyReferenceOperation)c.Operation;               // semantic model: no string matching of names
            if (p.Property.ContainingType.ToDisplayString() == "System.DateTime" && p.Property.Name is "Now" or "UtcNow")
                c.ReportDiagnostic(Diagnostic.Create(Rule, p.Syntax.GetLocation(), p.Property.Name));
        }, OperationKind.PropertyReference);
    }
}
```
Code fix: `[ExportCodeFixProvider]` deriving `CodeFixProvider`, `FixableDiagnosticIds`, register `CodeAction.Create(title, ct => ReplaceAsync(...))` editing the syntax tree (`SyntaxFactory`, `DocumentEditor`) and `WellKnownFixAllProviders.BatchFixer`.

## Testing
`Microsoft.CodeAnalysis.CSharp.Analyzer.Testing` (+ xUnit): 
```csharp
await CSharpAnalyzerVerifier<NoDateTimeNowAnalyzer, DefaultVerifier>.VerifyAnalyzerAsync(
    "class C { void M() { var x = {|ACME001:System.DateTime.UtcNow|}; } }");
```
Test no-diagnostic cases and edge syntax, plus the fix via `CSharpCodeFixVerifier`.

## Packaging and rules
- Pack into `analyzers/dotnet/cs` of the NuGet; `<IncludeBuildOutput>false</IncludeBuildOutput>`, `<DevelopmentDependency>true</DevelopmentDependency>`.
- Prefer operation/symbol actions over syntax actions; `RegisterCompilationStartAction` to cache type lookups once.
- Analyzers run in the IDE constantly: avoid allocations, no I/O, no static mutable state, be thread-safe.
- Keep released rule ids in `AnalyzerReleases.Shipped.md`/`Unshipped.md` (RS2000 warnings).
- Severity can be overridden by users with `.editorconfig` (`dotnet_diagnostic.ACME001.severity = error`).
- Roslyn version compatibility: reference the lowest Roslyn that supports your target SDKs.

## Gotchas
- Loading a netstandard2.0 analyzer cannot use newer BCL APIs.
- Diagnostics id collisions with other packages.
- Source generators are separate (`IIncrementalGenerator`).

## Verify
Tests pass; add the package to a sample project and see the squiggle in the IDE and a build warning from `dotnet build`.
