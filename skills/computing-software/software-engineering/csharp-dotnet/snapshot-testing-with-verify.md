---
id: computing-software.software-engineering.csharp-dotnet.snapshot-testing-with-verify
name: snapshot-testing-with-verify
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, verify-snapshot, snapshot-testing, approval-tests, scrubbers, dotnet-testing, xunit]
level: practitioner
status: gated
description: "Snapshot-test complex .NET output with Verify: verified vs received files, scrubbing GUIDs and dates, diff tools, HTTP/JSON/API approval, and keeping snapshots reviewable."
sources: ["https://github.com/VerifyTests/Verify", "https://github.com/VerifyTests/Verify/blob/main/docs/scrubbers.md", "https://github.com/VerifyTests/DiffEngine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot testing with Verify

**Goal:** test large or structured outputs (DTOs, JSON, generated code, emails, API
specs) without hand-writing dozens of assertions.

## Basics
```csharp
[UsesVerify]                       // the Verify README shows UsesVerifyAttribute for xUnit; check your framework package's docs (e.g. Verify.XunitV3)
public class InvoiceTests
{
    [Fact]
    public Task Renders_invoice()
    {
        var invoice = InvoiceBuilder.Sample().Build();
        return Verify(invoice);    // serialises to InvoiceTests.Renders_invoice.received.txt
    }
}
```
First run fails and writes `*.received.*`; when a diff tool is detected, DiffEngine shows the difference. Accepting moves the received file to `*.verified.*` (by hand, or via tooling such as DiffEngineTray). The Verify docs say to commit all `*.verified.*` files and exclude all `*.received.*` files from source control.

## Scrubbing nondeterminism
Verify scrubs nondeterministic values such as Guids and dates by default (placeholder naming and the opt-outs are in the Guid and Date docs) (gated: unconfirmed, source is paywalled or blocked). Extra rules on the scrubbers page include `ScrubLinesContaining` (removes lines containing any given string, case-insensitive by default) and the built-in `ScrubInlineGuids`:
```csharp
return Verify(result)
    .ScrubLinesContaining("generated at")
    .ScrubInlineGuids();
// ScrubMember, DontScrubDateTimes: member-level and opt-out settings, see the docs (gated: unconfirmed, source is paywalled or blocked)
```
Global settings belong in a `[ModuleInitializer]` (the README says global settings should be changed there):
```csharp
public static class VerifyInit
{
    [ModuleInitializer] public static void Init() => VerifierSettings.SortPropertiesAlphabetically();   // setting name: gated: unconfirmed, source is paywalled or blocked
}
```

## Useful integrations
- `Verify.Http`: verification of Http bits.
- `Verify.AspNetCore`: verification of AspNetCore bits (the `WebApplicationFactory` call shape here is illustrative).
- `Verify.EntityFramework`: verification of EntityFramework bits (capturing executed SQL: see its docs) (gated: unconfirmed, source is paywalled or blocked).
- `Verify.SourceGenerators`: verification of C# source generators.
- `VerifyJson(jsonString)`, `VerifyFile(path)`, images via `Verify.ImageSharp.Compare`.
- Parameterised tests: `UseParameters` exists (naming per case: see the docs) (gated: unconfirmed, source is paywalled or blocked).

## Keeping snapshots useful
- Small, focused snapshots; a 2,000-line snapshot nobody reads approves bugs.
- Review `.verified` diffs in PRs like code.
- CI must never auto-accept; Verify's build-server behaviour (including whether diff tools are launched) is in its "Build server" docs (gated: unconfirmed, source is paywalled or blocked).
- Use explicit assertions for the critical facts (totals, status) alongside snapshots.

## Verify
- [ ] `*.received.*` in `.gitignore`; `.verified.*` committed and reviewed.
- [ ] Tests stable across runs and machines (no culture/timezone/ordering drift).

## Checked

2026-11-02. Checked against the Verify README and docs/scrubbers.md on GitHub. Confirmed: UsesVerifyAttribute mentioned, framework packages (Verify.XunitV3, Verify.NUnit, MSTest, ...), module initializer for global settings, received/verified file handling, DiffEngine and DiffEngineTray, `ScrubLinesContaining` semantics, `ScrubInlineGuids` as a built-in scrubber, `VerifyJson`, integration packages Http, AspNetCore, EntityFramework, SourceGenerators, ImageSharp.Compare. Fixed: removed the xUnit 20+ version claim, the BuildServerDetector name and the CI diff-tool claim. Gated: ScrubMember, DontScrubDateTimes, default placeholder naming, SortPropertiesAlphabetically, UseParameters file naming, EF SQL capture.

Method: documentation only; no commands were run.
