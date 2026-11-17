---
id: computing-software.software-engineering.fsharp.dependency-audit
name: dependency-audit
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, dependency-audit, fsharp-security, nuget-audit, vulnerable-packages]
level: practitioner
status: docs-checked
description: "Audit NuGet dependencies for known vulnerabilities with NuGet Audit on restore and dotnet list package --vulnerable."
sources:
  - https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency auditing
**Goal:** find vulnerable packages early.

```bash
dotnet list package --vulnerable --include-transitive
dotnet list package --outdated
dotnet list package --deprecated
```
`dotnet package list` is the same command in the .NET 10 noun-first form. `--vulnerable` cannot be combined with `--deprecated` or `--outdated`, and `--include-transitive` is not on by default so add it. `--format json` gives machine-readable output.
```xml
<PropertyGroup>
  <NuGetAudit>true</NuGetAudit>
  <NuGetAuditMode>all</NuGetAuditMode>
  <NuGetAuditLevel>low</NuGetAuditLevel>
  <WarningsAsErrors>$(WarningsAsErrors);NU1903;NU1904</WarningsAsErrors>
</PropertyGroup>
```
- Restore runs the audit against the vulnerability data from your audit sources. Properties: `NuGetAudit` (default true), `NuGetAuditMode` (`direct` or `all`), `NuGetAuditLevel` (minimum severity: low, moderate, high, critical; default low).
- `NuGetAuditMode` defaults to `all` when a project targets net10.0 or higher, otherwise `direct`. If any target framework of a multi-targeted project selects `all`, all use it.
- Warnings: NU1900 error getting vulnerability info, NU1901 low, NU1902 moderate, NU1903 high, NU1904 critical severity package, NU1905 an audit source gives no vulnerability database.
- Audit sources come from the `auditSources` element in NuGet.Config; if absent, `packageSources` are used. nuget.org offers https://data.nuget.org/v3/index.json as a vulnerability-data-only index.
- `dotnet list package --vulnerable` uses audit sources from .NET SDK 9.0.300.
- To fail only in a dedicated pipeline, put the NU190x codes in `WarningsAsErrors` under a condition on a property (the page uses `AuditPipeline`) and run `dotnet restore -p:AuditPipeline=true`.
- Fixing: bump the vulnerable package; for a transitive one try updating the package closest to your direct reference first, then add the fixed version as a direct reference or use Central Package Management transitive pinning. `dotnet nuget why` shows why a transitive package is included. `dotnet package update --vulnerable` (.NET 10) updates to the first version without known vulnerabilities.
- Suppress a reviewed advisory with `<NuGetAuditSuppress Include="https://github.com/advisories/XXXX" />`; the page calls it a last resort and notes it suppresses the advisory for every package that shares it.

## Gotchas
- A clean result only means no known vulnerabilities at that moment; the advisory data changes, so audit in CI regularly.
- Making NU190x warnings errors everywhere lets a newly published advisory break unrelated builds; use `WarningsNotAsErrors` or the dedicated pipeline pattern.

## Self-check
Reference a known vulnerable package version in a scratch project and see an NU190x warning.

## Checked
Checked against the NuGet "Auditing package dependencies for security vulnerabilities" page and the dotnet package list reference.
Removed: the claim that audit applies only to nuget.org sources, the network-access gotcha, the Dependabot/Paket line (not on the pages) and the original generic index sources.
Method: docs-only read of cited pages, 2026-11-08
