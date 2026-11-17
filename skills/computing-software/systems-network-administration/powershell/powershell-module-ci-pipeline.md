---
id: computing-software.systems-network-administration.powershell.powershell-module-ci-pipeline
name: powershell-module-ci-pipeline
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-modules, module-ci, pester, psscriptanalyzer, module-publishing]
level: advanced
status: draft
description: "Build a CI pipeline for PowerShell modules: PSScriptAnalyzer, Pester with code coverage, versioning from tags, packaging and publishing to a private feed on release."
sources:
  - https://pester.dev/docs/usage/code-coverage
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CI pipeline for PowerShell modules

## Repository layout
```
MyModule/
  src/MyModule.psd1  src/MyModule.psm1  src/Public/*.ps1  src/Private/*.ps1
  tests/*.Tests.ps1
  build.ps1
  .github/workflows/ci.yml
```

## build.ps1 steps
```powershell
param([string]$Version = '0.0.1')
Invoke-ScriptAnalyzer -Path ./src -Recurse -Settings ./PSScriptAnalyzerSettings.psd1 -EnableExit
$cfg = New-PesterConfiguration
$cfg.Run.Path = './tests'; $cfg.Run.Exit = $true
$cfg.CodeCoverage.Enabled = $true; $cfg.CodeCoverage.Path = './src'; $cfg.CodeCoverage.CoveragePercentTarget = 75
$cfg.TestResult.Enabled = $true; $cfg.TestResult.OutputFormat = 'JUnitXml'
Invoke-Pester -Configuration $cfg
# stamp version and exported functions into the manifest
$public = (Get-ChildItem ./src/Public/*.ps1).BaseName
Update-ModuleManifest ./src/MyModule.psd1 -ModuleVersion $Version -FunctionsToExport $public
```

## GitHub Actions
```yaml
on: { push: { branches: [main], tags: ['v*'] }, pull_request: {} }
jobs:
  test:
    strategy: { matrix: { os: [windows-latest, ubuntu-latest] } }
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - shell: pwsh
        run: |
          Install-PSResource Pester, PSScriptAnalyzer -TrustRepository
          ./build.ps1 -Version ($env:GITHUB_REF_NAME -replace '^v','' -replace '^main$','0.0.1')
  publish:
    if: startsWith(github.ref, 'refs/tags/v')
    needs: test
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - shell: pwsh
        run: |
          ./build.ps1 -Version ($env:GITHUB_REF_NAME -replace '^v','')
          Register-PSResourceRepository -Name Internal -Uri ${{ vars.FEED_URL }} -Trusted
          Publish-PSResource -Path ./src -Repository Internal -ApiKey ${{ secrets.FEED_KEY }}
```
Add a Windows PowerShell 5.1 job (`shell: powershell`) if the module supports 5.1.

## Verify
- [ ] PRs fail on analyser errors or test failures; tagged releases appear in the feed with the tag's version.
