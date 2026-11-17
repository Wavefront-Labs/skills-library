---
id: computing-software.devops-ci-cd.dagger.argo-tekton-dagger
name: argo-tekton-dagger
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, argo-workflows, tekton, kubernetes, sidecar, ci]
level: practitioner
status: docs-checked
description: "Run Dagger in Argo Workflows or Tekton on Kubernetes using an engine sidecar that shares a unix socket with the CLI container, with submit and run commands."
sources: [https://docs.dagger.io/0.21/getting-started/ci-integrations/argo-workflows, https://docs.dagger.io/0.21/getting-started/ci-integrations/tekton]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger in Argo Workflows and Tekton (Dagger 0.21 docs)

Goal: run a Dagger Function as one step of a Kubernetes-native workflow, with the engine as a sidecar. Prerequisite for both: a Kubernetes cluster configured for Dagger with a working `kubectl` profile.

## Shared pattern

- Add a sidecar `dagger-engine` using image `registry.dagger.io/engine:v<version>`, `securityContext.privileged: true` with `capabilities.add: [ALL]`, readiness probe `exec: ["dagger", "core", "version"]`.
- Mount `emptyDir` volumes at `/run/dagger` (socket) and `/var/lib/dagger` (storage) in the sidecar; mount `/run/dagger` in the CLI container.
- Set `_EXPERIMENTAL_DAGGER_RUNNER_HOST=unix:///run/dagger/engine.sock` in the CLI container, so it uses that engine.
- Pass `DAGGER_CLOUD_TOKEN` from a Kubernetes secret only if you use Dagger Cloud.

## Argo Workflows

Template with `sidecars` as above and `inputs.artifacts`: `project-source` (git repo, path `/work`) and `dagger-cli` (HTTP download of `https://github.com/dagger/dagger/releases/download/v<version>/dagger_v<version>_linux_amd64.tar.gz` to `/usr/local/bin`, `mode: 0755`). Container: `alpine:latest`, `command: ["sh", "-c"]`, `args: ["dagger -m github.com/kpenfound/dagger-modules/golang@v0.2.0 call test --source=."]`, `workingDir: /work`. Confirm CLI version and architecture fit the cluster.

```shell
argo submit -n argo --watch ./workflow.yaml
kubectl logs -f POD_NAME
```

Run it twice; the second run should be much faster from caching. Argo Workflows has no repo triggers itself; pair with Argo Events for CI.

## Tekton

1. `tkn hub install task git-clone`.
2. Pipeline `dagger-pipeline` (params `repo-url`, `dagger-cloud-token`; workspace `shared-data`): task `fetch-source` uses `git-clone`, then task `dagger` with `runAfter: ["fetch-source"]`.
3. Task `dagger`: the engine sidecar above; one step on image `docker:dind` that does `apk add curl`, installs the CLI with `BIN_DIR=/usr/local/bin`, and runs `dagger -m github.com/kpenfound/dagger-modules/golang@v0.2.0 call build --source=. --args=.`.
4. PipelineRun with a `volumeClaimTemplate` (ReadWriteOnce, 1Gi), `podTemplate.securityContext.fsGroup: 65532`, and the two params.

```shell
kubectl apply -f dagger-task.yaml
kubectl apply -f git-pipeline.yaml
kubectl create -f git-pipeline-run.yaml
tkn pipelinerun logs clone-read-run-<id> -f
```

Gotcha: the docs page prints the second apply as `git-pipeline-yaml`, a typo for the `git-pipeline.yaml` file it created earlier.

Related: computing-software.devops-ci-cd.dagger.gitlab-ci-dagger.

## Checked

2026-11-07

Read in full from the docs source: getting-started/ci-integrations/argo-workflows.mdx and tekton.mdx, plus the snippet files argo-workflow.yaml, tekton-dagger-task.yaml, tekton-git-pipeline.yaml and tekton-git-pipeline-run.yaml. Confirmed the sidecar settings, volume mounts, runner host variable, artifact settings, Tekton task and pipeline layout, fsGroup, storage request and the git-pipeline-yaml typo on the page. No corrections needed.

Method: documentation only; no commands were run.
