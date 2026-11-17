---
id: computing-software.cloud-infrastructure-engineering.azure.azure-pipelines-publish-test-results-and-code-coverage
name: azure-pipelines-publish-test-results-and-code-coverage
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-pipelines-yaml, publish-test-results, code-coverage, test-analytics, flaky-tests]
level: practitioner
status: docs-checked
description: "Publish JUnit/TRX/NUnit test results and Cobertura or JaCoCo code coverage in Azure Pipelines, merge reports, show trends, and gate on coverage."
sources: ["https://learn.microsoft.com/azure/devops/pipelines/tasks/reference/publish-test-results-v2", "https://learn.microsoft.com/azure/devops/pipelines/tasks/reference/publish-code-coverage-results-v2", "https://learn.microsoft.com/azure/devops/pipelines/test/review-code-coverage-results", "https://learn.microsoft.com/azure/devops/pipelines/test/flaky-test-management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing test results and coverage

**Goal:** test outcomes and coverage visible on every run, with trends and PR gates.

## Test results
```yaml
- script: ./run-tests.sh   # writes TRX results and a Cobertura coverage file under $(Agent.TempDirectory)/tr
- task: PublishTestResults@2
  condition: succeededOrFailed()
  inputs:
    testResultsFormat: VSTest            # JUnit (default) | NUnit | VSTest | XUnit | CTest
    testResultsFiles: '**/*.trx'
    searchFolder: $(Agent.TempDirectory)/tr   # default $(System.DefaultWorkingDirectory)
    mergeTestResults: true               # default false
    failTaskOnFailedTests: true          # default false
    testRunTitle: 'Unit $(Agent.OS)'
```
- Tools that emit JUnit XML use `JUnit`; set `testResultsFormat` to match whatever your runner writes.
- Flaky test management is configured under Project settings > Test management (Pipelines section).

## Code coverage
```yaml
- task: PublishCodeCoverageResults@2
  inputs:
    summaryFileLocation: '$(Agent.TempDirectory)/tr/**/coverage.cobertura.xml'
```
- v2 accepts many formats (`.coverage`, Cobertura and JaCoCo XML, lcov and others), merges multiple summary files into one report, and publishes an HTML report plus the **Code Coverage** tab. It is build pipelines only, not release pipelines.
- JaCoCo reports carry no absolute source paths: set `pathToSources` (for example to `src/main/java/`). `failIfCoverageEmpty` defaults to false.
- Tasks such as Visual Studio Test, .NET Core, Maven and Gradle can publish coverage themselves, so a separate task is then unnecessary.

## Gate on coverage in PRs
- Diff coverage: Azure DevOps posts a coverage status on PRs for changed lines when coverage is published. The default target is 70%; change it in `azurepipelines-coverage.yml` at the repo root. The status is advisory until you add a branch policy that requires it (the status is named `<pipeline>/codecoverage`):
```yaml
coverage:
  status:
    comments: on
    diff:
      target: 70%
```
- Or fail the build with a threshold in your own coverage tooling.

## Gotchas
- Without `condition: succeededOrFailed()`, results are not published when tests fail, which is exactly when you need them.
- A glob that matches no files publishes nothing; check `testResultsFiles` and `searchFolder` against the task log.

## Verify
- [ ] Tests tab shows counts and failures; Code Coverage tab shows line coverage; PR shows a coverage status.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Publish Test Results v2, Publish Code Coverage Results v2, Review code coverage results, Flaky test management, pipeline expressions pages): `testResultsFormat` values and default, `searchFolder`, `mergeTestResults` and `failTaskOnFailedTests` defaults, `PublishCodeCoverageResults@2` inputs and formats, `azurepipelines-coverage.yml` with 70% default diff target, advisory status and branch policy, flaky test settings location, `succeededOrFailed()` condition function. Removed: dotnet, pytest, jest and coverlet command lines, DotNetCoreCLI auto-publish claim, log message text.
Method: documentation only; no commands were run.
