---
id: computing-software.software-engineering.csharp-dotnet.nuget-config-source-mapping-and-lock-files
name: nuget-config-source-mapping-and-lock-files
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, nuget-config, package-source-mapping, nuget-lock-files, private-feeds, dependency-confusion, nuget, nuget-audit]
level: practitioner
status: docs-checked
description: "Configure NuGet feeds safely: nuget.config hierarchy and credentials, package source mapping against dependency confusion, lock files with locked-mode restore, and audit settings."
sources:
  - https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file
  - https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping
  - https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files#locking-dependencies
  - https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# nuget.config, source mapping and lock files

**Goal:** restores that come from the intended feeds, produce the same packages every
time, and flag vulnerable dependencies.

## nuget.config (repo root, committed)
```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />                                           <!-- ignore previously defined sources -->
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
    <add key="acme" value="https://pkgs.dev.azure.com/acme/_packaging/internal/nuget/v3/index.json" />
  </packageSources>
  <packageSourceMapping>
    <packageSource key="nuget.org"><package pattern="*" /></packageSource>
    <packageSource key="acme"><package pattern="Acme.*" /></packageSource>
  </packageSourceMapping>
</configuration>
```
Settings from several `nuget.config` files (repo, user, machine) are applied by precedence; `<clear />` makes NuGet ignore previously defined values for that node, so the repo config is self-contained.

## Package source mapping
Package source mapping improves supply chain security when you mix public and private sources: when a package exists on several sources, which one it comes from is otherwise not deterministic. Every package must match a pattern, and patterns are resolved by a defined precedence (see the source mapping reference). Mapping `Acme.*` to the internal feed keeps those IDs from coming from nuget.org.

## Credentials
Never commit secrets. In `nuget.config`, `packageSourceCredentials` values can reference environment variables (for example `%ContosoPassword%` for `ClearTextPassword`), so the file holds no secret. For hosted feeds (Azure Artifacts, GitHub Packages) follow the vendor's NuGet authentication guide.

## Lock files
```xml
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>   <!-- writes packages.lock.json -->
</PropertyGroup>
```
```bash
dotnet restore --locked-mode       # CI: fail if the lock file would change
dotnet restore --force-evaluate    # intentionally update the lock file
```
The lock file lists the full closure of package dependencies. Put the property in
`Directory.Build.props` to apply repo-wide; commit every `packages.lock.json`. Locked mode can also be set with `RestoreLockedMode`. If you pin the SDK, the SDK docs recommend `rollForward: disable` when using package lock files.

## Auditing
NuGet audit (NuGet 6.8 / .NET 8 SDK and later) warns about known-vulnerable packages: NU1901 (low) to NU1904 (critical). `NuGetAuditMode` defaults to `all` for net10.0 and later, otherwise `direct`; `NuGetAuditLevel` defaults to `low`. Include transitive packages and fail builds on high severity:
```xml
<NuGetAudit>true</NuGetAudit>
<NuGetAuditMode>all</NuGetAuditMode>
<NuGetAuditLevel>high</NuGetAuditLevel>
<WarningsAsErrors>$(WarningsAsErrors);NU1903;NU1904</WarningsAsErrors>
```
`dotnet list package --vulnerable --include-transitive` reports vulnerabilities (`--include-transitive` is not the default).

## Verify
- [ ] Restore on a clean machine with only repo config succeeds; mapping covers every package.
- [ ] CI uses `--locked-mode`; audit warnings for high/critical fail the build.

## Checked

Checked 2026-10-25 against NuGet/docs.microsoft.com-nuget (nuget-config-file, Package-Source-Mapping, Package-References-in-Project-Files, Auditing-Packages, cli-ref-restore) on main.
Confirmed: `<clear />` semantics and settings precedence; `packageSourceMapping` element and pattern precedence; environment variables in credentials; `RestorePackagesWithLockFile`, `packages.lock.json`, `dotnet restore --locked-mode`, `RestoreLockedMode`, `--force-evaluate`; NuGet audit warning ids NU1901-NU1904 and the `NuGetAuditMode`/`NuGetAuditLevel` defaults; `dotnet list package --vulnerable --include-transitive`; NuGet 6.8 / .NET 8 SDK as the audit baseline.
Removed as unconfirmed: the `dotnet nuget update source` credential recipe, `NuGetPackageSourceCredentials_*`, credential provider variables, the "queries every feed" restore-speed claim, `dotnet list package --outdated`.

Method: documentation only; no commands were run.
