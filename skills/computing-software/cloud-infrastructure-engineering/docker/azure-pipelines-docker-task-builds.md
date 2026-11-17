---
id: computing-software.cloud-infrastructure-engineering.docker.azure-pipelines-docker-task-builds
name: azure-pipelines-docker-task-builds
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, azure-pipelines-docker, docker-task, azure-devops, service-connection, acr, buildx-azure-pipelines]
level: practitioner
status: docs-checked
description: "Build and push images in Azure Pipelines with the Docker@2 task: service connections, buildAndPush limits, buildx with registry cache, ACR Tasks."
sources:
  - https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/docker-v2
  - https://learn.microsoft.com/en-us/azure/devops/pipelines/ecosystems/containers/acr-template
  - https://learn.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Azure Pipelines Docker@2 builds

## Basic build and push
```yaml
trigger: [main]
pool: { vmImage: ubuntu-latest }
variables:
  imageRepository: shop/api
  tag: $(Build.BuildId)
steps:
- task: Docker@2
  displayName: Build and push
  inputs:
    command: buildAndPush
    containerRegistry: acr-prod-connection      # Docker Registry service connection name
    repository: $(imageRepository)
    Dockerfile: src/Api/Dockerfile
    buildContext: src
    tags: |
      $(tag)
      $(Build.SourceVersion)
```
- `containerRegistry` is the name of a **Docker Registry service connection** (registry types: Docker Hub, Others,
  Azure Container Registry). Docker@2 does not support an Azure Resource Manager service connection; to reuse an
  existing service principal, create a Docker Registry connection of type "Others" with the SPN credentials.
- `buildAndPush` ignores `arguments` (no `--build-arg`, `--platform`, `--target`). For those use separate
  `command: build` (with `arguments:`) and `command: push` steps, or call docker/buildx in a script step after
  `command: login`.
- `Dockerfile` defaults to `**/Dockerfile`, `buildContext` to `**`, `tags` to `$(Build.BuildId)`.
- The task adds traceability labels to the image, named `com.azure.dev.image.*` (build number, build URI, source
  version and others).

## Build args, targets, platforms
```yaml
- task: Docker@2
  inputs: { command: login, containerRegistry: acr-prod-connection }
- script: |
    docker buildx create --use --name ci
    docker buildx build src -f src/Api/Dockerfile \
      --platform linux/amd64,linux/arm64 \
      --build-arg VERSION=$(Build.BuildNumber) \
      --cache-from type=registry,ref=<REGISTRY>.azurecr.io/shop/api:buildcache \
      --cache-to type=registry,ref=<REGISTRY>.azurecr.io/shop/api:buildcache,mode=max \
      -t <REGISTRY>.azurecr.io/shop/api:$(tag) --push
  displayName: buildx build
- task: Docker@2
  condition: always()
  inputs: { command: logout, containerRegistry: acr-prod-connection }
```
Registry cache (`type=registry`) keeps layers outside the agent; its `ref` must differ from the image you push, and
`mode=max` caches all stages. With the default docker driver registry cache needs the containerd image store, which is
why the example creates a builder first. Check the buildx documentation for multi-platform requirements.

## Alternatives
- `az acr build --registry <REGISTRY> --image shop/api:$(tag) src` (AzureCLI@2 task): builds in ACR Tasks, then pushes
  to the registry, with no Docker daemon needed on the agent.
- Clean up local Docker state on self-hosted agents that keep it between runs.

## Verify
- [ ] Image with both tags appears in the registry (`az acr repository show-tags --name <REGISTRY> --repository shop/api`).
- [ ] Second run reuses cache layers (build log shows cache hits).

## Checked
2026-10-28. Confirmed on the Docker@2 task reference (inputs, defaults, buildAndPush ignoring arguments, login/logout,
labels, no ARM connection support), the service connections page (Docker Registry connection types), the ACR
quickstart (`az acr build`), Docker's registry cache page and az CLI reference (`az acr build`, `az acr repository
show-tags`, checked by flag). Corrected: ACR via workload identity federation does not apply to Docker@2 (it takes a
Docker Registry connection only); input is spelled `Dockerfile`. Removed: Microsoft-hosted agent cache statement, binfmt
command, VMSS note, scanner and approval advice, `DOCKER_BUILDKIT` env.
Method: documentation only; no commands were run.
