---
id: computing-software.web-development.biome.linter-project-and-types-domains-scanner-rules
name: linter-project-and-types-domains-scanner-rules
category: computing-software
field: web-development
product: biome
tags: [biome, project-domain, types-domain, scanner, module-graph, inference-engine, no-import-cycles, no-private-imports, no-undeclared-dependencies, no-unresolved-imports]
level: advanced
status: docs-checked
description: "Project and types domains: rules that need the module graph or type inference, which ones are recommended, and the scan cost of enabling them."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/domains.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The **project** domain "contains rules that perform project-level analysis", including the module graph for dependency resolution. Enabling any rule that belongs to it makes Biome scan the entire project, which has a performance impact on linting (see the scanner section of the architecture docs).

The **types** domain adds the inference engine: Biome scans the project "and it will enable the inference engine to resolve and flat types".

**Project rules.** Recommended: `noPrivateImports`. Not recommended: `noUndeclaredDependencies`, `noUnresolvedImports`, `useImportExtensions`, `useJsonImportAttributes`, `noDeprecatedImports`, `noImportCycles`, and `noUntrustedLicenses` (JSON). Nursery: `noSelfImport`, `noTailwindRawColors`, `noUndeclaredClasses`, `noUndeclaredCustomProperties`, `useTailwindSortedClasses`, and CSS `noUnusedClasses`. Some also apply to HTML.

**Types rules.** Not nursery: `useArrayFind`, `useConsistentEnumValueType`, `noUnnecessaryConditions`, `useArraySortCompare`. Nursery type-aware rules include `noFloatingPromises`, `noMisusedPromises`, `noBaseToString`, `noUnsafeReturn`, `useAwaitThenable`, `useExhaustiveSwitchCases`, `useNullishCoalescing`, `useStrictBooleanExpressions`, `useStringStartsEndsWith`, `useIncludes`, `useRegexpExec`, `noMisleadingReturnType`, `noUnsafePlusOperands`, `noUnsafeUnaryMinus`, `noUselessTypeConversion`, `noMeaninglessVoidOperator`, `useDisposables`.

Config values per domain are the same three: `recommended`, `all`, `none` (for example `"project": "recommended"` under `linter.domains`).

The doc page is generated from source, so lists change with versions.

## Checked

2026-11-08. Read the domains page in full. Unchanged: project and types domain descriptions, the project and types rule lists and their recommended or nursery status. Removed: advice to set none per package and force-ignore build output (not on the page) and the invented Verify step.

Method: documentation only; no commands were run.
