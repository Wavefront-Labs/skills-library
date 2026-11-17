---
id: computing-software.software-engineering.csharp-dotnet.code-coverage-with-coverlet
name: code-coverage-with-coverlet
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, coverlet, code-coverage, reportgenerator, dotnet-coverage, dotnet-testing]
level: practitioner
status: docs-checked
description: "Collect .NET test coverage with the coverlet collector, MSBuild or MTP package, render with ReportGenerator, and merge Microsoft coverage files with dotnet-coverage."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-code-coverage
  - https://github.com/coverlet-coverage/coverlet
  - https://github.com/danielpalme/ReportGenerator
  - https://learn.microsoft.com/en-us/dotnet/core/additional-tools/dotnet-coverage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code coverage with coverlet

**Goal:** coverage reports for each test project, rendered into a readable report.

## Collector (VSTest, CLI only)
```bash
dotnet test --collect:"XPlat Code Coverage"
```
- "XPlat Code Coverage" is the friendly name of the coverlet data collector; it is required and case insensitive. Use "Code Coverage" for .NET's built-in collector.
- The run writes `coverage.cobertura.xml` into the `TestResults` directory (under a GUID folder per run).

## MSBuild integration
```bash
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura
```
Produces `coverage.cobertura.xml`.

## Microsoft.Testing.Platform (MTP)
The VSTest-based coverlet packages (collector and MSBuild) are incompatible with MTP, which has no data collectors; it uses in-process and out-of-process extensions configured by config file or command line. For MTP projects add the `coverlet.MTP` package and run the test project with `--coverlet`; `--coverlet-output-format` accepts json, lcov, opencover and cobertura (default output is json and cobertura).

## Render with ReportGenerator
```bash
dotnet tool install -g dotnet-reportgenerator-globaltool
reportgenerator -reports:"<path>/TestResults/<guid>/coverage.cobertura.xml" -targetdir:"coveragereport" -reporttypes:Html
```
ReportGenerator converts reports from coverlet, OpenCover, Cobertura, JaCoCo, lcov and others into human-readable reports.

## Merge Microsoft coverage files
`dotnet-coverage merge -o merged.cobertura.xml -f cobertura **/*.coverage` merges all matching reports and writes a Cobertura file; `-f` supports coverage, xml and cobertura (default is the binary coverage format). Exclusions in its settings file use the same format as the runsettings data collector configuration, including `ExcludeFromCodeCoverageAttribute`.

## Verify
- [ ] Each test project produces a Cobertura file.
- [ ] The report is generated from those files in CI and kept as an artifact.

## Checked
2026-11-01. Confirmed against Microsoft Learn "Use code coverage for unit testing", the dotnet-coverage page, and the coverlet and ReportGenerator READMEs (collector name, output location, MSBuild properties, MTP incompatibility and coverlet.MTP options, reportgenerator options, merge command and formats). Removed as unconfirmed: runsettings sample, threshold properties, Microsoft.Testing.Extensions.CodeCoverage flags, MarkdownSummaryGithub, DeterministicReport and ContinuousIntegrationBuild advice, Codecov/Sonar upload.
Method: documentation only; no commands were run.
