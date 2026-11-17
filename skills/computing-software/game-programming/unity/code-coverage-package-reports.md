---
id: computing-software.game-programming.unity.code-coverage-package-reports
name: code-coverage-package-reports
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-code-coverage, code-coverage, testing, ci, game-programming]
level: practitioner
status: docs-checked
description: "Unity Code Coverage package 1.2: batchmode arguments and coverageOptions, assembly and path filters, combined EditMode and PlayMode reports, and reading the HTML report."
sources: ["https://docs.unity3d.com/Packages/com.unity.testtools.codecoverage@1.2/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.testtools.codecoverage@1.2/manual/CoverageBatchmode.html", "https://docs.unity3d.com/Packages/com.unity.testtools.codecoverage@1.2/manual/HowToInterpretResults.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code Coverage package

**Goal:** gather and read test coverage with the Unity Code Coverage package (1.2 docs).

## What it does
- Used with the Test Runner; after a run it generates an HTML report of which lines the tests executed.
  Supports PlayMode and EditMode tests, tracks coverage over time, and has a Coverage Recording feature
  to capture coverage on demand without tests.
- The report measures whether code is executed, not test quality. Other outputs: SonarQube, Cobertura and
  LCOV reports, and SVG/PNG summary badges.

## Batchmode
Arguments: `-enableCodeCoverage`; optional `-coverageResultsPath` and `-coverageHistoryPath` (default:
the project path); optional `-coverageOptions` with semicolon-separated options, quoted so shells do not
split it.

Options (page table): `generateHtmlReport`, `generateHtmlReportHistory`, `generateAdditionalReports`
(SonarQube, Cobertura, LCOV), `generateBadgeReport`, `generateAdditionalMetrics` (Cyclomatic Complexity
and Crap Score per method), `generateTestReferences`, `verbosity` (default info), `useProjectSettings`
(batchmode only), `dontClear`, `sourcePaths`, `assemblyFilters`, `pathFilters`, `pathFiltersFromFile`,
`filtersFromFile` (JSON), `pathReplacePatterns`.
- `assemblyFilters`: comma-separated, `+` include / `-` exclude, globbing allowed, aliases `<all>`,
  `<assets>`, `<packages>`. With no included assemblies, only those under Assets are included.
  Example: `assemblyFilters:+my.assembly.*,-my.assembly.tests`.
- `pathFilters`: same `+`/`-` form; relative paths need `sourcePaths`. If `pathFilters` is set with no
  included assemblies, all assemblies are included so path filtering takes precedence.
- `pathFiltersFromFile` will be deprecated next major release; use `filtersFromFile`.

Page example: `Unity.exe -projectPath <path> -batchmode -testPlatform editmode -runTests -testResults
<xml> -debugCodeOptimization -enableCodeCoverage -coverageResultsPath <dir> -coverageOptions
"generateAdditionalMetrics;generateHtmlReport;assemblyFilters:+my.assembly.*"`. The page passes
`-debugCodeOptimization` so Code optimization is in Debug mode.

Combined EditMode and PlayMode report: run the Editor three times: EditMode tests with `dontClear`,
PlayMode tests with `dontClear`, then a third run without `-runTests`, with `generateHtmlReport` and
`-quit`, using the same `-coverageResultsPath`. In Unity Test Framework 2.0+ results from both are in the
Automated folder; `dontClear` stops the first being cleared.

## Reading the HTML report
Open `index.htm` in the `Report` folder under `-coverageResultsPath`. Summary shows Line Coverage of
coverable lines (green or red); Coverage History appears only with history enabled; Risk Hotspots appear
only with additional metrics, listing methods with Cyclomatic Complexity above 15 and high Crap Score.
NPath Complexity and Branch Coverage are not implemented and always show zero.

## Checked
Date: 2026-11-07

Read in full: the package About page, the batchmode page (all option rows and examples) and "How to
interpret the results". The Code Coverage window pages, Quickstart, Code Optimization and other package
pages were not opened.

Removed because the pages do not confirm it: the Window > Analysis menu path and window options (Included
Assemblies, badges toggles), the example filter `-**/Generated/**` as an Editor path filter, IL2CPP
players producing no coverage, the asmdef-only collection claim, "coverage slows tests", the advice to
target specific game logic, the CI gate Verify item, and the claim that the draft's command line runs
merge with a repeated results path alone (the page requires `dontClear`).

Method: documentation only; no commands were run.
