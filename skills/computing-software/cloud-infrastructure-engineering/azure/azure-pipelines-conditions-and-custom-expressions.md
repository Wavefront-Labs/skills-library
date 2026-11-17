---
id: computing-software.cloud-infrastructure-engineering.azure.azure-pipelines-conditions-and-custom-expressions
name: azure-pipelines-conditions-and-custom-expressions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-pipelines-yaml, pipeline-conditions, succeededorfailed, expressions, runtime-variables]
level: advanced
status: gated
description: "Write Azure Pipelines conditions for stages, jobs and steps: status functions, variable and branch checks, dependency outputs, and compile-time vs runtime expressions."
sources: ["https://learn.microsoft.com/azure/devops/pipelines/process/conditions", "https://learn.microsoft.com/azure/devops/pipelines/process/expressions", "https://learn.microsoft.com/azure/devops/pipelines/process/set-variables-scripts"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure Pipelines conditions and expressions

**Goal:** run exactly the steps, jobs and stages you intend, including cleanup after failures.

## Status functions
| Function | Runs when |
|---|---|
| `succeeded()` (default) | All previous dependencies succeeded |
| `succeededOrFailed()` | Previous succeeded or failed, **not** when cancelled |
| `always()` | Even when cancelled |
| `failed()` | A previous dependency failed |
| `canceled()` | Run was cancelled |
Specifying any `condition:` **replaces** the default `succeeded()`; include it explicitly if you still need it.

## Examples
```yaml
- stage: Deploy
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'), ne(variables['Build.Reason'], 'PullRequest'))

- script: ./publish-test-results.sh
  condition: succeededOrFailed()              # publish results even if tests failed

- task: AzureCLI@2
  condition: and(succeeded(), eq(variables.deployInfra, 'true'))
```

## Outputs from earlier jobs/stages
```yaml
- job: A
  steps:
  - bash: echo "##vso[task.setvariable variable=changed;isOutput=true]true"
    name: detect
- job: B
  dependsOn: A
  condition: eq(dependencies.A.outputs['detect.changed'], 'true')
```

## Expression timing
The table below is (gated: unconfirmed, source is paywalled or blocked) (expressions reference page not fetched).
| Syntax | Evaluated | Use |
|---|---|---|
| `${{ }}` | Compile time (template expansion) | Parameters, `if`/`each` to include or remove YAML |
| `$[ ]` | Runtime, before job | Variables from dependencies, counters |
| `$(var)` | Macro, before task runs | Task inputs |
Conditions are runtime: use `variables['x']`, not `${{ }}`, for values set during the run. Use `${{ if eq(parameters.env, 'prod') }}:` to remove steps entirely.

## Gotchas
- Variables are strings: compare with `'true'`, not `true`.
- Cleanup steps should use `always()` but beware they also run when the run is cancelled mid-deploy.

## Verify
- [ ] Run the pipeline from a feature branch and from main; check the stage graph shows the intended skips with "condition evaluated to false" reasons.

## Checked

2026-10-28. Confirmed on the Azure Pipelines conditions page: succeededOrFailed() runs unless the run is canceled, always() runs even if canceled, failed() runs only when a previous dependency fails, a custom condition overwrites the default condition, multi-job output variables need isOutput=true, runtime-expression variables cannot be used in conditions within the same job. Removed: the cross-stage output syntax and the skipped-stage claim. Gated: the expression syntax timing table.

Method: documentation only; no commands were run.
