---
id: computing-software.devops-ci-cd.gitlab-ci.service-image-pull-policy-and-private-registries
name: service-image-pull-policy-and-private-registries
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, service-pull-policy, private-service-images, docker-auth-config, service-variables]
level: practitioner
status: docs-checked
description: "Pull service containers reliably: per-service pull_policy, DOCKER_AUTH_CONFIG for private registries, the dependency proxy image prefix, and per-service variables."
sources: ["https://docs.gitlab.com/ci/services/", "https://docs.gitlab.com/ci/yaml/#servicespull_policy", "https://docs.gitlab.com/ci/docker/using_docker_images/#access-an-image-from-a-private-container-registry", "https://docs.gitlab.com/runner/configuration/advanced-configuration/#the-runnersdocker-section", "https://docs.gitlab.com/ci/variables/predefined_variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service image pull policy and private registries

## 1. Per-service options
```yaml
integration:
  image: python:3.12
  services:
    - name: registry.example.com/platform/postgres-ci:16
      alias: db
      pull_policy: if-not-present        # needs runner allowed_pull_policies to include it
      variables:
        POSTGRES_PASSWORD: ci
        POSTGRES_DB: app
    - name: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/redis:7     # Docker Hub via dependency proxy
      alias: cache
      command: ["redis-server", "--save", ""]
```
`pull_policy` accepts `always`, `if-not-present` or `never`, as one value or a list (`[always, if-not-present]`). Runner side:
`allowed_pull_policies = ["always", "if-not-present"]` under `[runners.docker]`; a job whose policy is not allowed fails.

## 2. Private registry auth for services
The GitLab docs list these credential sources for private-registry images:
1. `DOCKER_AUTH_CONFIG` CI/CD variable (project/group):
```json
{"auths":{"registry.example.com":{"auth":"<base64 of user:token>"}}}
```
   (`printf 'user:token' | openssl base64 -A`) — use a deploy token / robot account with read-only scope.
   The full `hostname:port` of the registry must match the image reference in the YAML.
2. Runner-level `DOCKER_AUTH_CONFIG` environment variable in `config.toml`, or `config.json` in the `$HOME/.docker` directory of the user running the runner.

## 3. Reliability
- Pull Docker Hub images through the dependency proxy prefix (`CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX`) or a mirror.
- `if-not-present` + mutable tags = stale databases; pin tags (`postgres:16.4`) or digests.
- Service health: the runner's `wait_for_services_timeout` (default 30 seconds, `-1` disables) bounds the wait for services; the job still needs its own readiness loop (`pg_isready -h db`).

## Verify
- [ ] Log shows `Starting service registry.example.com/...` with no pull errors; second run on the same host skips pulling with if-not-present.

## Checked

2026-10-31. Confirmed against the GitLab CI services page, the CI YAML reference (services:pull_policy values, array form, failure when the runner disallows a policy), the private-registry section of the Docker images page (DOCKER_AUTH_CONFIG sources, `openssl base64 -A`, full hostname:port match), the Runner docker section (allowed_pull_policies, wait_for_services_timeout default 30 and -1) and the predefined variables page (CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX).
Removed: the Kubernetes allowed_pull_policies location, the job-token registry claim, the quoted pull error, and the claim that Docker Hub rate limits hit services first.

Method: documentation only; no commands were run.
