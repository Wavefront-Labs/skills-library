---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-registries
name: woodpecker-registries
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [registries, private-images, docker-config]
level: practitioner
status: docs-checked
description: "Authenticate Woodpecker agents to private container registries for step images."
sources: ["https://woodpecker-ci.org/docs/usage/registries", "https://woodpecker-ci.org/docs/administration/configuration/backends/docker", "https://woodpecker-ci.org/docs/administration/configuration/backends/kubernetes", "https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker registries

Add registry credentials in the repository settings to pull private images used as steps, or to avoid rate limits on public registries. The agent uses the credentials; they are never exposed to step containers, so they cannot be used to push and are safe with pull requests. To push, give the credentials to the appropriate plugin.

```yaml
steps:
  - name: build
    image: gcr.io/custom/golang
```

Woodpecker matches the registry hostname to each image:

- `gcr.io/foo/bar` has hostname `gcr.io`
- `foo/bar` has hostname `docker.io`
- `qux.com:8000/foo/bar` has hostname `qux.com:8000`

Hostname `docker.io` matches `golang`, `library/golang` and `bradrydzewski/golang:latest`.

Global registry support: point `WOODPECKER_DOCKER_CONFIG` at a Docker config file on the server (for example a `config.json`) to make a private registry available to all pipelines. With the Docker backend, credential helpers can be configured in that file; install the helper in the server image.

On Kubernetes, put registry credentials in Kubernetes Secrets in the namespace named by `WOODPECKER_BACKEND_K8S_NAMESPACE` and list them in `WOODPECKER_BACKEND_K8S_PULL_SECRET_NAMES` on the agent.

## Checked

2026-11-03. Confirmed against: registries (hostname matching, credentials never exposed to steps), Docker backend (WOODPECKER_DOCKER_CONFIG, credential helper) and Kubernetes backend (pull secrets). Removed: the claim that the repository-level registry extension wins over the global one.

Method: documentation only; no commands were run.
