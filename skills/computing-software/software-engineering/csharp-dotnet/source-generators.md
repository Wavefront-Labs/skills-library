---
id: computing-software.software-engineering.csharp-dotnet.source-generators
name: source-generators
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, source-generators, incremental-generators, roslyn, compile-time-codegen, aot-friendly, json-source-generation]
level: advanced
status: docs-checked
description: "Use and write C# source generators: built-in ones (System.Text.Json, LoggerMessage), writing an IIncrementalGenerator, packaging, debugging and performance rules."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/source-generators-overview", "https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.md", "https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/source-generation", "https://learn.microsoft.com/en-us/dotnet/core/extensions/logger-message-generator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Source generators

**Goal:** replace runtime reflection with compile-time generated code - faster startup,
trimming/AOT compatibility - and know when to write your own.

## Built-in generators worth using
```csharp
[JsonSerializable(typeof(Order))]
internal partial class AppJsonContext : JsonSerializerContext { }
JsonSerializer.Serialize(order, AppJsonContext.Default.Order);      // no reflection, AOT-safe


[LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} shipped")]
static partial void LogShipped(ILogger logger, Guid orderId);        // no boxing/params arrays
```

## Writing an incremental generator
```csharp
[Generator]
public sealed class ToStringGenerator : IIncrementalGenerator
{
    public void Initialize(IncrementalGeneratorInitializationContext ctx)
    {
        var types = ctx.SyntaxProvider.ForAttributeWithMetadataName(
            "Acme.AutoToStringAttribute",
            predicate: static (node, _) => node is ClassDeclarationSyntax,
            transform: static (c, _) => new Model(((INamedTypeSymbol)c.TargetSymbol).Name,
                ((INamedTypeSymbol)c.TargetSymbol).ContainingNamespace.ToDisplayString()));
        ctx.RegisterSourceOutput(types, static (spc, m) =>
            spc.AddSource($"{m.Name}.g.cs", $"namespace {m.Ns}; partial class {m.Name} {{ public override string ToString() => \"{m.Name}\"; }}"));
    }
    private sealed record Model(string Name, string Ns);     // value-equatable: enables caching
}
```
Rules: implement `IIncrementalGenerator`; use `ForAttributeWithMetadataName`; transform into small
**equatable** models (records) so unchanged inputs can be cached and skip regeneration;
generators only add code, never modify user code.


## Debugging and inspection
- Unit test a generator by running it in a test and snapshotting the generated source.

## Verify
- [ ] Generated files are visible in the IDE and build output.
- [ ] Editing an unrelated file does not re-run the generator's output step (incremental caching works).

## Checked

- Date: 2026-10-28
- Confirmed on Microsoft Learn (source generators overview, System.Text.Json source generation, logger message generator) and the Roslyn incremental generators doc: JsonSerializable context, LoggerMessage generator, IIncrementalGenerator, ForAttributeWithMetadataName.
- Removed: GeneratedRegex and LibraryImport examples, configuration-binding generator property, packaging/target framework details, EmitCompilerGeneratedFiles, CSharpGeneratorDriver, ReportDiagnostic, ISymbol remark.
Method: documentation only; no commands were run.
