---
id: computing-software.devops-ci-cd.dagger.gitlab-ci-dagger
name: gitlab-ci-dagger
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, gitlab-ci, ci, docker-in-docker, kubernetes, gitlab-runner]
level: practitioner
status: docs-checked
description: "Run Dagger in GitLab CI using the Docker executor with dind or the Kubernetes executor with pre-provisioned engine nodes, including runner ConfigMap settings."
sources: [https://docs.dagger.io/0.21/getting-started/ci-integrations/gitlab-ci, https://docs.dagger.io/0.21/reference/deployment/openshift]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger in GitLab CI (Dagger 0.21 docs)

Goal: call Dagger Functions from `.gitlab-ci.yml` on Docker or Kubernetes runners.

Supported runners: GitLab-hosted (Docker Machine executor), self-managed Docker executor, or self-managed Kubernetes executor. The job downloads the CLI, runs `dagger call ...`, and the CLI finds or starts an engine.

## Docker executor (engine via dind)

```yaml
.docker:
  image: docker:latest
  services:
    - docker:${DOCKER_VERSION}-dind
  variables:
    DOCKER_HOST: tcp://docker:2376
    DOCKER_TLS_VERIFY: '1'
    DOCKER_TLS_CERTDIR: '/certs'
    DOCKER_CERT_PATH: '/certs/client'
    DOCKER_DRIVER: overlay2
    DOCKER_VERSION: '27.2.0'
    DAGGER_CLOUD_TOKEN: $DAGGER_CLOUD_TOKEN   # masked/protected CI variable
.dagger:
  extends: [.docker]
  before_script:
    - apk add curl
    - curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=/usr/local/bin sh
hello:
  extends: [.dagger]
  script:
    - dagger -m github.com/shykes/daggerverse/hello@v0.1.2 call hello --greeting="bonjour" --name="monde"
```

Test then build: `test` job runs `dagger -m github.com/kpenfound/dagger-modules/golang@v0.2.0 call test --source=.`; `build` has `needs: ["test"]` and runs `... call build-container --source=. --args=. publish --address=ttl.sh/my-app-$RANDOM`.

## Kubernetes executor

Use `image: alpine:latest`, same `DAGGER_CLOUD_TOKEN` variable, and install the CLI to a writable path: `curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=/tmp sh`. Runners must be limited to nodes that already host a Dagger Engine, using taints/tolerations and pod affinity on a `dagger-node` key (node side: see the OpenShift deployment page; Helm values use toleration key `dagger-node` operator `Exists` and matching node affinity).

Runner ConfigMap (`config.toml`) key points from the page: `environment = ["HOME=/tmp","FF_GITLAB_REGISTRY_HELPER_IMAGE=1", "_EXPERIMENTAL_DAGGER_RUNNER_HOST=unix:///run/dagger/engine.sock"]`, `pre_build_script = "export PATH=\"/tmp/:$PATH\""`, `executor = "kubernetes"`, namespace `dagger`, `privileged = true`, node affinity `dagger-node In [true]`, toleration `"dagger-node" = ""`, run as root, and a `host_path` volume `/run/dagger` so jobs reach the engine socket. A `Runner` resource (`apps.gitlab.com/v1beta2`, name `dagger-runner`, `tags: dagger`, `runUntagged: false`) references that config. Replace the `YOUR-GITLAB-URL` and `YOUR-GITLAB-RUNNER-TOKEN-REFERENCE` placeholders.

Related: computing-software.devops-ci-cd.dagger.github-actions-dagger, computing-software.devops-ci-cd.dagger.argo-tekton-dagger.

## Checked

2026-11-07

Read getting-started/ci-integrations/gitlab.mdx in full (live slug /getting-started/ci-integrations/gitlab-ci; the old .../gitlab URL returned 404, fixed in sources), all six snippet files it embeds (gitlab-docker-hello.yml, gitlab-docker-test-build.yml, gitlab-kubernetes-hello.yml, gitlab-kubernetes-test-build.yml, gitlab-runner-config.yml, gitlab-runner.yml), and reference/deployment/openshift.mdx with its values snippet (now cited in sources) for the Helm toleration and node affinity statement. Confirmed supported runners, dind setup and variables, install script and BIN_DIR values, the test and build jobs, config.toml settings, the Runner resource and the placeholders. No claims removed.

Method: documentation only; no commands were run.
