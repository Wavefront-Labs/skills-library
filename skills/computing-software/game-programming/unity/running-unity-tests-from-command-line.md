---
id: computing-software.game-programming.unity.running-unity-tests-from-command-line
name: running-unity-tests-from-command-line
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-testing, unity-tests-cli, runtests, nunit-xml, ci-testing, code-coverage, game-programming]
level: practitioner
status: docs-checked
description: "Run Unity Test Framework suites headless in CI with -runTests: platforms, filters, NUnit XML results and code coverage in batchmode."
sources: ["https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html", "https://docs.unity3d.com/Packages/com.unity.testtools.codecoverage@1.2/manual/CoverageBatchmode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Unity tests from the command line

**Goal:** CI runs Edit Mode and Play Mode suites on every push and reads the result file.

## Command
```
Unity -batchmode -projectPath <project> -runTests -testPlatform EditMode -testResults results/editmode.xml
Unity -batchmode -projectPath <project> -runTests -testPlatform PlayMode -testResults results/playmode.xml
```
- Use `-batchmode` so no manual user input is needed.
- `-testPlatform` accepts `EditMode`, `PlayMode` (Play Mode tests in the Editor) or any `BuildTarget` value (Play Mode
  tests on a player built for that platform). With no value, tests run in Edit Mode.
- `-testFilter "Low;Medium"`: semicolon-separated test names (quoted) or a regular expression on the full test name.
  A leading `!` negates. A parameterised variation can be named like `"ClassName\.MethodName\(Param1,Param2\)"`.
- `-testCategory "firstCategory;secondCategory"`: same rules for categories. If both filter and category are given,
  only tests matching both run.
- `-assemblyNames "firstAssembly;secondAssembly"` limits the run to test assemblies.
- `-runSynchronously` runs Edit Mode tests in one editor update; multi-frame tests (`[UnityTest]`, `[UnitySetUp]`,
  `[UnityTearDown]`) are filtered out.
- `-retry <n>` retries failing tests up to n times; `-repeat <n>` repeats passing tests up to n times.
- `-playerHeartbeatTimeout <seconds>` is how long the editor waits for heartbeats from a player run (default 10 minutes).

## Results
- `-testResults <path>` writes the result file in NUnit XML format (default location is the project root).
- The Test Framework page states there is no common definition for exit codes across Unity components under test: read
  the error messages and stack traces rather than relying on a specific code.

## Code coverage
Install the Code Coverage package (`com.unity.testtools.codecoverage`), then add:
```
-debugCodeOptimization -enableCodeCoverage -coverageResultsPath <coverage-folder> -coverageOptions "generateAdditionalMetrics;generateHtmlReport;assemblyFilters:+my.assembly.*"
```
- `-coverageResultsPath` is optional (default is the project path).
- `-coverageOptions` values are separated by semicolons, so quote them in shells that treat `;` as a separator.
- `generateHtmlReport` makes an HTML report; `generateAdditionalMetrics` adds Cyclomatic Complexity and Crap Score;
  `generateAdditionalReports` generates SonarQube, Cobertura and LCOV reports.
- `assemblyFilters` is a comma-separated list; prefix with `+` to include, `-` to exclude; aliases `<all>`, `<assets>`,
  `<packages>`. With no included assemblies, only those under Assets are covered.
- `dontClear` accumulates results across sessions, which lets an Edit Mode run and a Play Mode run feed one report.
- The coverage results XML follows the OpenCover format.

## Verify
- [ ] The result XML exists after the run and your CI reads it.
- [ ] The coverage report lists the assemblies you expect (adjust `assemblyFilters` otherwise).

## Checked
Date: 2026-11-09. Read in full: Unity Test Framework 1.4 "Running tests from the command line" and Code Coverage 1.2
"Using Code Coverage in batchmode" (batchmode options table and examples). Removed as not on those pages: the claim to
omit `-quit` with `-runTests`, the 0/2/3 exit codes (the page says there is no common exit-code definition),
`-nographics`/Xvfb advice, `-logFile`, `-buildTarget`, the GameCI GitHub Actions example, CI-system ingestion advice and
`Library/` caching advice.
Method: docs-checked 2026-11-09 against the two Unity manual pages named above.
