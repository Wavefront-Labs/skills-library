---
id: computing-software.cloud-infrastructure-engineering.azure.azure-pipelines-yaml-templates-and-agents
name: azure-pipelines-yaml-templates-and-agents
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, azure-pipelines, yaml-pipelines, pipeline-templates, multi-stage-pipelines, stages, jobs, steps, template-expressions, runtime-parameters, extends-templates, template-repositories, conditions, dependson, matrix-strategy, caching, pipeline-artifacts, self-hosted-agents, agent-pools, managed-devops-pools, scale-set-agents, microsoft-hosted-agents, parallel-jobs, pipeline-triggers, pr-triggers, path-filters, pipeline-decorators]
level: practitioner
status: draft
description: "Author Azure Pipelines that scale: multi-stage YAML, templates and extends, parameters vs variables, expression timing, triggers, caching, matrix jobs, agent pools."
sources: ["https://learn.microsoft.com/en-us/azure/devops/pipelines/process/templates", "https://learn.microsoft.com/en-us/azure/devops/pipelines/process/phases", "https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/agents", "https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted", "https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/scale-set-agents"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure Pipelines YAML — templates, expression timing and agents that don't bottleneck

**Goal:** every repo's pipeline is a 20-line file that `extends` a governed template,
stages map to environments, expressions evaluate when you think they do, and agents
are sized and placed (hosted vs your VNet) on purpose.

## 1. Shape
```yaml
# azure-pipelines.yml in the app repo
trigger: { branches: { include: [main] }, paths: { exclude: [docs/*, '*.md'] } }
pr: { branches: { include: [main] } }
resources:
  repositories:
    - repository: templates
      type: git
      name: Platform/pipeline-templates
      ref: refs/tags/v3
parameters:
  - name: deployTo
    type: string
    default: dev
    values: [dev, test, prod]
extends:
  template: pipelines/dotnet-service.yml@templates
  parameters:
    serviceName: orders
    deployTo: ${{ parameters.deployTo }}
```
```yaml
# Platform/pipeline-templates/pipelines/dotnet-service.yml (extends template = governance boundary)
parameters: [{ name: serviceName, type: string }, { name: deployTo, type: string }]
stages:
  - stage: build
    jobs:
      - job: build
        pool: { vmImage: ubuntu-latest }
        steps:
          - template: ../steps/dotnet-build.yml
            parameters: { project: src/${{ parameters.serviceName }} }
          - publish: $(Build.ArtifactStagingDirectory)
            artifact: drop
  - ${{ if ne(parameters.deployTo, '') }}:
    - stage: deploy_${{ parameters.deployTo }}
      dependsOn: build
      condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
      jobs:
        - deployment: deploy
          environment: ${{ parameters.deployTo }}
          pool: { name: aks-agents-${{ parameters.deployTo }} }
          strategy:
            runOnce:
              deploy:
                steps:
                  - download: current
                    artifact: drop
                  - task: AzureCLI@2
                    inputs: { azureSubscription: sc-${{ parameters.deployTo }}, scriptType: bash, scriptLocation: inlineScript, inlineScript: ./deploy.sh }
```
- **Templates**: `steps`, `jobs`, `stages`, `variables` templates for reuse; **`extends`** templates for control (the template defines the structure a pipeline must follow; add a required template approval to enforce it).
- Template repo versioning by tag/branch (`ref:`) — never `main` for prod consumers.

## 2. Expression timing (the thing that bites everyone)
| Syntax | When | Use for |
|---|---|---|
| `${{ }}` compile-time (template expressions) | when the YAML is expanded, before the run starts | parameters, conditional insertion of stages/steps (`${{ if }}`), `each` loops |
| `$[ ]` runtime expressions | at job/stage start | `dependsOn` outputs (`$[ dependencies.build.outputs['job.var'] ]`), variables set earlier |
| `$(var)` macro | when the step runs | task inputs, scripts |
- Variables set with `##vso[task.setvariable variable=x;isOutput=true]` are available in later jobs via `dependencies`/`stageDependencies` runtime expressions; only runtime expressions see them.
- `parameters` are typed and compile-time → use for anything that changes pipeline *structure*; `variables` are strings and runtime → values.
- `condition:` is evaluated at runtime with `succeeded()`, `failed()`, `always()`, `eq(variables[...])`; a job with `condition: always()` runs even on cancel — for cleanup only.

## 3. Build mechanics
- **Triggers**: CI (`trigger`) with branch/path filters; `pr` for PR validation (GitHub needs the app; Azure Repos uses branch policies **instead** of `pr:`); `schedules` (cron; `always` defaults to false, so a scheduled run is skipped when nothing changed); pipeline **resources** (`resources.pipelines` with `trigger: true`) for chained pipelines.
- **Caching**: `Cache@2` keyed on lockfiles (`key: 'npm | "$(Agent.OS)" | package-lock.json'`, `restoreKeys`); Microsoft-hosted agents start empty every run — cache or you pay the restore every time.
- **Artifacts**: `publish`/`download` (Pipeline Artifacts, fast, deduped) — not the legacy `PublishBuildArtifacts`; downloads in deployment jobs are automatic for `current`.
- **Matrix/parallel**: `strategy: { matrix: { linux: { img: ubuntu-latest }, windows: { img: windows-latest } } }`, `parallel: 4` for test slicing (the job gets `System.JobPositionInPhase` and `System.TotalJobsInPhase`).
- Container jobs run each step of the job inside a container (YAML pipelines only; classic pipelines do not support them).
- Timeouts: `timeoutInMinutes` defaults to 60 when not specified; 0 means the maximum limit. Use `continueOnError` with care.

## 4. Agents
| Option | Pick when |
|---|---|
| **Microsoft-hosted** (`vmImage`) | no private network needs; Windows and Linux images run on 2-core, 7 GB RAM VMs with at least 10 GB free disk; Microsoft cannot increase specs, so move to self-hosted, scale set or Managed DevOps Pools if they are too small |
| **Self-hosted** (VM/container, `pool: { name }`) | private endpoints, custom tools, GPUs, licensed software; you patch and rotate them; each agent runs one job at a time |
| **Scale set agents** (VMSS-backed pool) | autoscaling self-hosted agents backed by a Virtual Machine Scale Set; Microsoft recommends considering Managed DevOps Pools instead |
| **Managed DevOps Pools** (newer) | fully managed service, an evolution of scale set agent pools; the VMs or containers live in a Microsoft subscription, not yours |
- Capabilities/demands (`demands: [docker, java]`) route jobs.
- Parallel jobs: the number of jobs that can run at once in the organization; extra concurrent jobs queue, the usual "queued forever" cause. Every organization gets a free tier with at least one parallel job.
- Agent networking: see Microsoft's Allowed IP addresses and domain URLs page for the FQDNs and IP ranges to open.

## 5. Governance and hygiene
- Pipeline **decorators** (extension) inject steps org-wide (security scan, telemetry) without touching YAML; **required templates** on service connections/environments stop drift.
- Use a shallow fetch (`fetchDepth: 1`) where history is not needed, and do not persist checkout credentials unless a later step needs them.
- Validate YAML before running with the pipeline editor's validate action or the REST pipelines run API in preview mode, which returns the expanded YAML.

## Gotchas
- `${{ if }}` on a value that only exists at runtime (e.g. `variables['Build.SourceBranch']` from a variable group) is always false — template expressions only see parameters and pipeline-YAML-defined variables.
- A `deployment` job without `environment` is just a job — approvals/checks never apply.
- `trigger: none` + `pr: none` + a resource trigger is the pattern for release pipelines; forgetting `pr: none` means every PR deploys.
- Template repo `ref: main` + a breaking template change breaks 40 pipelines at once; tag and promote.
- Secrets aren't available to PR builds from forks (good) — tests that need them must be skipped, not fail.
- Self-hosted agents keep the workspace between runs (`workspace: { clean: all }` to reset) — stale `node_modules` and credential files are the classic contamination.
- Hosted agent images change monthly; pin tool versions (`UseDotNet@2`, `NodeTool@0`) or use container jobs.

## Verify
- [ ] `preview` run returns the expanded YAML with the expected stages for `deployTo: prod` and none for `deployTo: ''`.
- [ ] A PR run executes build + tests only; a main push runs build → dev; the prod stage waits on the environment check (see environments skill).
- [ ] Cache hit on the second run; build time drops accordingly.
- [ ] Jobs land on the intended pool (`Agent.Name`/`Agent.OS` in logs); queue time stays low at peak (parallel jobs and pool size adequate).

## Checked
2026-10-31 additions: caching (`Cache@2` key format and `restoreKeys`), schedule `always` default, compile-time vs runtime expression contexts and container-job requirement confirmed on Learn; unconfirmed `batch: true` and `services:` removed. 2026-10-28. Confirmed on Microsoft Learn (templates, jobs/phases, agents, hosted agents, scale set agents pages): extends templates and required template approval, `timeoutInMinutes` default 60 and 0 meaning maximum, `parallel` slicing variables, hosted agent specs and 10 GB free disk, parallel jobs and queueing, Managed DevOps Pools as the recommended evolution of scale set agents and where its VMs live, `workspace: clean: all`. Removed: agent FQDN list, KEDA and per-core agent advice, preview API version, run-name settings, org setting names, and the hosted-agent disk and Managed DevOps Pools subscription claims that contradicted the docs. Still unchecked, so the skill stays draft: caching, trigger and PR-trigger details, container jobs, expression-timing table.
Method: documentation only; no commands were run.
