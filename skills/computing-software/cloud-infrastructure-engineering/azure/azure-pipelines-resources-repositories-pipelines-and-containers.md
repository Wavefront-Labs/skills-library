---
id: computing-software.cloud-infrastructure-engineering.azure.azure-pipelines-resources-repositories-pipelines-and-containers
name: azure-pipelines-resources-repositories-pipelines-and-containers
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, azure-pipelines, pipeline-resources, repository-resources, container-jobs, pipeline-completion-triggers, multi-repo-checkout, service-containers, package-resources, webhook-resources, yaml-pipelines]
level: practitioner
status: docs-checked
description: "Use Azure Pipelines YAML resources: multi-repo checkout and template repos, pipeline-completion triggers with artifact download, container jobs and service containers, webhooks."
sources: ["https://learn.microsoft.com/en-us/azure/devops/pipelines/process/resources", "https://learn.microsoft.com/en-us/azure/devops/pipelines/repos/multi-repo-checkout", "https://learn.microsoft.com/en-us/azure/devops/pipelines/process/container-phases", "https://learn.microsoft.com/en-us/azure/devops/pipelines/process/service-containers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Pipelines resources — repositories, pipelines, containers

**Goal:** a pipeline that consumes other repos, other pipelines' artifacts and container
images declaratively, with traceability of exactly which version of each it used.

## 1. Repository resources
```yaml
resources:
  repositories:
    - repository: templates            # alias
      type: git                        # Azure Repos; github / githubenterprise / bitbucket need endpoint:
      name: Platform/pipeline-templates
      ref: refs/tags/v3.2.0            # pin templates
    - repository: shared
      type: github
      endpoint: gh-wavefront           # service connection
      name: wavefront/shared-lib
      trigger: { branches: { include: [main] } }   # optional: CI from the other repo (Azure Repos + GitHub)
steps:
  - checkout: self
  - checkout: shared                    # multi-repo checkout
```
- With multiple checkouts, check each repository's path on the multi-repo checkout page; scripts that assume a single source directory must adapt.

## 2. Pipeline resources (chain pipelines)
```yaml
resources:
  pipelines:
    - pipeline: build                   # alias
      source: orders-ci                 # pipeline name
      project: Shop
steps:
  - download: build                     # artifacts into $(Pipeline.Workspace)/build/
    artifact: drop
  - script: echo "Deploying the build pipeline artifact"
```
- Deployment pipelines triggered by CI completion keep build and deploy separate while tracing the exact run.

## 3. Container jobs and service containers
```yaml
resources:
  containers:
    - container: build
      image: myacr.azurecr.io/build/dotnet-sdk:8.0
    - container: pg
      image: postgres:16
      env: { POSTGRES_PASSWORD: test }
      ports: [ "5432:5432" ]
jobs:
  - job: test
    pool: { vmImage: ubuntu-latest }
    container: build                    # every step runs inside this container
    services: { postgres: pg }          # side-car reachable as host 'postgres'
    steps: [ { script: dotnet test } ]
```
- Azure Pipelines can run Linux or Windows containers: use the hosted Ubuntu pool for Linux containers and the hosted Windows pool for Windows containers. Windows containers need a matching host and container kernel version.

## Gotchas
- Templates from an unpinned `ref` mean any merge to the template repo changes every pipeline at the next run — pin tags.

## Verify
- [ ] Run summary *Resources* lists each repository commit and pipeline run used.
- [ ] A completed `orders-ci` main run triggers the deploy pipeline and artifacts download.
- [ ] Container job tests reach the `postgres` service container.

## Checked
2026-10-28. Confirmed on the pipelines resources, multi-repo checkout and container jobs pages: `resources.pipelines`, `download:` of pipeline artifacts into `$(Pipeline.Workspace)/<pipeline>/<artifact>`, Linux and Windows container jobs on the hosted Ubuntu and Windows pools, Windows container kernel matching.
Removed (not confirmed): `fetchDepth`, the self checkout path claim, tag triggers, `runName`/`sourceBranch` variables, registry `endpoint`, authorization-scope and prompt notes, ACR/webhook triggers, hosted Windows service container limits and image digest listing.

Method: documentation only; no commands were run.
