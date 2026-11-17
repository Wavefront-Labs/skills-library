---
id: computing-software.devops-ci-cd.skaffold.pipeline-stages
name: pipeline-stages
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [pipeline, stages, workflow, dev-loop]
level: intro
status: docs-checked
description: "The stages Skaffold chains together, from init to cleanup, and the commands that expose them."
sources:
  - "https://skaffold.dev/docs/pipeline-stages/"
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold has a multi-stage workflow. It collects source code, builds artifacts with the tool of your choice, tags them and pushes them to the repository you specify, then helps deploy them to your Kubernetes cluster with the tools you prefer. Skaffold allows you to skip stages: for example, with a local cluster such as Minikube it does not push artifacts to a remote repository.

Stages as listed on the page:

- Init: generate a starting point for Skaffold configuration
- Build: build images with different builders
- Render: render manifests with different renderers
- Tag: tag images based on different policies
- Test: run tests with testers
- Deploy: deploy with kubectl, kustomize or helm
- Verify: verify deployments with specified test containers
- File Sync: sync changed files directly to containers
- Log Tailing: tail logs from workloads
- Port Forwarding: forward ports from services and arbitrary resources to localhost
- Deploy Status Checking: wait for deployed resources to stabilize
- Lifecycle Hooks: run code triggered by different events during the Skaffold process lifecycle
- Cleanup: clean up manifests and images

Commands (descriptions from the CLI reference): `run` (run a pipeline), `dev` (run a pipeline in development mode), `debug` (run a pipeline in debug mode), `build` (build the artifacts), `test` (run tests against your built application images), `deploy` (deploy pre-built artifacts), `delete` (delete any resources deployed by Skaffold), `render` (generate rendered Kubernetes manifests), `apply` (apply hydrated manifests to a cluster), `verify` (run verification tests against Skaffold deployments), `init` (generate configuration for deploying an application).

## Checked

2026-11-04. Read the whole Skaffold Pipeline Stages page and the command list at the top of the CLI reference. Confirmed the stage list, the skip-stages behaviour and command descriptions. Removed: which commands run which stages, the "typical choice" recommendations, the list of config sections per stage and the profiles advice (the page states none of these).
Method: documentation only; no commands were run.
