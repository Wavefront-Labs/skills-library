---
id: computing-software.software-engineering.refactoring.deprecating-and-removing-library-api
name: deprecating-and-removing-library-api
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, api-deprecation-refactoring, deprecation, semver, library-maintenance, codemods]
level: advanced
status: draft
description: "Deprecate and remove library API safely: deprecation annotations with replacements, warnings, semver timing, migration codemods and measuring remaining usage before removal."
sources: ["https://semver.org/", "https://docs.python.org/3/library/warnings.html#warnings.deprecated", "https://docs.oracle.com/en/java/javase/21/core/enhanced-deprecation1.html", "https://learn.microsoft.com/en-us/dotnet/api/system.obsoleteattribute"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deprecating and removing library API

## 1. Provide the replacement first
New function/class/parameter ships and is documented before anything is deprecated. The old one
delegates to the new one so there's one implementation.

## 2. Mark it deprecated (machine-readable)
- Java: `@Deprecated(since = "4.2", forRemoval = true)` + Javadoc `@deprecated use {@link #parse(Path)}`.
- C#: `[Obsolete("Use Parse(Path). Will be removed in 5.0.", DiagnosticId = "ACME001", UrlFormat = "https://...")]`
  (error: true in the final release before removal).
- Kotlin: `@Deprecated("...", ReplaceWith("parse(path)"), level = DeprecationLevel.WARNING)` lets IDEs auto-fix.
- Python 3.13+: `@warnings.deprecated("use parse()")` (also `typing_extensions.deprecated`) so type
  checkers flag calls; plus runtime `warnings.warn(..., DeprecationWarning, stacklevel=2)`.
- TypeScript/JS: JSDoc `/** @deprecated use parse() */` (editors strike through) + optional one-time
  `process.emitWarning`.
- Rust: `#[deprecated(since = "0.9.0", note = "use parse")]`. Go: `// Deprecated: use Parse.` comment
  paragraph (gopls and staticcheck SA1019 flag uses).
Message must name the replacement and the removal version.

## 3. Timeline (semver)
Deprecate in a minor release; remove only in the next major. Keep at least one minor (often a year
for widely used libraries) between. Document in the changelog and migration guide.

## 4. Help migration
- Codemods: OpenRewrite recipes (Java), jscodeshift, LibCST/Bowler (Python), `gofix`-style
  `//go:fix inline` directives, Roslyn code fixes, Kotlin `ReplaceWith`.
- Search dependents (GitHub code search, sourcegraph, deps.dev) to see real usage.

## 5. Remove
Major release, migration guide link in release notes. Remove tests of the old API, but keep a test
that the old name no longer exists if accidental re-export is a risk.

## Internal codebases
Same steps; you can measure all call sites, migrate them yourself (codemod PR), then delete in one
go. Linters with "banned API" rules (`no-restricted-imports`, `BannedApiAnalyzers`) stop new uses.
